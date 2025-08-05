package alex9smith;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "eventId",
    "emitterCode",
    "action",
    "user"
})
public class Event {
  @JsonProperty("eventId")
  private String eventId;

  @JsonProperty("emitterCode")
  private int emitterCode;

  @JsonProperty("action")
  private String action;

  @JsonProperty("user")
  private User user;

  public Event() {
    super();
  }

  public Map<String, AttributeValue> toAttributeMap() {
    HashMap<String, AttributeValue> map = new HashMap<>();
    map.put("eventId", AttributeValue.fromS(eventId));
    map.put("emitterCode", AttributeValue.fromN(String.valueOf(emitterCode)));
    map.put("action", AttributeValue.fromS(action));
    map.put("user", AttributeValue.fromM(user.toAttributeMap()));

    return map;
  }
}
