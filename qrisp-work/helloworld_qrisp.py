from qrisp import QuantumString

org_str = "hello, quantum world!"   # "Hello, Quantum World!" 이건 안됨???
q_str = QuantumString(len(org_str))
q_str[:] = org_str
print(q_str)
