import { SQSEvent, Context } from "aws-lambda";
import { Logger } from "@aws-lambda-powertools/logger";
import { Ajv } from "ajv";
import { schema } from "./schema";

export interface Event {
  eventId: string;
  emitterCode: number;
  action: string;
  user: {
    id: string;
    sessionId: string;
    deviceId?: string;
  };
}

const ajv = new Ajv();
const validate = ajv.compile(schema);

export function validateEvent(event: Event): void {
  validate(event);

  if (validate.errors) {
    const first = validate.errors.pop();
    throw new Error(`Event failed validation: ${first?.message}`);
  }
}

export async function writeEventToDynamoDb(event: Event): Promise<void> {}

const logger = new Logger();

export async function handler(
  event: SQSEvent,
  context: Context
): Promise<void> {
  logger.addContext(context);
  await Promise.all(
    event.Records.map(async (record) => {
      try {
        const event: Event = JSON.parse(record.body);
        validateEvent(event);
        await writeEventToDynamoDb(event);
      } catch (error) {
        logger.error((error as Error).message);
        throw error;
      }
    })
  );
}
