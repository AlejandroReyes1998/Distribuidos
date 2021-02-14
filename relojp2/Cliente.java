import java.net.*;
import java.io.*;
import javax.swing.*;
import java.awt.*;
import java.util.*;

public class Cliente extends JFrame implements Runnable{
	JLabel reloj;
	Thread h1;
	int horas=0,minutos=0,segundos=0;
	Tiempo h2;
	public Cliente(){
		h1=new Thread(this);
		h1.start();
	}

	public void run(){
		while(true){
			System.out.println("--------------------->");
			try{
				MulticastSocket cliente=new MulticastSocket(5007);
				System.out.println("--------------------->Puerto");
				InetAddress group=InetAddress.getByName("224.1.1.1");
				cliente.joinGroup(group);
				System.out.println("--------------------->Grupo");
				DatagramPacket hora=new DatagramPacket(new byte[3000],3000);
				cliente.receive(hora);
				System.out.println("--------------------->receive");
				String mensaje=new String(hora.getData());
				System.out.println(""+mensaje);
				String[] partes=mensaje.split(":");
				System.out.println("--------------------->"+partes[2]);
				horas=Integer.parseInt(partes[0]);
				System.out.println("--------------------->Parse"+horas);
				minutos=Integer.parseInt(partes[1]);
				System.out.println("--------------------->Parse2"+minutos);
				segundos=Integer.parseInt(partes[2]);
				System.out.println("--------------------->Parse3"+segundos);
				h2=new Tiempo(horas,minutos,segundos);
				System.out.println("--------------------->Hilo de conteo");
			}catch(Exception e){
			}
		}
	}

	public static void main(String []args){
		Cliente c=new Cliente();
		
	}		
}