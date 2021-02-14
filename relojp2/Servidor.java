import java.net.*;
import java.io.*;
import java.util.*;

public class Servidor implements Runnable{
	Interfaz s;
	InetAddress group;
	MulticastSocket socket;
	byte[] salida;
	int tamano=3000;
	Thread h;
	String mensaje;
	DatagramPacket dgp;

	public Servidor(){
		s=new Interfaz();
		salida=new byte[tamano];
		h=new Thread(this);
		h.start();
		System.out.println(""+s.aux2);
		try{
			group=InetAddress.getByName("224.1.1.1");
			socket=new MulticastSocket();
		}catch(Exception e){

		}
	}

	public void run(){
		while(true){
			System.out.println(""+mensaje);
			if(s.aux2){
				mensaje=s.horas+":"+s.minutos+":"+s.segundos+":";
				System.out.println(""+mensaje);
				salida=mensaje.getBytes();
				s.aux2=false;
				System.out.println("------------->"+salida.length);
				try{
					System.out.println("------------->Try");
					dgp=new DatagramPacket(salida,salida.length,group,5007);
					socket.send(dgp);
					System.out.println("------------->Enviado");
					System.out.println("------------->");
				}catch(Exception e){

				}
			}
		}
	}	
}