using Qiskit
using Qiskit.C # lower-level C API functions

function build_bell()
    qc = QuantumCircuit(2, 2) # 2 qubits, 2 clbits
    qc.h(1)
    qc.cx(1, 2)
    qc.measure(1, 1)
    qc.measure(2, 2)
    qc
end

function build_chain_target(num_qubits)
    target = Qiskit.Target(num_qubits)

    # Add 1q basis gates
    for gate in (QkGate_X, QkGate_SX, QkGate_RZ)
        entry = Qiskit.target_entry_gate(gate)
        for i in 1:num_qubits
            error = 0.8e-6 * i
            duration = 1.8e-9 * i
            qk_target_entry_add_property(entry, [i], duration, error)
        end
        qk_target_add_instruction(target, entry)
    end

    # Add 2q basis gate (ECR)
    ecr_entry = Qiskit.target_entry_gate(QkGate_ECR)
    for i in 1:num_qubits-1
        inst_error = 0.0090393 * (num_qubits - i + 1)
        inst_duration = 0.020039
        qk_target_entry_add_property(ecr_entry, [i, i + 1], inst_duration, inst_error)
    end
    qk_target_add_instruction(target, ecr_entry)

    # Add measurement instruction
    meas_entry = Qiskit.target_entry_measure()
    for i in 1:num_qubits
        error = 0.0
        duration = 0.0
        qk_target_entry_add_property(meas_entry, [i], duration, error)
    end
    qk_target_add_instruction(target, meas_entry)

    return target
end

qc = build_bell()
@show qc.num_instructions

target = build_chain_target(qc.num_qubits)

result = transpile(qc, target)
@show result.circuit.num_instructions