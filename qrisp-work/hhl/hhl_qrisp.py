#
# ref: https://www.qrisp.eu/general/tutorial/HHL.html
#

from qrisp import *

def fake_inversion(qf, res=None):
    if res is None:
        res = QuantumFloat(qf.size + 1)
    for i in jrange(qf.size):
        cx(qf[i], res[qf.size - i])
    return res

@RUS(static_argnums=[0, 1])
def HHL_encoding(b, hamiltonian_evolution, n, precision):
    # Prepare the state |b>. Step 1
    qf = QuantumFloat(n)
    # Reverse the endianness for compatibility with Hamiltonian simulation.
    prepare(qf, b, reversed=True)

    qpe_res = QPE(qf, hamiltonian_evolution, precision=precision)  # Step 2
    inv_res = fake_inversion(qpe_res)  # Step 3

    case_indicator = QuantumFloat(inv_res.size)

    with conjugate(h)(case_indicator):
        qbl = case_indicator >= inv_res

    cancellation_bool = (measure(case_indicator) == 0) & (measure(qbl) == 0)

    # The first return value is a boolean.
    # Additional return values are QuantumVariables.
    return cancellation_bool, qf, qpe_res, inv_res

def HHL(b, hamiltonian_evolution, n, precision):
    qf, qpe_res, inv_res = HHL_encoding(b, hamiltonian_evolution, n, precision)
    with invert():
        QPE(qf, hamiltonian_evolution, target=qpe_res)
        fake_inversion(qpe_res, res=inv_res)
    # Reverse the endianness for compatibility with Hamiltonian simulation.
    for i in jrange(qf.size // 2):
        swap(qf[i], qf[n - i - 1])
    return qf


from qrisp.operators import QubitOperator
import numpy as np

# A = np.array([[3 / 8, 1 / 8], [1 / 8, 3 / 8]])
# b = np.array([1, 1])
# H = QubitOperator.from_matrix(A).to_pauli()
# def U(qf):
#     # By default e^{-itH} is performed. Therefore, we set t=-pi.
#     H.trotterization()(qf, t=-np.pi, steps=1)

# @terminal_sampling
# def main():
#     x = HHL(tuple(b), U, 1, 3)
#     return x

# res_dict = main()
# for k, v in res_dict.items():
#     res_dict[k] = v**0.5
# print(res_dict)

# x = (np.linalg.inv(A) @ b) / np.linalg.norm(np.linalg.inv(A) @ b)
# print(x)

def hermitian_matrix_with_power_of_2_eigenvalues(n):
    # Generate eigenvalues as inverse powers of 2.
    eigenvalues = 1 / np.exp2(np.random.randint(1, 4, size=n))

    # Generate a random unitary matrix.
    Q, _ = np.linalg.qr(np.random.randn(n, n))

    # Construct the Hermitian matrix.
    A = Q @ np.diag(eigenvalues) @ Q.conj().T

    return A


# Example
n = 3
A = hermitian_matrix_with_power_of_2_eigenvalues(2**n)

H = QubitOperator.from_matrix(A).to_pauli()


def U(qf):
    H.trotterization()(qf, t=-np.pi, steps=5)


b = np.random.randint(0, 2, size=2**n)

print("Hermitian matrix A:")
print(A)

print("Eigenvalues:")
print(np.linalg.eigvals(A))

print("b:")
print(b)

@terminal_sampling
def main():

    x = HHL(tuple(b), U, n, 4)
    return x


res_dict = main()

for k, v in res_dict.items():
    res_dict[k] = v**0.5

print(np.array([res_dict[key] for key in sorted(res_dict)]))

x = (np.linalg.inv(A) @ b) / np.linalg.norm(np.linalg.inv(A) @ b)
print(x)