import java.net.*;
import java.io.*;
import java.util.*;
import java.awt.event.*;
import javax.swing.JButton;
import java.sql.*;

public class Servidor implements ActionListener{
	Interfaz s;
	InetAddress group;
	Thread h;
	Thread t;
	InetAddress gpo = null;
	JButton bAumentarHora;
	JButton bDisminuirHora;
	JButton bAumentarMinutos;
	JButton bDisminuirMinutos;
	JButton bAumentarSegundos;
	JButton bDisminuirSegundos;
	JButton bAcelerar;
	JButton bDisminuir;
	JButton bPausar;
	JButton bSend;
	int tam = 1024;
	List<String> clientes;
	String nombre="maestro";
	int port = 5007;

	public Servidor(){
		clientes = new ArrayList<String>();
		s=new Interfaz(true);
		JButton bAumentarHora = s.bAumentarHora;
		JButton bDisminuirHora = s.bDisminuirHora;
		JButton bAumentarMinutos = s.bAumentarMinutos;
		JButton bDisminuirMinutos = s.bDisminuirMinutos;
		JButton bAumentarSegundos = s.bAumentarSegundos;
		JButton bDisminuirSegundos = s.bDisminuirSegundos;
		JButton bAcelerar = s.bAcelerar;
		JButton bDisminuir = s.bDisminuir;
		JButton bPausar = s.bPausar;
		JButton bSend = s.bSend;
		
		bAumentarHora.addActionListener(this);
		bDisminuirHora.addActionListener(this);
		bAumentarMinutos.addActionListener(this);
		bDisminuirMinutos.addActionListener(this);
		bAumentarSegundos.addActionListener(this);
		bDisminuirSegundos.addActionListener(this);
		bAcelerar.addActionListener(this);
		bDisminuir.addActionListener(this);
		bPausar.addActionListener(this);
		bSend.addActionListener(this);
		h=new Thread(new ReadThread(port,gpo,s));
		h.start();
		t=new Thread(new ReadTCP());
		t.start();
	}

	class ReadThread implements Runnable {
		private int port;
		private InetAddress gpo;
		private static final int tam = 1024;
		private Interfaz s;

		public ReadThread(int port, InetAddress gpo, Interfaz s){
			this.port=port;
			this.gpo=gpo;
			this.s=s;
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
					DatagramPacket datagram = new DatagramPacket(buffer, buffer.length, group, port);
					socket.receive(datagram);
					String msj = new String(buffer, 0, datagram.getLength(), "UTF-8");
					System.out.println("Datagrama recibido: "+msj+"\n");
					System.out.println("Servidor descubierto: "+datagram.getAddress()+":"+datagram.getPort()+"\n");
					if(msj.startsWith("HOLA")) {
						clientes.add(datagram.getAddress()+"");
						String time = s.horas+":"+s.minutos+":"+s.segundos;
						byte[] by = time.getBytes();
						DatagramPacket q =new DatagramPacket(by,by.length,gpo,port);
						socket.send(q);
					}else {
						System.out.println(msj);
					}
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}

	class ReadTCP implements Runnable{
		public void run(){
			try {

				ServerSocket s = new ServerSocket (7000);
	
				for(;;){
	
					System.out.println("Esperando cliente...");
					Socket cl = s.accept();
					InetAddress ipdir = cl.getInetAddress();
					String stringip = ipdir.toString();
					String ipport =Integer.toString(cl.getPort()); 
					System.out.println("Conexion establecida desde: " + stringip + ":" + ipport);                
					DataInputStream dis = new DataInputStream(cl.getInputStream());

					int n = dis.readInt(); 
					byte[] b = new byte[1024];
					String[] nombre = new String [n];
					String thename = "";
					for( int i=0; i<n ; i++)
					{
						nombre[i]=dis.readUTF();
						System.out.println("Recibimos el archivo "+ (i+1)+": "+ nombre[i]);
						thename=nombre[i];
					}
					//System.out.println("Chinga tu madre servin: "+thename);
					long[] tam = new long [n];
					for( int i=0; i<n ; i++)
					{
						tam[i] = dis.readLong();
					}
	
					for(int i=0; i<n ; i++)
					{
						DataOutputStream dos = new DataOutputStream(new FileOutputStream(nombre[i]));
						long recibidos = 0;
						int m=0;
						int porcentaje=0;
						while (recibidos < tam[i]){
							int falt = (int)(tam[i]-recibidos);
							if (falt < 1024){
								m = dis.read(b,0,falt);
							}    
							else{
								m = dis.read(b);
							}
							dos.write(b,0,m);
							dos.flush();
							recibidos = recibidos + m;
							porcentaje = (int)(recibidos*100/tam[i]);
							System.out.print("Recibido: " + porcentaje + "%\r");
						}  
						System.out.println("\nArchivo "+(i+1)+" recibido\n");
						dos.close();  
					}
					dis.close();
					//cl.close();
					String filelinex="";
					File fileToRead = new File(thename);
					try( FileReader fileStream = new FileReader( fileToRead ); 
					    BufferedReader bufferedReader = new BufferedReader( fileStream ) ) {
					    String line = null;
					    while( (line = bufferedReader.readLine()) != null ) {
					        System.out.println("Numeros a sumar: "+line);
					        filelinex=line;
					    }

					    } catch ( FileNotFoundException e) {
					       e.printStackTrace();
					    } catch ( IOException e) {
					       e.printStackTrace();
						}
					String[] parts = filelinex.split(" ");
					int sum=sumanumbers(parts);
					System.out.println("Suma = "+Integer.toString(sum));
					    try
					    {
					      // create a mysql database connection
					      //String myDriver = " com.mysql.jdbc.Driver";
					      //String myUrl = "jdbc:mysql://localhost/datos";
					      //Class.forName(myDriver);
					      //Connection connx = DriverManager.getConnection(myUrl, "root", "");
					      Class.forName("com.mysql.jdbc.Driver");  
						Connection connx=DriverManager.getConnection(  
						"jdbc:mysql://localhost:3306/datos","root","");  
						//here sonoo is database name, root is username and password  
						Statement stmt=connx.createStatement();  
					      // the mysql insert statement
					      String query = " insert into info (ip, puerto, resultado)"
					        + " values (?, ?, ?)";

					      // create the mysql insert preparedstatement
					      PreparedStatement preparedStmt = connx.prepareStatement(query);
					      preparedStmt.setString (1, stringip);
					      preparedStmt.setString (2, ipport);
					      preparedStmt.setInt    (3, sum);

					      // execute the preparedstatement
					      preparedStmt.execute();
					      System.out.println("Resultados guardados en base de datos!!");
					      connx.close();
					    }
					    catch (Exception e)
					    {
					      System.err.println("Got an exception!");
					      e.printStackTrace();
					    }
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	public void enviar(String opcion) {
        try {
            MulticastSocket e = new MulticastSocket(port);
            e.setReuseAddress(true);
            e.setTimeToLive(1);
            gpo=InetAddress.getByName("224.1.1.1");
			e.joinGroup(gpo);
			String time="";
			if(opcion.trim().equals("hora"))
				time = s.horas+":"+s.minutos+":"+s.segundos;
			else if (opcion.trim().equals("pausa"))
				time = new String ("pausa");
			else if (opcion.trim().equals("reanuda"))
				time = new String ("reanuda");
			else if (opcion.trim().equals("acelera"))
				time = new String ("acelera");
			else
				time = new String ("alenta");	
			byte[] by = time.getBytes();
			DatagramPacket p =new DatagramPacket(by,by.length,gpo,port);
			e.send(p);
        } catch (Exception e) { 
            e.printStackTrace();
        }
	}
	
	public void actionPerformed(ActionEvent e){
		
		if(e.getSource()==s.bAumentarHora){
			s.horas++;
			if(s.horas==24){
				s.horas=0;
			}
		}
		if(e.getSource()==s.bDisminuirHora){
			s.horas--;
			if(s.horas==-1){
				s.horas=23;
			}
		}
		if(e.getSource()==s.bAumentarMinutos){
			s.minutos++;
			if(s.minutos==60){
				s.horas++;
				s.minutos=0;
				if(s.horas==24)
					s.horas=0;
			}

		}
		if(e.getSource()==s.bDisminuirMinutos){
			s.minutos--;
			if(s.minutos==-1)
			{
				s.horas--;
				s.minutos=59;
				if(s.horas==-1){
					s.horas=23;
				}
			}
		}
		if(e.getSource()==s.bAumentarSegundos){
			s.segundos++;
			if(s.segundos==60){
				s.minutos++;
				s.segundos=0;
				if(s.minutos==60){
					s.horas++;
					s.minutos=0;
					if(s.horas==24){
						s.horas=0;
					}
				}
			}
		}
		if(e.getSource()==s.bDisminuirSegundos){
			s.segundos--;
			if(s.segundos==-1){
				s.segundos=59;
				s.minutos--;
				if(s.minutos==-1){
					s.minutos=59;
					s.horas--;
					if(s.horas==-1)
						s.horas=23;
				}
			}
		}

		if(e.getSource()==s.bAcelerar){
			s.pausa=s.pausa/2;
			this.enviar("acelera");
		}
		if(e.getSource()==s.bDisminuir){
			s.pausa=s.pausa*2;
			this.enviar("alenta");
		}
		if(e.getSource()==s.bPausar){
			if(s.aux==true){
				s.aux=false;
				s.h.suspend();
				this.enviar("pausa");
			}else{
				s.aux=true;
				s.h.resume();
				this.enviar("reanuda");
			}
		}
		if(e.getSource()==s.bSend){
			this.enviar("hora");
		}
	}

	public int sumanumbers(String [] num){
		int[] numbers = new int[num.length];
		int total=0;
		for(int i = 0;i < num.length;i++)
		{
		   numbers[i] = Integer.parseInt(num[i]);
		   total=total+numbers[i];
		}
		return total;
	}

	public static void main(String [] args){
		Servidor s= new Servidor();
	}
}