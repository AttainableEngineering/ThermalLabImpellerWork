% Group 4:
clc;clear;close;

%% System curve
Ho = 35; % [m]
beta2_double = -1600;  % [s^2/m^5]
beta1_double = 15;     % [s/m^2]
syms Q
h = Ho + beta1_double*Q + beta2_double*Q^2;
% Differentiate and substitute
dh = diff(h, Q);
dh = subs(dh, Q, 0.08);

%% Blade dimensions and operation
omega = 2*pi*2500/60;   % [rad/s]  -  angular velocity
g = 9.81;               % [m/s^2]  -  gravity
n = 10;                 % blades
t = 3/16*25.4*10^(-3);  % [m] thickness

b1 = 40.65*10^(-3);     % [m]  -  impeller thickness at inner diameter 
b2 = 23.336*10^(-3);    % [m]  -  impeller thickness at outer diameter
r1 = 83*10^(-3);        % [m]  -  impeller inner radius
r2 = 118.428*10^(-3);   % [m]  -  impeller outer radius
D1 = 2*r1;              % [m]  -  impeller inner diameter
D2 = 2*r2;              % [m]  -  impeller outer diameter

%% Calculate Blade Angles
syms beta_1
Q = 0.08;   % [m^3/s]
eqn_beta1 = tan(beta_1) == Q/(r1*omega*(pi*b1*D1 - n*b1*(t/sin(beta_1))));
beta1_soln = solve(eqn_beta1, beta_1);  % [rad]
beta1_double = double(abs(beta1_soln)); % [rad]
beta1_deg = beta1_double*180/pi;        % [deg]

fprintf("Absolute value of calculated Beta 1:\n%f\t%f\n\n",beta1_deg(1),beta1_deg(2));
fprintf("Beta 1 is %f\n\n", min(beta1_deg));
fprintf("180 degrees - max(Beta 1) = %f\n", 180-max(beta1_deg))

fprintf("\n\n\n");

syms beta_2
eqn_beta2 = dh == - (omega*r2)/(g*b2*(pi*D2 - n*(t/sin(beta_2)))*tan(beta_2));
beta2_soln = solve(eqn_beta2, beta_2);  % [rad]
beta2_double = double(abs(beta2_soln)); % [rad]
beta2_deg = beta2_double*180/pi;        % [deg]

fprintf("Absolute value of calculated Beta 2:\n%f\t%f\n\n",beta2_deg(1),beta2_deg(2));
fprintf("Beta 2 is %f\n\n", min(beta2_deg));
fprintf("180 degrees - max(Beta 2) = %f\n", 180-max(beta2_deg))
