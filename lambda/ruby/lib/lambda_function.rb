require "json"
require "json-schema"

module Lambda
  class Handler
    def self.process(lambda_event:, context:)
      lambda_event['Records'].each do |message|
        event = JSON.parse(message)
        self.validate_event(event)
        self.write_to_dynamo_db(event)
      end
    end

    def self.validate_event(event)
      JSON::Validator.validate!(Lambda.schema, event)
    end

    def self.write_to_dynamo_db(event)
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
