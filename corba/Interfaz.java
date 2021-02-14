import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.lang.Math;


public class Interfaz extends JFrame implements Runnable{
	public JButton bAumentarHora;
	public JButton bDisminuirHora;
	public JButton bAumentarMinutos;
	public JButton bDisminuirMinutos;
	public JButton bAumentarSegundos;
	public JButton bDisminuirSegundos;
	public JButton bAcelerar;
	public JButton bDisminuir;
	public JButton bPausar;
	public JButton bSend;
	public JButton bFile;
	public Boolean aux;
	public Boolean aux2;
	public JLabel reloj;
	public Thread h;
	public int horas,minutos,segundos,pausa;


	public Interfaz(boolean esServidor){
		aux=true;
		aux2=false;
		double randomDouble = Math.random();
		randomDouble = randomDouble * 24;
		horas = (int) randomDouble;
		randomDouble = Math.random();
		randomDouble = randomDouble * 60;
		minutos = (int) randomDouble;
		randomDouble = Math.random();
		randomDouble = randomDouble * 60;
		segundos = (int) randomDouble;
		pausa=1000;
		h=new Thread(this);
		setLayout(null);
		setSize(370,320);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		reloj=new JLabel(String.format("%02d",horas)+":"+String.format("%02d",minutos)+":"+String.format("%02d",segundos));
		reloj.setFont(new Font("Serif", Font.BOLD, 32));
		reloj.setBounds(100,10,200,70);
		add(reloj);
		
		if(esServidor) {
			bAumentarHora=new JButton("Aumentar hora");
			bAumentarHora.setBounds(10,80,150,20);
			add(bAumentarHora);
	
	
			bDisminuirHora=new JButton("Disminuir hora");
			bDisminuirHora.setBounds(170,80,150,20);
			add(bDisminuirHora);
	
	
			bAumentarMinutos=new JButton("Aumentar minutos");
			bAumentarMinutos.setBounds(10,110,150,20);
			add(bAumentarMinutos);
	
	
			bDisminuirMinutos=new JButton("Disminuir minutos");
			bDisminuirMinutos.setBounds(170,110,150,20);
			add(bDisminuirMinutos);
	
	
			bAumentarSegundos=new JButton("Aumentar segundo");
			bAumentarSegundos.setBounds(10,140,150,20);
			add(bAumentarSegundos);
	
			bDisminuirSegundos=new JButton("Disminuir segundos");
			bDisminuirSegundos.setBounds(170,140,150,20);
			add(bDisminuirSegundos);
	
			bAcelerar=new JButton("Acelerar");
			bAcelerar.setBounds(10,170,150,20);
			add(bAcelerar);
	
			bDisminuir=new JButton("Disminuir");
			bDisminuir.setBounds(170,170,150,20);
			add(bDisminuir);
	
			bPausar=new JButton("Pausar/iniciar");
			bPausar.setBounds(10,200,150,20);
			add(bPausar);
	
			bSend=new JButton("Enviar");	
			bSend.setBounds(170,200,150,20);
			add(bSend);
		}
		if(!esServidor){
			bFile=new JButton("Archivo");	
			bFile.setBounds(100,230,150,20);
			add(bFile);
		}
		
		h.start();
	}

	public void run(){
		while(true){
			try{
				segundos++;
				h.sleep(pausa);
				if(segundos==60){
					segundos=0;
					minutos++;
				}if(minutos==60){
					minutos=0;
					horas++;
				}if(horas==24){
					segundos=0;
					minutos=0;
					horas=0;
				}
				reloj.setText(String.format("%02d",horas)+":"+String.format("%02d",minutos)+":"+String.format("%02d",segundos));
			}catch(Exception e){

			}
		}
	}
}