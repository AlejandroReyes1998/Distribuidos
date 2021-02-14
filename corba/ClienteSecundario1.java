import java.net.*;
import java.io.*;
import javax.swing.*;
import java.awt.*;
import java.util.*;
import java.awt.event.*;
import javax.swing.JFileChooser;

public class ClienteSecundario1 extends JFrame implements Runnable,ActionListener{
	JLabel reloj;
	Thread h1;
	Interfaz s;
	InetAddress gpo;
	int tam=1025;
	String nombre="principal";
	int port = 5007;
	String host;
	
	public ClienteSecundario1(){
		s = new Interfaz(false);
		JButton bFile = s.bFile;
		bFile.addActionListener(this);
		h1=new Thread(this);
		h1.start();
		try {
			gpo=InetAddress.getByName("224.1.1.1");
			MulticastSocket socket =new MulticastSocket(port);
			socket.setReuseAddress(true);
            socket.setTimeToLive(1);
			String salida= new String("HOLA");
			byte[] by=salida.getBytes();
			DatagramPacket dgp=new DatagramPacket(by,by.length,gpo,port);
			socket.send(dgp);
		}catch(Exception e) {
			e.printStackTrace();
		}
	}

	public void run(){
        try {
            MulticastSocket socket = new MulticastSocket(port);
            socket.setTimeToLive(1);
            System.out.println("Servidor escuchando puerto "+socket.getLocalPort());
            socket.setReuseAddress(true);
            try {
                gpo = InetAddress.getByName("224.1.1.1");
            } catch (UnknownHostException u) {
                System.out.println("Direccion erronea");
            }
            socket.joinGroup(gpo);
            System.out.println("Unido al grupo");
            while(true){
				byte[] buffer = new byte[tam];
				DatagramPacket datagram = new DatagramPacket(buffer, buffer.length, gpo, port);
                socket.receive(datagram);
				String msj = new String(buffer, 0, datagram.getLength(), "UTF-8");
				if(!msj.startsWith("HOLA")){
					if(msj.startsWith("pausa")){
						s.h.suspend();
					}else if(msj.startsWith("reanuda")){
						s.h.resume();
					}else if(msj.startsWith("acelera")){
						s.pausa = s.pausa / 2;
					}else if(msj.startsWith("alenta")){
						s.pausa = s.pausa * 2;
					}else{
						String[] hora = msj.split(":");
						s.horas = (Integer.parseInt(hora[0])<23)?Integer.parseInt(hora[0])+1:0;
						if(Integer.parseInt(hora[1])>=30){
							s.minutos = Integer.parseInt(hora[1])-30;
							s.horas	= s.horas+1;
						}else{
							s.minutos = Integer.parseInt(hora[1])+30;
						}
						s.segundos = Integer.parseInt(hora[2]);
						System.out.println("Datagrama recibido: "+msj+"\n");
						System.out.println("Servidor descubierto: "+datagram.getAddress()+":"+datagram.getPort()+"\n");
					}
					host = datagram.getAddress()+"";
					System.out.println(host);
				}	
			}
        } catch (Exception e) {
            e.printStackTrace();
        }
	}

	public void enviarArchivo(){
		try {
			host = host.substring(1,host.length());
            System.out.println(host);
            Socket cl = new Socket (host,7000);
            JFileChooser jf = new JFileChooser();
            jf.setMultiSelectionEnabled(true);
            int r = jf.showOpenDialog(null);

            if (r == JFileChooser.APPROVE_OPTION){

                File[] f = jf.getSelectedFiles();
                int n = f.length;
                String[] archivo = new String[n];
                String[] nombre = new String[n];
                long[] tam = new long [n];
                for(int i=0 ; i<n ;i++)
                {
                    archivo[i]= f[i].getAbsolutePath();
                    nombre[i]= f[i].getName();
                    tam[i] = f[i].length();
                }

                DataOutputStream dos = new DataOutputStream(cl.getOutputStream());

                dos.writeInt(n);
                dos.flush();
                for(int i=0; i<n ; i++)
                {
                    dos.writeUTF(nombre[i]);
                    dos.flush();                    
                }
                for(int i=0; i<n ; i++){
                    dos.writeLong(tam[i]);
                    dos.flush();
                }    
                byte[] b = new byte[1024];

                for(int i=0; i<n ; i++)
                {
                    long enviado = 0;
                    int porcentaje,m;
                    DataInputStream dis = new DataInputStream(new FileInputStream(archivo[i]));
                    while (enviado < tam[i]) {                     
                        
                        m = dis.read(b);
                        dos.write(b,0,m);
                        dos.flush();
                        enviado = enviado + m;
                        porcentaje = (int)(enviado*100/tam[i]);
                        System.out.print("Enviado: " + porcentaje + "%\r");
                    }
                    System.out.println("\nArchivo "+ (i+1) +": enviado.\n");
                    dis.close();
                }
                
                dos.close();
                cl.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
	}

	public void actionPerformed(ActionEvent e){
		if(e.getSource()==s.bFile){
			this.enviarArchivo();
		}
	}

	public static void main(String []args){
		ClienteSecundario1 c=new ClienteSecundario1();
		
	}		
}