close all; clear; clc

%% Modelo del motor 222050
% Parametros del motor

LA= 0.2*10^(-3);          % Inductancia (Unidad : henrios H)
RA= 4.05;                   % Resistencia (Unidad : ohms)
KT= 17.2*10^(-3);           % Torque constant (Unidad : N-m/A)
KB= 1/((557)*(pi)/30);      % Speed constant (Unidad : V.s/rad)
J= 4.28*(10^(-7));          % Inercia del rotor (Unidad : Kg.m^2)
TN= 12.4*10^(-3);             % Torque nominal (Unidad : N-m)WN= (5850*(pi))/30;
WN= (6650*(pi))/30;         % Velocidad angular(rad/s) (Unidad : rad/s)
B= (0.01*TN)/WN;           % Friccion del sistema (Unidad : N-ms/rad)


%% Modelo de estados
AV = [-B/J    KT/J
      -KB/LA -RA/LA];

BV = [0; 1/LA];

CV = [1 0];

DV = 0;

%% Calcular K óptimo

% Matrices del Sistema con Integrador:
Ai = [ AV zeros(2,1); -CV 0 ];
Bi = [ BV; 0 ];
Ci = [ CV 0 ];
Di = 0;
Wi = [ zeros(2,1); 1 ];

% Cálculo del Controlador.
Q = diag([10 1 20000])/1000;
R = 1;
Km = lqr(Ai,Bi,Q,R);

disp('Los K óptimos son:')
K = Km(1,1:2) %#ok
Ki = -Km(1,3) %#ok

ti = 0; dt = 0.00001; tf = 1;
% Condiciones Iniciales.
x = [0 0 0 ]'; 
u = 0; 
r = 500;
TORC=6*10^-3;

% Simulación:
k = 1;
for t = ti:dt:tf
    TI(k,1) = t;
    X1(k,1) = x(1,1);
    X2(k,1) = x(2,1);
    X3(k,1) = x(3,1);
    U(k,1) = u;
    xp = Ai*x + Bi*u + Wi*r +[-1/J ; 0; 0]*TORC;
    y = Ci*x + Di*u;
    % ley de control
    if (u>15)
        u=15;
    end 
    
    if (u<-15)
        u=-15;
    end
    u = -K*x(1:2,1) + Ki*x(3,1);
    Y(k,1) = y;
    x = x + xp*dt;
    k = k + 1;
end

subplot(2,2,1)
plot(TI,X1,'b')
title('Estado X1: velocidad Controlada con integrador'); grid on;
xlabel('tiempo (s)')
ylabel('Velocidad (rad/s)')

subplot(2,2,2)
plot(TI,X2,'b')
title('Estado X2: corriente Controlada con integrador'); grid on;
xlabel('tiempo (s)')
ylabel('Amperios (A)')

subplot(2,2,3)
plot(TI,U,'b')
title('Ley de control');grid on;
xlabel('tiempo (s)')
ylabel('Voltaje (V)')

subplot(2,2,4)
plot(TI,Y,'b')
title('Salida: velocidad');grid on; 
xlabel('tiempo (s)')
ylabel('rad/s')

hold on
plot(TI,r*ones(size(Y)),'k--')
hold off
legend('velocidad','set point')