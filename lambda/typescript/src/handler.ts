import { SQSEvent, Context } from "aws-lambda";
import { Logger } from "@aws-lambda-powertools/logger";

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

export function validateEvent(event: Event): void {}

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
