from projectq.ops import H, Measure, X, Y, Z, CNOT, All, Toffoli
from projectq import MainEngine
from projectq.meta import Loop, Compute, Uncompute, Control
from projectq.backends import CircuitDrawer

#Algoritmo de Deutsch-Jozsa.
def runDeutsch(eng, n, oracle):
    drawing_engine = CircuitDrawer() # Esto nos permite que se registre todo el circuito ejecutado.
    # Instanciamos dos qubits, estos se inicializan con valor |0>
    x = eng.allocate_qureg(n) #on esta instruccion instanciamos un array de qubits, x. (Entrada superior)
    q2 = eng.allocate_qubit() # qubit de la entrada inferior
    #Aplicamos la puerta H a todos los qubits de x, dejandolos en una superposicion.
    All(H) | x
    #Ponemos el estado |1> en la entrada inferior y luego aplicamos la puerta H para dejarlo en superposicion.
    #De este modo hacemos la inversion de fase.
    X | q2
    H | q2

    oracle(x,q2)

    # Volvemos a aplicar H a todos los qubits de x para retirar la superposicion.
    # En funicion del oraculo algunos pueden estar en inversion de fase y anularse entre si.
    All(H) | x

    #Mediciones
    All(Measure) | x
    Measure | q2
    eng.flush()

    #Imprimimos cada qubit de la cadena
    # Si medimos |0> para todo x, el oraculo implementa una funcion constnate.
    # Si encontramos cualquier otra cosa sera balanceada.
    for qb in x:
        print("Measured: {}".format(int(qb)))
    # Con esta instruccion obtendremos como salida el codigo latex que permitira mostrar el circuito ejecutado
    # print(drawing_engine.get_latex())

def function_jozsa_balanceada(x, q2):
    # Aplicamos CNOT, con X[0] como control y q2 como objetivo.
    # De esta manera, en la mitad de las posibles entradas q2 se invetira
    CNOT | (x[0], q2)

def function_jozsa_constante(x, q2):
    pass #No es necesario hacer nada, q2 se quedara como esta



if __name__ == "__main__":
    eng = MainEngine()  # use default compiler engine
    runDeutsch(eng, 2,  function_jozsa_balanceada)
