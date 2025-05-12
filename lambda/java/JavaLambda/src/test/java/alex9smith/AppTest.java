package alex9smith;

import com.amazonaws.services.lambda.runtime.events.SQSEvent;
import com.amazonaws.services.lambda.runtime.events.SQSEvent.SQSMessage;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.Test;

class AppTest {
  @Test
  void handleRequest_shouldReturnConstantValue() {
    List<SQSMessage> records = Collections.emptyList();
    SQSEvent event = new SQSEvent();
    event.setRecords(records);

    App function = new App();
    SQSEvent result = function.handleRequest(event, null);
    assertEquals(event, result);
  }
}
