import java.util.HashMap;

import org.json.JSONObject;

import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
/**
 * Hello world!
 *
 */
public class App 
{
    public static final String ACCOUNT_SID = System.getenv("ACCOUNT_SID");
    public static final String AUTH_TOKEN = System.getenv("AUTH_TOKEN");

    public static void main( String[] args )
    {
        Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        Message message = Message.creator(
            new PhoneNumber("whatsapp:+"), 
            new PhoneNumber("whatsapp:+"), 
            (String) null
        )
        .setContentSid("HXb5b62575e6e4ff6129ad7c8efe1f983e")
        .setContentVariables(new JSONObject(new HashMap<String, Object>() {{
            put("1", "22 July 2026");
			put("2", "3:15pm");
        }}).toString()).create();    

        System.out.println(message.getSid());
    }

    private static void sendMessage() {
        Message message = Message.creator(
                new PhoneNumber("+"),
                new PhoneNumber("+"),
                "Test"
        ).create();

        System.out.println(message.getSid());
    }
}
