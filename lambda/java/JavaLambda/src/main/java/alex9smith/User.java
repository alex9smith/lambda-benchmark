package alex9smith;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "id",
    "sessionId",
    "deviceId"
})
public class User {
  @JsonProperty("id")
  private String id;

  @JsonProperty("sessionId")
  private String sessionId;

  @JsonProperty("deviceId")
  private String deviceId;

  public User() {
    super();
  }

  public Map<String, AttributeValue> toAttributeMap() {
    HashMap<String, AttributeValue> map = new HashMap<>();
    map.put("id", AttributeValue.fromS(id));
    map.put("sessionId", AttributeValue.fromS(sessionId));
    map.put("deviceId", AttributeValue.fromS(deviceId));

    return map;
  }
}
