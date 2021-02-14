import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;


public class Interfaz extends JFrame implements ActionListener,Runnable{
	private JButton bAumentarHora;
	private JButton bDisminuirHora;
	private JButton bAumentarMinutos;
	private JButton bDisminuirMinutos;
	private JButton bAumentarSegundos;
	private JButton bDisminuirSegundos;
	private JButton bAcelerar;
	private JButton bDisminuir;
	private JButton bPausar;
	private JButton bSend;
	private Boolean aux;
	public Boolean aux2;
	public JLabel reloj;
	public Thread h;
	public int horas,minutos,segundos,pausa;


	public Interfaz(){
		aux=true;
		aux2=false;
		horas=0;
		minutos=0;
		segundos=0;
		pausa=1000;
		h=new Thread(this);
		h.start();
		setLayout(null);
		setSize(370,280);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		reloj=new JLabel(String.format("%02d",horas)+":"+String.format("%02d",minutos)+":"+String.format("%02d",segundos));
		reloj.setBounds(120,10,100,70);
		add(reloj);

		bAumentarHora=new JButton("Aumentar hora");
		bAumentarHora.setBounds(10,80,150,20);
		add(bAumentarHora);
		bAumentarHora.addActionListener(this);


		bDisminuirHora=new JButton("Disminuir hora");
		bDisminuirHora.setBounds(170,80,150,20);
		add(bDisminuirHora);
		bDisminuirHora.addActionListener(this);


		bAumentarMinutos=new JButton("Aumentar minutos");
		bAumentarMinutos.setBounds(10,110,150,20);
		add(bAumentarMinutos);
		bAumentarMinutos.addActionListener(this);


		bDisminuirMinutos=new JButton("Disminuir minutos");
		bDisminuirMinutos.setBounds(170,110,150,20);
		add(bDisminuirMinutos);
		bDisminuirMinutos.addActionListener(this);


		bAumentarSegundos=new JButton("Aumentar segundo");
		bAumentarSegundos.setBounds(10,140,150,20);
		add(bAumentarSegundos);
		bAumentarSegundos.addActionListener(this);

		bDisminuirSegundos=new JButton("Disminuir segundos");
		bDisminuirSegundos.setBounds(170,140,150,20);
		add(bDisminuirSegundos);
		bDisminuirSegundos.addActionListener(this);

		bAcelerar=new JButton("Acelerar");
		bAcelerar.setBounds(10,170,150,20);
		add(bAcelerar);
		bAcelerar.addActionListener(this);

		bDisminuir=new JButton("Disminuir");
		bDisminuir.setBounds(170,170,150,20);
		add(bDisminuir);
		bDisminuir.addActionListener(this);

		bPausar=new JButton("Pausar/iniciar");
		bPausar.setBounds(10,200,150,20);
		add(bPausar);
		bPausar.addActionListener(this);

		bSend=new JButton("Enviar");	
		bSend.setBounds(170,200,150,20);
		add(bSend);
		bSend.addActionListener(this);
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

	public void actionPerformed(ActionEvent e){
		if(e.getSource()==bAumentarHora){
			horas++;
			if(horas==24){
				horas=0;
			}
		}
		if(e.getSource()==bDisminuirHora){
			horas--;
			if(horas==-1){
				horas=23;
			}
		}
		if(e.getSource()==bAumentarMinutos){
			minutos++;
			if(minutos==60){
				horas++;
				minutos=0;
				if(horas==24)
					horas=0;
			}

		}
		if(e.getSource()==bDisminuirMinutos){
			minutos--;
			if(minutos==-1)
			{
				horas--;
				minutos=59;
				if(horas==-1){
					horas=23;
				}
			}
		}
		if(e.getSource()==bAumentarSegundos){
			segundos++;
			if(segundos==60){
				minutos++;
				segundos=0;
				if(minutos==60){
					horas++;
					minutos=0;
					if(horas==24){
						horas=0;
					}
				}
			}
		}
		if(e.getSource()==bDisminuirSegundos){
			segundos--;
			if(segundos==-1){
				segundos=59;
				minutos--;
				if(minutos==-1){
					minutos=59;
					horas--;
					if(horas==-1)
						horas=23;
				}
			}
		}

		if(e.getSource()==bAcelerar){
			pausa=pausa/2;
		}
		if(e.getSource()==bDisminuir){
			pausa=pausa*2;
		}
		if(e.getSource()==bPausar){
			if(aux==true){
				aux=false;
				h.suspend();
			}else{
				aux=true;
				h.resume();
			}
		}
		if(e.getSource()==bSend){
			aux2=true;
		}
	}
}