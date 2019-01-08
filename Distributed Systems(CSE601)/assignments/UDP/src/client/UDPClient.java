package client;
import java.net.*;
import java.util.Arrays;
import java.util.Scanner;
import java.io.*;
public class UDPClient{
	
	static DatagramSocket aSocket = null;
	
	public static void main(String args[]) throws IOException{
		// args give message contents and server hostname
		aSocket = new DatagramSocket();
		String methodName = "";
		byte[] ip = new byte[]{  127, 0,0,1};
		InetAddress aHost = InetAddress.getByAddress(ip);
		int serverPort = 6789;
		DatagramPacket request;
		String retString;
		byte[] buffer  = new byte[1000];
		request = 
				new DatagramPacket(methodName.getBytes(), methodName.length(), aHost, serverPort);
		aSocket.send(request);
		
		
		DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
		aSocket.receive(reply);
		System.out.println("Reply: " + new String(reply.getData())+reply.getLength());
		
		Scanner input = new Scanner(System.in);
		System.out.print("Enter name of class:");
		String className = input.nextLine();
		System.out.print("Enter name of method:");
		methodName = input.nextLine();
		
		methodName = className+" "+methodName;
		byte[] realData = Arrays.copyOf( reply.getData(), reply.getLength() );
		retString = new String(realData);
		
		/*ParameterizedType param1;
		ParameterizedType param2;*/
		/*Class cl = Class.forName(className);*/
		
		/*Constructor con = cl.getConstructor(Param1Type.class, Param2Type.class);*/
		/*Object xyz = con.newInstance(param1, param2);*/
		
		
		/*t.myMathod();*/
		input.close();
		
		
		myRMI(methodName);
	}

	private static void myRMI(String methodName) {
		/*DatagramSocket aSocket = null;*/
		try {
			/*aSocket = new DatagramSocket();*/
			
			/*byte[] methoName = s.getBytes();*/
			/*byte [] m = new byte [] {'a', 'b'};*/
			byte[] ip = new byte[]{  127, 0,0,1};
			InetAddress aHost = InetAddress.getByAddress(ip);
			int serverPort = 6789;
			DatagramPacket request =
					new DatagramPacket(methodName.getBytes(), methodName.length(), aHost, serverPort);
			aSocket.send(request);
			byte[] buffer = new byte[1000];
			DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
			aSocket.receive(reply);
			System.out.println("Reply: " + new String(reply.getData()));
		} catch (SocketException e){System.out.println("Socket: " + e.getMessage());
		} catch (IOException e){System.out.println("IO: " + e.getMessage());
		} finally { if(aSocket != null) aSocket.close();}
	}
	
	
	
	
}