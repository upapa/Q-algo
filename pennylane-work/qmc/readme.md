DGX spark에서 CPU, GPU 속도 비교
NOTE: CPU모드에서 multi-thread가 가능(20cores). 
python은 일반적은 multi-thread 계산이 불가능한데, pennylane back-end가 지원하는 것 같다. 

n=m=9 (# of real qubits=19)
CPU: 4.7 sec
GPU: 4.4 sec

n=m=10 (# of real qubist=21)
CPU: 35.2 sec
GPU: 24.5 sec

n=m=11 (# of real qubist=23)
CPU: 264 sec
GPU: 192 sec

n=m=12 (# of real qubits=25)
CPU: 2256 sec
GPU: 1689 sec
