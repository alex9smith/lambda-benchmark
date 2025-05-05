use aws_lambda_events::event::sqs::SqsEvent;
use lambda_runtime::{Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use serde_json;

#[derive(Deserialize, Serialize, Default)]
pub struct User {
    id: String,
    session_id: String,
    devide_id: Option<String>,
}

#[derive(Deserialize, Serialize, Default)]
pub struct Event {
    event_id: String,
    user: User,
    emitter_code: u32,
    action: String,
}

pub(crate) async fn function_handler(lambda_event: LambdaEvent<SqsEvent>) -> Result<(), Error> {
    // Extract some useful information from the request
    let payload = lambda_event.payload;
    for message in payload.records {
        let event: Event = serde_json::from_str(&message.body.unwrap()).unwrap();
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use aws_lambda_events::sqs::SqsMessage;
    use lambda_runtime::{Context, LambdaEvent};
    use std::collections::HashMap;

    fn build_message(body: &str) -> SqsMessage {
        SqsMessage {
            message_id: None,
            receipt_handle: None,
            aws_region: None,
            body: Some(body.to_string()),
            md5_of_body: None,
            md5_of_message_attributes: None,
            event_source: None,
            event_source_arn: None,
            attributes: HashMap::new(),
            message_attributes: HashMap::new(),
        }
    }

    fn build_event(body: &str) -> SqsEvent {
        SqsEvent {
            records: vec![build_message(body)],
        }
    }

    #[tokio::test]
    async fn test_event_handler() {
        let event = LambdaEvent::new(
            build_event(&serde_json::to_string(&Event::default()).unwrap()),
            Context::default(),
        );
        let response = function_handler(event).await.unwrap();
        assert_eq!((), response);
    }
}
