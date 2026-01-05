#
# ref: https://www.qrisp.eu/general/tutorial/tutorial.html
# 
from qrisp import QuantumFloat, control, QFT, h 

def QPE(psi, U, precision):
    res = QuantumFloat(precision, -precision)
    h(res)
    for i in range(precision):
        with control(res[i]):
            for j in range(2**i):
                U(psi)
    return QFT(res, inv=True)

from qrisp import p, QuantumVariable, multi_measurement
import numpy as np

def U(psi):
    phi_1 = 0.5
    phi_2 = 0.125
    
    p(phi_1*2*np.pi, psi[0])   # p: phase gate  |0>은 그대로 두고, |1> -> e^{i phi}|1> 
    p(phi_2*2*np.pi, psi[1])
    
psi = QuantumVariable(2)
h(psi)
res = QPE(psi, U, 3) 
print(multi_measurement([psi,res]))