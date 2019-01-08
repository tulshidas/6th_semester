package server;

import java.net.*;
import java.util.Arrays;
import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class UDPServer {
	public static void main(String args[]) throws NoSuchMethodException, SecurityException, IllegalAccessException,
			IllegalArgumentException, InvocationTargetException, InstantiationException {
		DatagramSocket aSocket = null;
		try {
			aSocket = new DatagramSocket(6789);
			byte[] buffer = new byte[1000];
			while (true) {
				DatagramPacket request = new DatagramPacket(buffer, buffer.length);
				aSocket.receive(request);
				byte[] realData = Arrays.copyOf(request.getData(), request.getLength());
				MyClass cClass = new MyClass();
				
				String methodName = new String(realData);
				String retValue;
				if (methodName.length() != 0) {
					System.out.println(methodName);
					String className = methodName.split(" ")[0];
					methodName = methodName.split(" ")[1];
					Class<?> xyz;
					try {
						xyz = Class.forName(className);
						Method m = xyz.getDeclaredMethod(methodName);
						retValue = (String) m.invoke(xyz.newInstance());

						System.out.println("method:" + methodName + methodName.length());
						
						DatagramPacket reply = new DatagramPacket(retValue.getBytes(), retValue.length(),
								request.getAddress(), request.getPort());

						aSocket.send(reply);
					} catch (ClassNotFoundException e) {
						

						retValue = "Class not found";

						
						System.out.println("method:" + methodName + methodName.length());
						
						DatagramPacket reply = new DatagramPacket(retValue.getBytes(), retValue.length(),
								request.getAddress(), request.getPort());

						aSocket.send(reply);

					}

				}

				else {

					retValue = "Available invokable classes and methods:\nserver.MyClass\n\tremoteMethod\n\t"
							+ "remoteMethod1\n\tremoteMethod2\nserver.MyClass2\n\tremoteMethod\n\tremoteMethod1"
							+ "\n\tremoteMethod2\nserver.MyClass3\n\tremoteMethod\n\tremoteMethod1\n\tremoteMethod2";

				
					DatagramPacket reply = new DatagramPacket(retValue.getBytes(), retValue.length(),
							request.getAddress(), request.getPort());

					aSocket.send(reply);

				}
			}
		} catch (SocketException e) {
			System.out.println("Socket: " + e.getMessage());
		} catch (IOException e) {
			System.out.println("IO: " + e.getMessage());
		} finally {
			if (aSocket != null)
				aSocket.close();
		}
	}

}