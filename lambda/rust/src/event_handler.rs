use aws_lambda_events::event::sqs::SqsEvent;
use lambda_runtime::{Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use serde_json::{self, json};

use crate::schema::get_schema;

#[derive(Deserialize, Serialize, Default)]
#[serde(rename_all="camelCase")]
pub struct User {
    id: String,
    session_id: String,
    device_id: Option<String>,
}

#[derive(Deserialize, Serialize, Default)]
#[serde(rename_all="camelCase")]
pub struct Event {
    event_id: String,
    user: User,
    emitter_code: u32,
    action: String,
}

pub(crate) async fn function_handler(lambda_event: LambdaEvent<SqsEvent>) -> Result<(), Error> {
    let validator = jsonschema::validator_for(&get_schema())?;
    let payload = lambda_event.payload;
    
    for message in payload.records {
        let body = match message.body {
            Some(b) => b,
            None => panic!("No message body!")
        };
        let event: Event = serde_json::from_str(&body)?;
        assert!(validator.is_valid(&json!(&event)));
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
    async fn test_event_handler_parses_a_valid_event() {
        let body = serde_json::to_string(&Event {
            event_id: "event-id".to_string(),
            emitter_code: 50,
            action: "sign_in".to_string(),
            user: User {
                id: "user-id".to_string(),
                session_id: "session-id".to_string(),
                device_id: Some("device-id".to_string()),
            },
        }).unwrap();
        let event = LambdaEvent::new(
            build_event(&body),
            Context::default(),
        );
        let response = function_handler(event).await.unwrap();
        assert_eq!((), response);
    }

    #[tokio::test]
    #[should_panic]
    async fn test_event_handler_panics_with_invalid_payload() {
        let body = serde_json::to_string(&"").unwrap();
        let event = LambdaEvent::new(
            build_event(&body),
            Context::default(),
        );
        function_handler(event).await.unwrap();
    }

    #[tokio::test]
    #[should_panic]
    async fn test_event_handler_panics_when_payload_doesnt_validate_against_schema() {
        // emitterCode too high
        let body = serde_json::to_string(&Event {
            event_id: "event-id".to_string(),
            emitter_code: 5000,
            action: "sign_in".to_string(),
            user: User {
                id: "user-id".to_string(),
                session_id: "session-id".to_string(),
                device_id: Some("device-id".to_string()),
            },
        }).unwrap();
        let event = LambdaEvent::new(
            build_event(&body),
            Context::default(),
        );
        function_handler(event).await.unwrap();
        
    }
}
