package alex9smith;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.SQSEvent;
import com.amazonaws.services.lambda.runtime.events.SQSEvent.SQSMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.InputFormat;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion.VersionFlag;

import software.amazon.awssdk.services.dynamodb.DynamoDbAsyncClient;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;
import software.amazon.awssdk.services.dynamodb.model.PutItemResponse;

/**
 * Lambda function entry point. You can change to use other pojo type or
 * implement
 * a different RequestHandler.
 *
 * @see <a
 *      href=https://docs.aws.amazon.com/lambda/latest/dg/java-handler.html>Lambda
 *      Java Handler</a> for more information
 */
public class App implements RequestHandler<SQSEvent, Object> {
  private final DynamoDbAsyncClient dynamoDbClient;
  private final JsonSchema jsonSchema;
  private final ObjectMapper objectMapper;
  private final String tableName;

  public App() {
    String schemaData = "{\n" + //
        "  \"$schema\": \"http://json-schema.org/draft-07/schema#\",\n" + //
        "  \"type\": \"object\",\n" + //
        "  \"properties\": {\n" + //
        "    \"eventId\": {\n" + //
        "      \"type\": \"string\",\n" + //
        "      \"maxLength\": 128\n" + //
        "    },\n" + //
        "    \"emitterCode\": {\n" + //
        "      \"type\": \"integer\",\n" + //
        "      \"minimum\": 0,\n" + //
        "      \"maximum\": 100\n" + //
        "    },\n" + //
        "    \"action\": {\n" + //
        "      \"type\": \"string\",\n" + //
        "      \"enum\": [\"sign_in\", \"sign_out\", \"create_account\", \"delete_account\"]\n" + //
        "    },\n" + //
        "    \"user\": {\n" + //
        "      \"type\": \"object\",\n" + //
        "      \"properties\": {\n" + //
        "        \"id\": {\n" + //
        "          \"type\": \"string\",\n" + //
        "          \"maxLength\": 128\n" + //
        "        },\n" + //
        "        \"sessionId\": {\n" + //
        "          \"type\": \"string\",\n" + //
        "          \"maxLength\": 128\n" + //
        "        },\n" + //
        "        \"deviceId\": {\n" + //
        "          \"type\": \"string\",\n" + //
        "          \"maxLength\": 128\n" + //
        "        }\n" + //
        "      },\n" + //
        "      \"required\": [\"id\", \"sessionId\"]\n" + //
        "    }\n" + //
        "  },\n" + //
        "  \"required\": [\"eventId\", \"emitterCode\", \"action\", \"user\"]\n" + //
        "}\n";

    dynamoDbClient = DependencyFactory.dynamoDbClient();
    JsonSchemaFactory factory = JsonSchemaFactory.getInstance(VersionFlag.V7);
    jsonSchema = factory.getSchema(schemaData);
    objectMapper = new ObjectMapper();
    tableName = System.getenv("TABLE_NAME");

  }

  @Override
  public SQSEvent handleRequest(final SQSEvent input, final Context context) {
    ArrayList<CompletableFuture<PutItemResponse>> futures = new ArrayList<>();
    System.out.println(input);
    for (SQSMessage message : input.getRecords()) {
      try {
        System.out.println(message.getBody());
        jsonSchema.validate(message.getBody(), InputFormat.JSON);
        Event event = objectMapper.readValue(message.getBody(), Event.class);
        PutItemRequest request = PutItemRequest.builder()
            .tableName(tableName)
            .item(event.toAttributeMap())
            .build();
        futures.add(dynamoDbClient.putItem(request));

      } catch (JsonProcessingException e) {
        e.printStackTrace();
        System.exit(1);
      }

    }

    List<PutItemResponse> results = futures.stream().map(CompletableFuture::join).toList();
    System.out.println(results.size());

    return input;
  }
}
