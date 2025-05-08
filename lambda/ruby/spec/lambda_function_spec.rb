require "json-schema"
require 'rspec'
require 'lambda_function'

RSpec.describe Lambda do
  describe "#validate_event" do
    it "doesn't raise an error when parsing a valid event" do
      valid_event = {
        "eventId" => "event_id",
        "emitterCode" => 50,
        "action" => "sign_in",
        "user" => {
          "id" => "id",
          "sessionId" => "session_id",
          "deviceId" => "device_id"
        }
      }

      expect {Lambda::Handler.validate_event(valid_event) }.not_to raise_error
    end

    it "does raise an error when parsing an invalid event" do
      invalid_event = {
        "eventId" => "event_id",
        "emitterCode" => 5000,
        "action" => "sign_in",
        "user" => {
          "id" => "id",
          "sessionId" => "session_id",
          "deviceId" => "device_id"
        }
      }

      expect {Lambda::Handler.validate_event(invalid_event) }.to raise_error(JSON::Schema::ValidationError)
    end
  end
end
