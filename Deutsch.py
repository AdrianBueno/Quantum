from projectq.ops import H, Measure, X, Y, Z, CNOT
from projectq import MainEngine
from projectq.meta import Loop, Compute, Uncompute, Control

#Algoritmo de Deutsch básico.
def runDeutsch(eng, oracle):
    # Instanciamos dos qubits
    q1 = eng.allocate_qubit()
    q2 = eng.allocate_qubit()
    # Mediante las puertas de Pauli fijamos el estado de incicio de los qubits
    Z | q1 # inicializamos al estado |0> el primer qubit
    X | q2 # y al estado |1> el segundo
    # El estado del sistema sería el indicado en la sección 5.1.2

    # Mediante la puerta de Hadamard pones los dos qubit en estado de superposición (sección 5.1.3)
    H | q1
    H | q2
    # Aplicamos el oráculo, en el circuito el operador U_f, que puede ser una función continua o balanceada
    oracle(q1,q2)

    # Como seguimos teniendo una superposición aplicando de nuevo la puerta H,
    # la superposición se deshará y mediremos 0 o 1 en función de lo que tenga dentro el oráculo.
    H | q1
    # Medimos.
    Measure | q1
    Measure | q2

    eng.flush()
    # imprimimos el resultado
    print("Measured: {}".format(int(q1)))

#Estos son los posibles oráculos que podemos pasar en este algoritmo

def function_deutsch_balanceada(q1, q2):
    # Aplicamos la Controlled NOT.
    CNOT | (q1, q2)
    # Aplicamos a q2 la pauli X
    X | q2
    # Entonces q1 = 1 -> 0 XOR f(x) -> f(1) = 1 y f(0) = 0

def function_deutsch_continua(q1, q2):
    # Aplicamos a q2 la pauli X: X 0 = 1 -> 1 XOR f(x) -> f(1) = 0 y f(0) = 1
    X | q2


if __name__ == "__main__":

    eng = MainEngine()  
    runDeutsch(eng, function_deutsch_balanceada)
