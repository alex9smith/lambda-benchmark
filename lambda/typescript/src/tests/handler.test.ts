import { validateEvent, Event } from "../handler";

const validEvent: Event = {
  eventId: "event-id",
  emitterCode: 50,
  action: "sign_in",
  user: {
    id: "user-id",
    sessionId: "session-id",
    deviceId: "device-id",
  },
};

describe("validateEvent", () => {
  test("it doesn't throw an error for a valid event", () => {
    expect(() => {
      validateEvent(validEvent);
    }).not.toThrow();
  });

  test.todo("it throws an error when the event is missing a property");

  test.todo(
    "it throws an error when the event matches the interface but not the schema"
  );
});
