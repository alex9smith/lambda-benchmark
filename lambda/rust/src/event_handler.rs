use aws_lambda_events::event::sqs::SqsEvent;
use aws_sdk_dynamodb::types::AttributeValue;
use aws_sdk_dynamodb::Client;
use lambda_runtime::{Error, LambdaEvent};
use serde::{Deserialize, Serialize};
use serde_json::{self, json};
use std::collections;
use std::env;

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

pub(crate) async fn write_event(
    client: &Client,
    event: Event,
    table: &String,
) -> Result<(), aws_sdk_dynamodb::Error> {
    let mut user = collections::HashMap::new();
    user.insert("id".to_string(), AttributeValue::S(event.user.id));
    user.insert(
        "sessionId".to_string(),
        AttributeValue::S(event.user.session_id),
    );

    if event.user.device_id.is_some() {
        user.insert(
            "deviceId".to_string(),
            AttributeValue::S(event.user.device_id.unwrap()),
        );
    }

    let request = client
        .put_item()
        .table_name(table)
        .item("eventId", AttributeValue::S(event.event_id))
        .item(
            "emitterCode",
            AttributeValue::N(event.emitter_code.to_string()),
        )
        .item("action", AttributeValue::S(event.action))
        .item("user", AttributeValue::M(user));

    request.send().await?;

    Ok(())
}

pub(crate) async fn function_handler(lambda_event: LambdaEvent<SqsEvent>) -> Result<(), Error> {
    let validator = jsonschema::validator_for(&get_schema())?;
    let payload = lambda_event.payload;

    let table_name = env::var("TABLE_NAME")?;
    let config = aws_config::load_defaults(aws_config::BehaviorVersion::latest()).await;
    let client = aws_sdk_dynamodb::Client::new(&config);

    for message in payload.records {
        let body = match message.body {
            Some(b) => b,
            None => panic!("No message body!"),
        };
        let event: Event = serde_json::from_str(&body)?;
        validate_event(&validator, &event);
        write_event(&client, event, &table_name).await?;
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
