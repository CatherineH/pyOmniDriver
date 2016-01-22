import py4j.GatewayServer;
import com.oceanoptics.omnidriver.api.wrapper.Wrapper;
public class SpectrometerServer extends Wrapper {
	 // SpectrometerServer is a gateway server to the OmniDriver wrapper.	
	
	  public static void main(String[] args) {
		SpectrometerServer app = new SpectrometerServer();
	    // app is now the gateway.entry_point
	    GatewayServer server = new GatewayServer(app);	    
	    server.start();	    
	  }
}
