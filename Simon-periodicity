from projectq.ops import H, Measure, X, Y, Z, CNOT, All, Toffoli
from projectq import MainEngine
from projectq.meta import Loop, Compute, Uncompute, Control
from projectq.backends import CircuitDrawer
import array as arr
#Simon's periodicity algorithm

aux = arr.array('i', [1,0,1]) #Definimos el valor de c para el oraculo
n = 3 # el tamaño de c debe ser igual que n

def runDeutsch(eng, n, oracle):
    drawing_engine = CircuitDrawer() # Esto nos permite que se registre todo el circuito ejecutado.
    x = eng.allocate_qureg(n) #con esta instruccion instanciamos un array de qubits, x. (Entrada superior)
    y = eng.allocate_qureg(n) #con esta instruccion instanciamos un array de qubits, y. (Entrada inferior)

    #Aplicamos la puerta H a todos los qubits de x, dejandolos en una superposicion.
    All(H) | x

    #Inicializamos c como qubit para poder usarlo en la puerta como control
    c = eng.allocate_qureg(n)
    initialize_c(c)
    oracle(x,y,c)

    # Volvemos a aplicar H a todos los qubits de x para retirar la superposicion.
    # En funicion del oraculo algunos pueden estar en inversion de fase y anularse entre si.
    All(H) | x

    #Mediciones
    All(Measure) | x
    All(Measure) | y

    for qs in x:
        print("Measured: {}".format(int(qs)))

    # Con esta instruccion obtendremos como salida el codigo latex que permitira mostrar el circuito ejecutado
    # print(drawing_engine.get_latex())


#funcion generica
def function_generica(x, y, c):
    for i in range(len(c)):
        X | x[i]
        Toffoli | (x[i], c[i], y[i])
        X | x[i]

# Inicializamos c.
def initialize_c(c):
    for i in range(len(c)):
        if aux[i] == 1:
            X| c[i]


if __name__ == "__main__":
    eng = MainEngine()  # use default compiler engine
    runDeutsch(eng, n, function_generica)
    eng.flush()





def function_simon(x, y):
    X | x[0]
    X | x[1]
    Toffoli | (x[0], x[1], y[0])
    X | x[0]
    X | x[1]

    X | x[0]
    X | x[2]
    Toffoli | (x[0], x[2], y[1])
    X | x[0]
    X | x[2]

    X | x[1]
    X | x[2]
    Toffoli | (x[1], x[2], y[2])
    X | x[1]
    X | x[2]

    Toffoli | (x[0], x[1], y[0])
    Toffoli | (x[0], x[2], y[1])
    Toffoli | (x[1], x[2], y[2])
