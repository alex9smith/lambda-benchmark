require 'aws-sdk-dynamodb'
require "json"
require "json-schema"

module Lambda
  class Handler
    def self.process(event:, context:)
      client = Aws::DynamoDB::Client.new
      table = Aws::DynamoDB::Resource.new(client: client).table(ENV['TABLE_NAME'])

      event['Records'].each do |message|
        sqs_event = JSON.parse(message['body'])
        self.validate_event(sqs_event)
        self.write_to_dynamo_db(table, sqs_event)
      end
    end

    def self.validate_event(event)
      JSON::Validator.validate!(Lambda.schema, event)
    end

    def self.write_to_dynamo_db(table, event)
      table.put_item(item: event)
    end
  end

  def schema
    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "eventId": {
          "type": "string",
          "maxLength": 128
        },
        "emitterCode": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        },
        "action": {
          "type": "string",
          "enum": ["sign_in", "sign_out", "create_account", "delete_account"]
        },
        "user": {
          "type": "object",
          "properties": {
            "id": {
              "type": "string",
              "maxLength": 128
            },
            "sessionId": {
              "type": "string",
              "maxLength": 128
            },
            "deviceId": {
              "type": "string",
              "maxLength": 128
            }
          },
          "required": ["id", "sessionId"]
        }
      },
      "required": ["eventId", "emitterCode", "action", "user"]
    }
  end
  module_function :schema
end
