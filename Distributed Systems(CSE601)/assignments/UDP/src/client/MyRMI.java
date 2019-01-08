package client;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.Scanner;

public class MyRMI {

	
	private DatagramSocket socket;
	private byte[] ip;
	private int port;
	private InetAddress host;
	
	public MyRMI() throws SocketException {
		 socket = new DatagramSocket();
	}
	public String invoke(byte[] ipBt, int port) throws IOException{
		ip = ipBt;
		this.port = port;
		host = InetAddress.getByAddress(ip);
		System.out.println("port1s:"+this.port);
		String reply =send("");
		System.out.println(reply);

		System.out.print("Enter name of class:");
		Scanner input = new Scanner(System.in);
		String className = input .nextLine();
		System.out.print("Enter name of method:");
		String methodName = input.nextLine();
		String message = className+" "+methodName;
		reply =send( message);
		System.out.println(reply);
		input.close();
		return reply;
	}
	
	private String send(String message) throws IOException {
		DatagramPacket request = new DatagramPacket(message.getBytes(), message.length(), host, port);
		socket.send(request);
		byte[] buffer= new byte[1000];
		DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
		socket.receive(reply);
		return new String(reply.getData())+reply.getLength();
	}
}
