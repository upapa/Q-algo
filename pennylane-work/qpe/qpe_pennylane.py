import pennylane as qml
import numpy as np

# 큐비트 한개에만 작용. 두개에 작용하는 것로 확장할 수 있을까?
# qrisp 데모 참조(두 개에 작용하는 유니터리 행렬)
# 
def U(wires):
    return qml.PhaseShift(2 * np.pi / 5, wires=wires)


dev = qml.device("default.qubit")
@qml.qnode(dev)
def circuit_qpe(estimation_wires):
    # initialize to state |1>
    qml.PauliX(wires=0)
    
    for wire in estimation_wires:
        qml.Hadamard(wires=wire)
    
    qml.ControlledSequence(U(wires=0), control=estimation_wires)
    
    qml.adjoint(qml.QFT)(wires=estimation_wires)
    
    return qml.probs(wires=estimation_wires)


import matplotlib.pyplot as plt
estimation_wires = range(1,5)
results = circuit_qpe(estimation_wires)
bit_strings = [f"0.{x:0{len(estimation_wires)}b}" for x in range(len(results))]
decimal_number = [int(f"{x:0{len(estimation_wires)}b}",2)*2**(-len(estimation_wires)) for x in range(len(results))]
# print(bit_strings)
# print(results)
   
plt.bar(bit_strings, results)
plt.xlabel("phase")
plt.ylabel("probability")
plt.xticks(rotation="vertical")
plt.subplots_adjust(bottom=0.3)
plt.savefig("out.png")

max_idx = np.argmax(results)
print("Max Prob: ", results[max_idx])
print("Binary String: ", bit_strings[max_idx])
print("Decimal Number: ", decimal_number[max_idx])