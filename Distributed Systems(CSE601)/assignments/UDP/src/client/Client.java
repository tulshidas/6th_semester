package client;
import java.net.*;
import java.util.Scanner;
import java.io.*;
public class Client{
	
	static DatagramSocket aSocket = null;
	
	public static void main(String args[]) throws IOException{
		Scanner input = new Scanner(System.in);
		System.out.print("Enter Ip(p.q.r.s):");
		String ips = input.nextLine();
		System.out.println("ips:"+ips);
		System.out.print("Enter port:");
		
		int port = input.nextInt();
		System.out.println("port:"+port);
		String []ipss = ips.split("\\.");
		System.out.println("size:"+ipss.length);
		input.close();
		byte[] ipBt = new byte[4];
		for(int i=0;i<ipss.length;i++){
			System.out.println("ip"+ipss[i]);
			ipBt[i] = Integer.valueOf(ipss[i]).byteValue();
		}
		
		MyRMI myRmi = new MyRMI();
		myRmi.invoke(ipBt,port);
		
	}

	
	
}