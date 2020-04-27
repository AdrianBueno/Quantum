from projectq.ops import H, Measure, X, Y, Z, CNOT
from projectq import MainEngine
from projectq.meta import Loop, Compute, Uncompute, Control
from projectq.backends import CircuitDrawer

#Algoritmo de Deutsch.
def runDeutsch(eng, oracle):
    drawing_engine = CircuitDrawer() # Esto nos permite que se registre todo el circuito ejecutado.
    # Instanciamos dos qubits, estos se inicializan con valor |0>
    q1 = eng.allocate_qubit()
    q2 = eng.allocate_qubit()
    X | q2 #Para realizar la inversion de fase dejamos el estado |1> con la puerta X

    # Ahora dejamos en superposicion los dos qubits mediante la puerta H.
    H | q1 # 1/sqrt(2) (|0> + |1>)
    H | q2 # 1/sqrt(2) (|0> - |1>)

    oracle(q1,q2) # Aplicamos U y obtenemos el estado: -1^f(x) |x> q2

    H | q1 # Aplicamos H para quitar la superposicion y obtener el estado 0|0> o -1|0>

    #Mediciones
    Measure | q1
    Measure | q2

    eng.flush() #Con esta instruccion finalizamos la parte cuantica
    # Ahora mostramos el valor de q1, si este esta en el estado |0> el oraculo implementa una funcion constante.
    # Por otro lado si tiene el estado |1> seria balanceada.
    print("Measured: {}".format(int(q1)))
    #Con esta instruccion obtendremos como salida el codigo latex que permitira mostrar el circuito ejecutado
    #print(drawing_engine.get_latex())


def function_deutsch_balanceada(q1, q2):
    # Aplicamos la Controlled NOT
    CNOT | (q1, q2) # q1 es el qubit de control y q2 el objetivo.
    # Ahora si q1 == 1 entonces q2 inventira su valor.

def function_deutsch_constante(q1, q2):
    pass # Para la constante no hacemos nada y q2 seguira como esta


if __name__ == "__main__":
    eng = MainEngine() # Con esta instruccion iniciamos la parte cuantica
    runDeutsch(eng, function_deutsch_constante) # Pasamos la funcion constante como oraculo.
