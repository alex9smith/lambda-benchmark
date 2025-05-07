use aws_lambda_events::event::sqs::SqsEvent;
use lambda_runtime::{Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use serde_json::{self, json};

use crate::schema::get_schema;

#[derive(Deserialize, Serialize, Default)]
#[serde(rename_all = "camelCase")]
pub struct User {
    id: String,
    session_id: String,
    device_id: Option<String>,
}

#[derive(Deserialize, Serialize, Default)]
#[serde(rename_all = "camelCase")]
pub struct Event {
    event_id: String,
    user: User,
    emitter_code: u32,
    action: String,
}

pub(crate) fn validate_event(validator: &jsonschema::Validator, event: &Event) {
    assert!(validator.is_valid(&json!(&event)));
}

pub(crate) async fn function_handler(lambda_event: LambdaEvent<SqsEvent>) -> Result<(), Error> {
    let validator = jsonschema::validator_for(&get_schema())?;
    let payload = lambda_event.payload;

    for message in payload.records {
        let body = match message.body {
            Some(b) => b,
            None => panic!("No message body!"),
        };
        let event: Event = serde_json::from_str(&body)?;
        validate_event(&validator, &event);
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_doesnt_panic_for_a_good_event() {
        let event = Event {
            event_id: "event-id".to_string(),
            emitter_code: 50,
            action: "sign_in".to_string(),
            user: User {
                id: "user-id".to_string(),
                session_id: "session-id".to_string(),
                device_id: Some("device-id".to_string()),
            },
        };
        let validator = jsonschema::validator_for(&get_schema()).unwrap();
        validate_event(&validator, &event);
    }

    #[test]
    #[should_panic]
    fn test_validate_panics_for_an_event_which_doesnt_match_the_schema() {
        // emitterCode too high
        let event = Event {
            event_id: "event-id".to_string(),
            emitter_code: 5000,
            action: "sign_in".to_string(),
            user: User {
                id: "user-id".to_string(),
                session_id: "session-id".to_string(),
                device_id: Some("device-id".to_string()),
            },
        };
        let validator = jsonschema::validator_for(&get_schema()).unwrap();
        validate_event(&validator, &event);
    }
}
