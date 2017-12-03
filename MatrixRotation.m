% --------------------------------------------------------------
% Author:		Senthil Palanivelu              
% Written:		11/20/2017                             
% Last Updated: 	12/03/2017
% Purpose:  		To calcuate Dihedral angle and Matrix Rotation
% --------------------------------------------------------------

Input_file = ('C:\Users\toshiba\Desktop\612 - Nurit\Hw4\coordinates.txt');
cartesian_coordinates = textread(Input_file, '%f');
N = length(cartesian_coordinates)/3; % No of rows of coordinates
backbone_chain = zeros(N,3);
backbone_chain(:,4) = 1;

% copy co-ordinates from array to matriz
for i = 1 : N
for j = 1 : 3
backbone_chain(i, j) = cartesian_coordinates((i - 1) * 3 + j);
end
end

% ----------------------- Phi Angle ------------------------%
% Normal vector to A-B-C
u = backbone_chain(2,:) - backbone_chain(1,:); % U = B - A
v = backbone_chain(3,:) - backbone_chain(2,:); % V = C - B
u = u(:,1:end-1);
v = v(:,1:end-1);
n_1 = cross_product(u,v);
% Normal vector to B-C-D
x = backbone_chain(3,:) - backbone_chain(2,:); % X = C - B
y = backbone_chain(4,:) - backbone_chain(3,:); % Y = D - C
x = x(:,1:end-1);
y = y(:,1:end-1);
n_2 = cross_product(x,y);
Phi_angle = find_angle(n_1, n_2);
%------------------------------------------------------------%

% ----------------------- Psi Angle -------------------------%
% Normal vector to B-C-D
u1 = backbone_chain(3,:) - backbone_chain(2,:); % U1 = C - B
v1 = backbone_chain(4,:) - backbone_chain(3,:); % V1 = D - C
u1 = u1(:,1:end-1);
v1 = v1(:,1:end-1);
n_3 = cross_product(u1,v1);
% Normal vector to C-D-E
x1 = backbone_chain(4,:) - backbone_chain(3,:); % X1 = D - C
y1 = backbone_chain(5,:) - backbone_chain(4,:); % Y1 = E - D
x1 = x1(:,1:end-1);
y1 = y1(:,1:end-1);
n_4 = cross_product(x1,y1);
Psi_angle = find_angle(n_3, n_4);
%------------------------------------------------------------%

% Sign of the Dihedral angle
sign_1 = dot(n_1, y);
sign_2 = dot(n_3, y1);

if sign_1 < 0
    degree = Phi_angle*-1;
    disp(degree);
else
    disp(Phi_angle);
end

if sign_2 < 0
    degree = Psi_angle*-1;
    disp(degree);
else
    disp(Psi_angle);
end

% ---------------------Rotations Operation--------------------------%
Input_file = ('C:\Users\toshiba\Desktop\612 - Nurit\Hw4\rotate.txt');
glu_coordinates = textread(Input_file, '%f');
N1 = length(glu_coordinates)/3; % No of rows of coordinates
glu_chain = zeros(N1,3);
glu_chain(:,4) = 1;

for i = 1 : N1
for j = 1 : 3
glu_chain(i, j) = glu_coordinates((i - 1) * 3 + j);
end
end

% Drag the Amino acid to the Origin
glu_chain    = glu_chain(:,1:end-1);
origin       = glu_chain(1,:);
glu_chain    = glu_chain - origin;
[yaw, pitch] = get_eulers_angle(glu_chain);

% Rotate 30 degree and apply matrix tranformation
rotate_by_degree(yaw, pitch, 30);
for k = 1 : N1;
atom_x = glu_chain(k,:);
atom_x = transpose(atom_x);
Rotation_M*atom_x+transpose(origin);
end

% Rotate 20 degree and apply matrix tranformation
rotate_by_degree(yaw, pitch, 20);
for k = 1 : N1;
atom_x = glu_chain(k,:);
atom_x = transpose(atom_x);
Rotation_M*atom_x+transpose(origin);
end

% Function to find the angle between the two vector
function [ ThetaInDegrees ] = find_angle(n_1, n_2)
a  = sqrt(sum(n_1.*n_1));
b  = sqrt(sum(n_2.*n_2));
n_1 = n_1/a;
n_2 = n_2/b;
CosTheta = dot(n_1, n_2);
ThetaInDegrees = acosd(CosTheta);
end

% Function to get the cross product of two vectors
function [ result ] = cross_product(x,y)
mag_1  = sqrt(sum(x.*x));
mag_2  = sqrt(sum(y.*y));
x = x/mag_1;
y = y/mag_2;
result = cross(x,y);
end

% Z-Y-X-Y-Z
function [ Rotation_M ]  = rotate_by_degree(yaw, pitch, x)
un_swing    = [cos(-yaw) -sin(-yaw) 0 ; sin(-yaw) cos(-yaw) 0 ; 0 0 1] ;
un_lean     = [cos(-pitch) 0 sin(-pitch) ; 0 1 0 ; -sin(-pitch) 0  cos(-pitch)] ;
twist       = [1 0 0; 0 cos(x) -sin(x) ; 0 sin(x) cos(x)] ;
lean        = [cos(pitch) 0 sin(pitch) ; 0 1 0 ; -sin(pitch) 0  cos(pitch)] ;
swing       = [cos(yaw) -sin(yaw) 0 ; sin(yaw) cos(yaw) 0 ; 0 0 1] ;
Rotation_M  = swing*lean*twist*un_lean*un_swing;
end

% Function to get the Eulers angle
function [ yaw, pitch ] = get_eulers_angle(Matrix)
C          = Matrix(2,:) - Matrix(1,:);
mag_c      = sqrt(sum(C.*C));
C          = C/mag_c;
Psi        = C(:,2)/C(:,1);
adj        = sqrt((C(:,2)*C(:,2))+(C(:,1)*C(:,1)));
Phi        = C(:,3)/adj;
yaw        = atand(Psi); % Theta Beta lean
pitch      = atand(Phi); % Phi Gamma Swing
end
