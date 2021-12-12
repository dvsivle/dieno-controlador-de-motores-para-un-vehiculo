"""
Proyecto: Panel de control de velociadad de motores Tf 
@Autor: EDVS
"""

#%%
# import libraries 
import sys
from time import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import  QtSerialPort

import time

# Author of the library: Stefan Holstein 
# inspired by: https://github.com/Werkov/PyQt4/blob/master/examples/widgets/analogclock.py
from analoggaugewidget import AnalogGaugeWidget

class Main_App(QMainWindow):

    def __init__(self,parent=None,*args):
        super(Main_App,self).__init__(parent=parent)

        self.ancho = 450 
        self.altura = 800
        self.run = True

        # --- VARIABLES PARA LA LECTURA DE DE LOS SENSORES--------
        self.velocidad_M1 = 0
        self.velocidad_M2 = 0
        self.corriente_M1 = 0
        self.corriente_M2 = 0

        self.setFixedSize(self.ancho,self.altura)
        self.setWindowTitle("panel de control")
        self.General = QLabel(self)
        self.General.setGeometry(0,0,self.ancho,self.altura)
        self.General.setStyleSheet("border-radius: 3px; border: none; background-color: #000000;")


        self.box_Panel = QLabel(self.General)
        self.tv_tituloPANEL = QLabel("PANEL DE CONTROL",self.box_Panel)
        
        self.compotenes = QWidget(self.box_Panel)
        self.name_dispsitivo = QLabel('Dispositivos:',self.compotenes)
        
        
        self.list_Puertos = QComboBox(self)
    
        #----------Box panel---------#
        self.box_Panel.setGeometry(QRect(10, 10,self.ancho-20, self.altura-20))
        self.box_Panel.setStyleSheet(" border-radius: 15px; background-color: #101010;")
        
        #----------Box panel de control---------#
        
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.tv_tituloPANEL.setFont(font)
        self.tv_tituloPANEL.setStyleSheet("border: none; color: #C2185B;")
        self.tv_tituloPANEL.setGeometry(100, 10, 250, 40)

        ## --- COMPONENTES ---------------
        self.compotenes.setGeometry(5,50,420,46)
        self.compotenes.setStyleSheet(" border-radius: 5px; border:1px solid #607D8B;")

        #-------dispositivos-----
        font = QFont()
        font.setPointSize(11)
        self.name_dispsitivo.setFont(font)
        self.name_dispsitivo.setStyleSheet(" border-radius: 15px; border: none;color:#1565C0")
        self.name_dispsitivo.setGeometry(10,3,120,40)

        #---------Lista de puertos--------------#
        font.setPointSize(10)
        self.list_Puertos.setFont(font)
        self.list_Puertos.setGeometry(135, 65, 150, 35)
        ports = ["COM1", "COM2", "COM3", "COM4", "COM5"]
  
        self.list_Puertos.addItems(ports)
       
        self.list_Puertos.setStyleSheet("QListView {background-color: #B3E5FC;}")
        self.list_Puertos.setStyleSheet("border-radius: 2px; border:1px solid #1565C0;color:#4CAF50; background-color: transparest;")
        

        
        # -----  button list ports-------------
        font.setPointSize(11)

        self.button = QPushButton(self.compotenes)
        self.button.setFont(font)
        self.button.setMouseTracking(True)
        self.button.setText("Conectar")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setAutoDefault(False)
        self.button.setGeometry(300, 6, 100, 34)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.Mensaje)
        self.button.setStyleSheet("background-color: rgb(251, 192, 45); border-radius: 5px; border: 1px solid rgb(100,100,100);")

        

        # ----------- PROGRES BARR--------------#
        
        self.C_bar = QWidget(self.box_Panel)
        self.C_bar.setGeometry(20, 100,390,300)
        self.C_bar.setStyleSheet(" border-radius: 10px; background-color: black; border:none;")

        self.frame_1 = QFrame(self.C_bar)
        self.frame_1.setGeometry(10, 10,160,160)
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.sensor_M1= AnalogGaugeWidget(self.frame_1)
        self.sensor_M1.setMinimumSize(QSize(150, 150))
        
        
        self.frame_2 = QFrame(self.C_bar)
        self.frame_2.setGeometry(220, 10,160,160)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        

        self.frame_2.setFrameShadow(QFrame.Raised)
        self.sensor_M2= AnalogGaugeWidget(self.frame_2)
        self.sensor_M2.setMinimumSize(150, 150)
        self.sensor_M2.value_min = -60
        self.sensor_M2.value_max = 60
        self.sensor_M2.units = "deg"

        # ---Label----------
        self.LedDirecion = QLabel(self.C_bar)
        self.LedDirecion.setGeometry(175, 20,30,30)
        self.LedDirecion.setStyleSheet(" border-radius: 15px; background-color: black; border: 1px solid #CFD8DC;")
        
        # +++++++++++++++++++++++Label para la lectura del sensor de corriente++++++++++++++++++++++++
        self.img_LogoCarrito = QLabel(self.C_bar)
        self.img_LogoUPC = QLabel(self.C_bar)
        #----------------LOGO UPC---------#
        self.img_LogoCarrito.setGeometry(10,180, 120, 100)
        self.img_LogoCarrito.setPixmap(QPixmap("imagenes/carrito.png"))
        self.img_LogoCarrito.setStyleSheet("background-color: black ;border:none;")
        
        self.img_LogoCarrito.setScaledContents(True)

        #----------LOGO AESS---------#
        self.img_LogoUPC.setGeometry(250, 180, 100, 100)
        self.img_LogoUPC.setPixmap(QPixmap("imagenes/LOGO_UPC.png"))
        self.img_LogoUPC.setStyleSheet("border:none;")
        
        self.img_LogoUPC.setScaledContents(True)


        # ----DEFINIR SET POINT DEL MOTOR 1 (motor derecho)-------
        """self.corr_M1 = QWidget(self.C_bar)
        self.corr_M1.setGeometry(110,200,165,50)
        self.corr_M1.setStyleSheet(" border-radius: 10px; border: 1px solid #FFEE58;")

        self.L_corrD = QLabel("Corriente MI: (mA):",self.corr_M1)
        self.L_corrD.setGeometry(5,2,150,20)
        self.L_corrD.setAlignment(Qt.AlignCenter)
        self.L_corrD.setStyleSheet("border: none; color: #F5F5F5")

        self.mA_M1 = QLabel(str(self.corriente_M1),self.corr_M1)
        self.mA_M1.setGeometry(5,24,150,20)
        self.mA_M1.setAlignment(Qt.AlignCenter)
        self.mA_M1.setStyleSheet("border: none; color: #4CAF50")
        font.setPointSize(10)
        self.mA_M1.setFont(font)"""


        # -----------BOTONES PARA CONTROLAR LA DIRECION Y VELOCIDAD-----
        
        self.botones = QWidget(self.box_Panel)
        self.botones.setGeometry(20, 410,390,350)
        self.botones.setStyleSheet(" border-radius: 10px; border: none; background-color: black")

        # ----DEFINIR SET POINT DEL MOTOR 1 (motor derecho)-------
        self.SP_M1 = 0
        self.SP_M2 = 0

        self.motor1 = QWidget(self.botones)
        self.motor1.setGeometry(10,10,120,50)
        self.motor1.setStyleSheet(" border-radius: 10px; border: 1px solid #E91E63;")

        self.L_motorD = QLabel("MOTOR VEL (rpm):",self.motor1)
        self.L_motorD.setGeometry(5,2,110,20)
        self.L_motorD.setStyleSheet("border: none; color: #F5F5F5")

        self.RMP_M1 = QLabel(str(self.SP_M1),self.motor1)
        self.RMP_M1.setGeometry(10,24,100,20)
        self.RMP_M1.setAlignment(Qt.AlignCenter)
        self.RMP_M1.setStyleSheet("border: none; color: #4CAF50")
        font.setPointSize(10)
        self.RMP_M1.setFont(font)

        
        # ----DEFINIR SET POINT DEL MOTOR 2 (motor izquierdo)-------
        self.motor2 = QWidget(self.botones)
        self.motor2.setGeometry(260,10,120,50)
        self.motor2.setStyleSheet(" border-radius: 10px; border: 1px solid #E91E63;")

        self.L_motorI = QLabel("MOTOR POS (deg):",self.motor2)
        self.L_motorI.setGeometry(5,2,110,20)
        self.L_motorI.setStyleSheet("border: none; color: #F5F5F5")

        self.RMP_M2 = QLabel(str(self.SP_M2),self.motor2)
        self.RMP_M2.setGeometry(10,24,100,20)
        self.RMP_M2.setAlignment(Qt.AlignCenter)
        self.RMP_M2.setStyleSheet("border: none; color: #4CAF50")
        font.setPointSize(10)
        self.RMP_M2.setFont(font)

        # *************** BOTONES ********************
        h_1 = 80
        w_1 = 80
        cx = 160
        cy = 160

        # --------------- BOTON PARA AVANZAR ADELANTE-------------
        self.b_upper = QPushButton(self.botones)
        self.b_upper.setGeometry(cx, cy-h_1, w_1, h_1)
        self.b_upper.setMouseTracking(True)
        self.b_upper.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowUp")))
        self.b_upper.setIconSize(QSize(h_1,w_1))
        self.b_upper.setCursor(Qt.PointingHandCursor)
        self.b_upper.setAutoDefault(False)
        
        #self.b_upper.clicked.connect(self.Mup)
        self.b_upper.pressed.connect(self.Mup)
        self.b_upper.released.connect(self.stopCount)
        self.b_upper.setStyleSheet("border-radius: 30px;")
        self.b_upper.setCheckable(True)

        # --------------- BOTON BOTON PARA RETROCEDER-------------        
        self.b_Back = QPushButton(self.botones)
        self.b_Back.setGeometry(cx, cy+h_1, w_1, h_1)
        self.b_Back.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowDown")))
        self.b_Back.setMouseTracking(True)
        self.b_Back.setIconSize(QSize(h_1,w_1))
        self.b_Back.setCursor(Qt.PointingHandCursor)
        self.b_Back.setAutoDefault(False)

        #self.b_Back.clicked.connect(self.MDown)
        self.b_Back.pressed.connect(self.MDown)
        self.b_Back.released.connect(self.stopCount)
        self.b_Back.setStyleSheet("border-radius: 30px;")

         # --------------- BOTON PARA GIRAR A LA IZQUIERDA-------------    
        self.b_left = QPushButton(self.botones)
        self.b_left.setGeometry(cx+w_1+10, cy, w_1, h_1)
        self.b_left.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowRight")))
        self.b_left.setMouseTracking(True)
        self.b_left.setIconSize(QSize(h_1,w_1))
        self.b_left.setCursor(Qt.PointingHandCursor)
        self.b_left.setAutoDefault(False)

        #self.b_left.clicked.connect(self.MLeft)
        self.b_left.pressed.connect(self.MLeft)
        self.b_left.released.connect(self.stopCount)
        self.b_left.setStyleSheet("border-radius: 30px;")

        # --------------- BOTON PARA GIRAR A LA DERECHA------------- 

        self.b_right = QPushButton(self.botones)
        self.b_right.setGeometry(cx-w_1-10, cy, w_1, h_1)
        self.b_right.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowLeft")))
        self.b_right.setMouseTracking(True)
        self.b_right.setIconSize(QSize(h_1,w_1))
        self.b_right.setCursor(Qt.PointingHandCursor)
        self.b_right.setAutoDefault(False)

        #self.b_right.clicked.connect(self.Mright)
        self.b_right.pressed.connect(self.Mright)
        self.b_right.released.connect(self.stopCount)
        self.b_right.setStyleSheet("border-radius: 30px;")


                
        #-------Interrupcion cada 50ms para actualizar el set point
        self.direction =''
        self.timer1 = QTimer()
        self.timer1.setInterval(50)
        self.timer1.timeout.connect(self.contador)
        self.timer1.stop() #Inicai imagen statica

  # ======================= FUNCIONES ============================
    
    def contador(self):
        if self.direction== 'UP':

            self.SP_M1 = self.SP_M1+1
            
            if self.SP_M1>=821:
                self.SP_M1 =821
                        
                       
            
        elif self.direction== 'DW':
                      
            self.SP_M1 = self.SP_M1-1
            
            if self.SP_M2<=-821:
                self.SP_M1=-821
                      
        elif self.direction== 'LF':
            self.SP_M2 = self.SP_M2 +1
            if self.SP_M2>=45 :
                self.SP_M2=45
                
            
        elif self.direction== 'RT':
            self.SP_M2 = self.SP_M2-1

            if self.SP_M2<=-45 :
                self.SP_M2=-45
                       
        self.RMP_M1.setText(str(self.SP_M1))
        self.RMP_M2.setText(str(self.SP_M2))
        #texto1 = 'SP:' + str(self.SP_M1) + ';'+ str(self.SP_M2)
        #self.serial.write(texto1.encode())

    def stopCount(self):
        self.timer1.stop()
        self.Write_SetPoint()
           
    def Mup(self):
        self.direction = 'UP' #adelante
        self.timer1.start()

    def MDown(self):
        self.direction = 'DW' #retroceso
        self.timer1.start()

    def MLeft(self):
        self.direction = 'LF' #Giro a la izquierda
        self.timer1.start()
        
    def Mright(self):
        self.direction = 'RT' ##Giro a la derecha
        self.timer1.start()
        

    def Mensaje(self,checked):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle("Mensaje")
        mensaje.setStyleSheet("background-color: rgb(38, 198, 218);color: balck")
        font = QFont()
        font.setPointSize(10)
        mensaje.setFont(font)

        #baud_rate = 9600
        Port = self.list_Puertos.currentText()
        self.serial = QtSerialPort.QSerialPort(Port,baudRate=9600,readyRead=self.ReadValuesSensor)
        self.button.setText("Desconectar" if checked else "Conectar")
        if checked:
            if not self.serial.isOpen():
                if not self.serial.open(QIODevice.ReadWrite):
                    self.btn_Conectar.setChecked(False)
                    #self.timer.start()
                    

                    
        else:
            self.serial.close()
            #self.timer.stop()
        self.contador()
        
        mensaje.setText("La conexion fue realizada con éxito ")
        mensaje.move(self.pos().x()+50, self.pos().y()+150)
        mensaje.exec()

    
    def Write_SetPoint(self):
        
        texto1 = 'SP:' + str(int(self.SP_M1*(255/821))) + ';'+ str(int((255/2)*(int(self.SP_M2)/60+1)))
        self.serial.write(texto1.encode())
        # print(texto)
        # SP:-NN;-MN
        # (255/2)(int(self.SP_M2)/60+1)
        print(texto1)

    def ReadValuesSensor(self):

        while self.serial.canReadLine():
            cad = self.serial.readLine().data().decode().strip()
            print(cad)
            if ":" in cad:
                #print(cad)
                pos=cad.index(":")
                label=cad[:pos]
                value=cad[pos+1:]
                if label == 'velo1':
                    self.velocidad_M1 = int(value)
                if label == 'velo2':
                    self.velocidad_M2 = int(value)
                    
                if label == 'corr1':
                    self.corriente_M1 = int(value)
                if label == 'corr2':
                    self.corriente_M2 = int(value)

                self.update_data()

    def update_data (self):
        self.sensor_M1.update_value(abs(int(self.velocidad_M1*(821/1023))))
        self.sensor_M2.update_value(int(int(self.velocidad_M2)*(120/1024)-60))
        #(255/2)(int(self.SP_M2)/60+1)
        self.mA_M1.setText(str(round(self.corriente_M1*(5000000/(1023*752)),2)))

        if (self.SP_M1<0):
            self.LedDirecion.setStyleSheet("background-color: red")
        else:
            self.LedDirecion.setStyleSheet("background-color: green")
        


def main():
    app = QApplication(sys.argv)
    ex = Main_App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


#%%