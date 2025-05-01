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

const missingProperty = {
  eventId: "event-id",
  emitterCode: 50,
  user: {
    id: "user-id",
    sessionId: "session-id",
    deviceId: "device-id",
  },
};

const emitterCodeTooLarge: Event = {
  eventId: "event-id",
  emitterCode: 5000,
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

  test("it throws an error when the event is missing a property", () => {
    expect(() => {
      validateEvent(missingProperty as unknown as Event);
    }).toThrow();
  });

  test("it throws an error when the event matches the interface but not the schema", () => {
    expect(() => {
      validateEvent(emitterCodeTooLarge);
    }).toThrow();
  });
});
