import java.awt.*;
import java.util.*;
import java.net.*;
import java.io.*;
import javax.swing.*;
import java.awt.*;
import java.util.*;


public class Tiempo extends JFrame implements Runnable{
	Thread h1;
	JLabel reloj;
	int horas,minutos,segundos;
	int pausa;
	public Tiempo(int h, int m,int s){
		setLayout(null);
		setSize(100,100);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		reloj=new JLabel("");
		reloj.setBounds(10,10,100,70);
		add(reloj);
		h1=new Thread(this);
		horas=h;
		minutos=m;
		segundos=s;
		pausa=1000;
		h1.start();
	}
	public void run(){
		while(true){
			try{
				segundos++;
				h1.sleep(pausa);
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