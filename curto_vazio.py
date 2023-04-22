from math import sqrt
from statistics import mean

def calc_coef(tipo): # Tabela da norma NBR 5383-1:2002
    if tipo == 'rotor_bobinado': coef = 0.78
    elif tipo == 'D': coef = 0.78
    elif tipo == 'N': coef = 0.68
    elif tipo == 'H': coef = 0.58
    else: coef = 1

    return coef    

# Dados colhidos no ensaio CC e a vazio:
montagem = "delta"
f1 = 60
R_medido  = [13.6, 13.6, 13.6]
V_L = 220
I_linha = [1.6, 1.6, 1.75]
P_wattimetros = [280, 190]

# Dados colhidos no ensaio de rotor bloqueado:
f2 = 60
tipo_MIT = 'N' # rotor_bobinado, D, N ou H
V_L_RB = 55
I_linha_RB = [2.1, 2.1, 2.0]
P_wattimetros_RB = [120, 45]

# Calculos voltados para os ensaios CC e a vazio
iL_medio = mean(I_linha_RB)

if montagem == "delta":
    R1 = 3/2*(mean(R_medido))
    i_fase = iL_medio/sqrt(3)
    V_fi = V_L
elif montagem == "estrela":
    R1 = 1/2*(mean(R_medido))
    V_fi = V_L/sqrt(3)
    i_fase = iL_medio
else: print("Erro no fechamento do motor")

P_entrada = abs(P_wattimetros[0] - P_wattimetros[1])

P_CE = 3*R1*(i_fase**2)
P_rot = P_entrada - P_CE
fp_vz = P_entrada/(sqrt(3)*V_L*iL_medio)
soma_reat = sqrt((V_fi/i_fase)**2 - R1**2)

print(f"\nDADOS DO ENSAIO CC E VAZIO:")
print(f"Perdas no cobre Pce = {P_CE} [Watts]")
print(f"Potência de entrada = {P_entrada} [Watts]")
print(f"Perdas rotacionais = {P_rot} [Watts]")
print(f"Fator de potência a vazio = {fp_vz}")
print(f"Zeq = {R1} + j* {soma_reat} [ohms]")
print(f"Soma da reatância = {soma_reat} [ohms]")

# Calculos voltados para o ensaio de rotor bloqueado
iL_medio = mean(I_linha_RB)
P_entrada = abs(P_wattimetros_RB[0] + P_wattimetros_RB[1])

if montagem == "delta":
    i_fase = iL_medio/sqrt(3)
    V_fi = V_L_RB
elif montagem == "estrela":
    V_fi = V_L_RB/sqrt(3)
    i_fase = iL_medio
else: print("Erro no fechamento do motor")

R2 = (P_entrada/(3*i_fase**2)) - R1

soma_x1_e_X2 = sqrt((V_fi/i_fase)**2 - (R1+R2)**2)
X2 = (1/(1+calc_coef(tipo_MIT))) * soma_x1_e_X2
X1 = soma_x1_e_X2 - X2

# Frequências devem ser iguais para poder somar e subtrair reatâncias diretamente. Frequência do ensaio a vazio é usada como referência uma vez que é a frequência nominal
if f1 != f2:
    k = f1/f2
    X1 = k*X1
    X2 = k*X2

XM = soma_reat - X1

print(f"\nDADOS CALCULADOS DO CIRCUITO EQUIVALENTE, TIPO DO MOTOR: {tipo_MIT}")

print(f"R1 = {R1} [ohms]")
print(f"R2 = {R2} [ohms]")
print(f"X1 = {X1} [ohms]")
print(f"X2 = {X2} [ohms]")
print(f"XM = {XM} [ohms]")
