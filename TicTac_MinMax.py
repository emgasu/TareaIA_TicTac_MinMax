import math
import time
import random

tamañoTablero = 3
diag1 = [(tamañoTablero-1)*i for i in range(1, tamañoTablero+1)]
diag2Diff = int((math.pow(tamañoTablero, 2) - 1)/(tamañoTablero-1))
diag2 = [diag2Diff*i for i in range(tamañoTablero)]

posicionJugador = {"X": [], "O": []}

class Juego():
    def __init__(self):
        self.board = self.definirTablero()
        self.ganador = None
    
    @staticmethod
    def definirTablero():
        return [str(i) for i in range(int(math.pow(tamañoTablero, 2)))]
    
    def imprimirTablero(self):
        for fila in [self.board[i*tamañoTablero:(i+1) * tamañoTablero] for i in range(tamañoTablero)]:
            print('| ' + ' | '.join(fila) + ' |')

    def movimiento(self, posicion, letra):
        if Entero(self.board[posicion]):
            self.board[posicion] = letra
            if self.verificarGanador(posicion, letra):
                self.ganador = letra
            return True
        return False
    
    def regresarMovimiento(self, posicion, letra):
        if self.verificarGanador(posicion, letra):
            self.ganador = None
        self.board[posicion] = str(posicion)
    
    def verificarGanador(self, posicion, letra):
        filaIndice = math.floor(posicion/tamañoTablero)
        fila = self.board[filaIndice*tamañoTablero:(filaIndice+1)*tamañoTablero]
        if all([c == letra for c in fila]):
            return True
        
        colIndice = posicion % tamañoTablero
        col = [self.board[colIndice+(i*tamañoTablero)] for i in range(tamañoTablero)]
        if all([c == letra for c in col]):
            return True
        diagonal1 = [self.board[i] for i in diag1]
        if all([c == letra for c in diagonal1]):
            return True

        diagonal2 = [self.board[i] for i in diag2]
        if all([c == letra for c in diagonal2]):
            return True
        return False
    
    def movimientosDisponibles(self):
        posiciones = []
        for i in range(int(math.pow(tamañoTablero, 2))):
            if Entero(self.board[i]):
                posiciones.append(i)
        return posiciones
    
    def movimientoDisponiible(self):
        posiciones = set()
        for i in range(int(math.pow(tamañoTablero, 2))):
            if not Entero(self.board[i]):
                posiciones.update(self.obtenerPosicion(i))
        
        return list(posiciones)
    
    def obtenerPosicion(self, posicion):
        posiciones = []

        posiciones.append(posicion + tamañoTablero)
        posiciones.append(posicion - tamañoTablero)
        if posicion % tamañoTablero != 0:
            posiciones.append(posicion - 1)
            posiciones.append(posicion + tamañoTablero - 1)
            posiciones.append(posicion - tamañoTablero - 1)
        if (posicion + 1) % tamañoTablero != 0:
            posiciones.append(posicion + 1)
            posiciones.append(posicion + tamañoTablero + 1)
            posiciones.append(posicion - tamañoTablero + 1)
        
        finalposiciones = []
        for c in posiciones:
            
            if c >= 0 and c < int(math.pow(tamañoTablero, 2)) and Entero(self.board[c]):
                finalposiciones.append(c)
        
        return finalposiciones
    
    def tableroVacio(self):
        return len(self.movimientosDisponibles()) == int(math.pow(tamañoTablero, 2))
    
    def posicionesEsquinas(self):
        return [0, tamañoTablero-1, tamañoTablero*(tamañoTablero-1), int(math.pow(tamañoTablero, 2))-1]

def jugar(Juego, jugadorX, jugadorO):
    Juego.imprimirTablero()

    letra = "X"

    while Juego.ganador == None and len(Juego.movimientosDisponibles()) > 0:
        if letra == "X":
            posicion = jugadorX.movimiento(Juego)
        else:
            posicion = jugadorO.movimiento(Juego)
        
        
        posicionJugador[letra].append(posicion)
        Juego.obtenerPosicion(posicion)

        print("\n Tirada ", letra," \n")
        Juego.imprimirTablero()
    
     
        letra = "O" if letra == "X" else "X"

        time.sleep(0.5)
        
    

    if (Juego.ganador == None):
        print("\n Empate \n")
    else:
        print("\n Ganador \n ", Juego.ganador)

def Entero(a):
    try:
        int(a)
        return True
    except ValueError:
        return False
    

class jugador():
    def __init__(self, letra):
        self.letra = letra
    
    def movimiento(self, Juego):
        pass

class jugadorUsuario(jugador):
    def __init__(self, letra):
        super().__init__(letra)
    
    def movimiento(self, Juego):
        posiciones = Juego.movimientosDisponibles()
        while True:
            movimientoPosicion = int(input("\n Tirada Usuario  \n"))
            if (movimientoPosicion in posiciones):
                break
        Juego.movimiento(movimientoPosicion, self.letra)
        return movimientoPosicion


class jugadorIA(jugador):
    def __init__(self, letra):
        super().__init__(letra)
    
    def movimiento(self, Juego):
        # funcion de MiniMax y la poda alpha beta
        print("\n Tirada Maquina  \n")

        if Juego.tableroVacio():
            posiciones = Juego.movimientosDisponibles()
            movimientoPosicion = random.choice(posiciones)
        else:
            # minimax
            profundidad = len(Juego.movimientoDisponiible())
            marcador  = (self.minimax(Juego, profundidad, -math.inf, math.inf, True))
            movimientoPosicion =  marcador [" posicion "]
        Juego.movimiento(movimientoPosicion, self.letra)
        return movimientoPosicion


    def minimax(self, estadoJuego, profundidad, alpha, beta, isMaxjugador):
        maxjugador = self.letra
        minjugador = "X" 

        if profundidad == 0 or estadoJuego.ganador != None:
            if estadoJuego.ganador == maxjugador:
                return {" marcador ": 1 * (len(estadoJuego.movimientosDisponibles()) + 1), " posicion ": None}
            elif estadoJuego.ganador == minjugador:
                return {" marcador ": -1 * (len(estadoJuego.movimientosDisponibles()) + 1), " posicion ": None}
            else:
                return {" marcador ": 0, " posicion ": None}
        
        if isMaxjugador:
            mejorTirada  = {" marcador ": -math.inf, " posicion ": None}
            jugador = maxjugador
        else:
            mejorTirada  = {" marcador ": math.inf, " posicion ": None}
            jugador = minjugador
        
        for posHijo in estadoJuego.movimientoDisponiible():
            estadoJuego.movimiento(posHijo, jugador)
            eval = self.minimax(estadoJuego, profundidad-1, alpha, beta, not isMaxjugador)
            estadoJuego.regresarMovimiento(posHijo, jugador)
            eval[' posicion '] = posHijo

            if isMaxjugador:
                if eval[" marcador "] > mejorTirada [" marcador "]:
                    mejorTirada  = eval
                alpha = max(alpha, eval[" marcador "])
                if beta <= alpha:
                    break
            else:
                if eval[" marcador "] < mejorTirada [" marcador "]:
                    mejorTirada  = eval
                beta = min(beta, eval[" marcador "])
                if beta <= alpha:
                    break

        return mejorTirada  
    
    
if __name__ == "__main__":
    jugadorX = jugadorUsuario("X")
    jugadorO = jugadorIA("O")
    g = Juego()
    jugar(g, jugadorX, jugadorO)
    