# Este script contiene una implementacion simple del algoritmo UCT Monte Carlo Tree Search (MCTS UTC) en Python 2.7
# La funcion estrella UCT(rootstate, itermax, verbose = False) se encuentra cerca del fondo del codigo.
# La eficiencia de este algoritmo se ha reducido para aumentar la claridad de su implementacion.

# Escrito por Peter Cowling, Ed Powley, Daniel Whitehouse and Daniel Hernandez (University of York, UK) September 2012 - 2017.

from __future__ import division  # Para que el operador de division '/' tenga la misma funcionalidad que Python3.
from math import *  # Necesario para la equacion de UCB1. Usaremos math.sqrt y math.log
import random

import colorama # Para imprimir texto de colores en la terminal.
from colorama import Fore

import sys

class GameState:
    """
        Un GameState representa una configuracion valida del 'estado' de un juego.
        Por ejemplo, las posiciones de todas las piezas activas en una partida de ajedrez.
        Las funciones presentadas en esta clase son las minimas necesarias
        para la implementacion del algoritmo UCT para cualquier juego de 2-jugadores.

        Esta clase es una interfaz. Su uso es puramente ilustrativo. Trabajad con la clase Connect4State 
    """

    def __init__(self):
        self.playerJustMoved = 2  # Al empezar el juego se considera que el jugador 2 ha hecho un movimiento. Que es equivalente a decir que el jugador 1 empieza.

    def Clone(self):
        """ Crea una copia profunda del estado del juego.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Transforma el GameState al llevar a cabo el movimiento 'move'.
            Es importante que se actualize playerJustMoved, la variable que indica a quien le toca jugar.

            @input move: (int) accion tomada por el agente
        """
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ Devuelve una array con todos los posibles movimientos
        """

    def GetResult(self, playerJustMoved):
        """ Devuelve el ganador de la partida desde el punto de vista de playerJustMoved.

            @input playerJustMoved: (int) numero del jugador que acaba de tomar una accion.
        """

    def __repr__(self):
        """ Funcion 'built in' de python. devuelve una string del objecto (como obj.toString() en Java)
        """
        pass


class Connect4State:
    """
        GameState para el juego de 4 en Raya (Connect4 en ingles).
        El tablero (board) es una array 2D (filas y columnas).
        Para cada entrada de la array: 0 = vacio, 1 = jugador 1 (X), 2 = jugador 2 (O)
        En el juego de 4 en Raya los jugadores se turnan para dejar caer piezas
        en una de las 7 columnas, cada columna puede contener 6 piezas. El jugador que consigue
        crear una fila, columna o diagonal con 4 piezas, gana.
    """

    def __init__(self, width=7, height=6):
        self.playerJustMoved = 2  # Al empezar el juego se considera que el jugador 2 ha hecho un movimiento. Que es equivalente a decir que el jugador 1 empieza.
        self.winner = 0 # 0 = ningun ganador, 1 = jugador 1 ha ganado, 2 = jugador 2 ha ganado.

        self.width = width
        self.height = height
        self.InitializeBoard()

    def InitializeBoard(self):
        """ Inicializa el tablero de juego, la representacion interna del estado del tablero.
        """
        self.board = []  # 0 = vacio, 1 = jugador 1 (X), 2 = jugador 2 (O)
        for y in range(self.width):
            self.board.append([0] * self.height) # Genera una fila de 0s. Generando un tablero vacio

    def Clone(self):
        """ Crea una copia profunda del este GameState. Usado en las simulaciones 
            dado que el GameState de la simulacion tiene que ser diferente al GameState de la partida real.
        """
        st = Connect4State(width=self.width, height=self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = [self.board[col][:] for col in range(self.width)]
        return st

    def DoMove(self, movecol):
        """ Transforma el GameState al llevar a cabo el movimiento 'movecol'.
            Es importante que se actualize playerJustMoved.

            @input movecol: (int) columna sobre la que se va a soltar la pieza.
            @output void
        """

        assert movecol >= 0 and movecol <= self.width and self.board[movecol][self.height - 1] == 0
        row = self.height - 1
        while row >= 0 and self.board[movecol][row] == 0:
            row -= 1 # encuentra la primera fila ocupada (o 0 si no hay ninguna ficha en la columna)

        row += 1 # el primer espacio libre en la columna

        self.playerJustMoved = 3 - self.playerJustMoved # siguiente jugador
        self.board[movecol][row] = self.playerJustMoved # coloca la ficha en la celda correcta
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved # apunta el ganador de la partida

    def GetMoves(self):
        """ Devuelve una array con todos los movimientos posibles - todas las columnas que tienen un espacio libre.
        """
        if self.winner != 0:
            return [] # ningun movimiento posible dado que hay un ganador (in DoMove())
        return [col for col in range(self.width) if self.board[col][self.height - 1] == 0] # lista de columnas con espacio libre

    def DoesMoveWin(self, x, y):
        """ Comprueba si el movimiento en la posicion (x,y) genera una linea (columna, fila o diagonal) de longitud 4 (o mayor).
            No hace falta entender esta funcion.

            @input x: index de la columna
            @input y: index de la fila

            @output doesMoveWin: (boolean) True si el ultimo movimiento ha ganado la partida
        """
        me = self.board[x][y]
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            p = 1
            while self.IsOnBoard(x+p*dx, y+p*dy) and self.board[x+p*dx][y+p*dy] == me:
                p += 1
            # (x+(p-1)*dx,y+(p-1)*dy) is the last counter of my colour in direction (dx,dy) starting from (x,y)

            n = 1
            while self.IsOnBoard(x-n*dx, y-n*dy) and self.board[x-n*dx][y-n*dy] == me:
                n += 1
            # (x-(n-1)*dx,y-(n-1)*dy) is the last counter of my colour in direction (-dx,-dy) starting from (x,y)

            if p + n >= 5: # want (p-1) + (n-1) + 1 >= 4, or more simply p + n >- 5
                return True

        return False

    def IsOnBoard(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def GetResult(self, playerJustMoved):
        """ Devuelve el ganador de la partida desde el punto de vista de playerJustMoved.

            @input playerJustMoved: (int) numero del jugador que acaba de tomar una accion.

            @output: (int) 1 si el ultimo jugador en tomar una accion ha ganado la partida, 0 en cualquier otro caso.
        """
        return playerJustMoved == self.winner

    def IsGameOver(self):
        return self.GetMoves() == []

    def __repr__(self):
        s = ""
        for x in range(self.height - 1, -1, -1):
            for y in range(self.width):
                s += [Fore.WHITE + '.', Fore.RED + 'X', Fore.YELLOW + 'O'][self.board[y][x]]
                s += Fore.RESET
            s += "\n"
        return s


""" MCTS ALGORITHM
"""


class Node:
    """ Un nodo del game treee. self.wins siempre esta desde el punto de vista de playerJustMoved. (aclarar)
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # el move que se hizo en un state previo para llegar a este estado. "None" para el nodo raiz.
        self.parentNode = parent  # "None" para el nodo raiz
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # Futuros nodos hijo
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Usa la formula de UCB1 para seleccionar uno de los nodos hijo:
                lambda child: child.wins/child.visits + const * sqrt(2*log(self.visits)/child.visits)
            la constante se usa para escoger entre exploracion o explotacion.
            En este caso, const = 1
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, move, state):
        """ Quita move de la array untriedMoves y anhade un nuevo nodo hijo para este movimiento
            se devuelve el nodo hijo que se ha anhadido.

            @input move: (int) accion tomada por el agente
            @input state: (GameState) estado correspondiente al nuevo nodo hijo (childNode)

            @output node
        """
        node = Node(move=move, parent=self, state=state)
        self.untriedMoves.remove(move)
        self.childNodes.append(node)
        return node

    def Update(self, result):
        """ Actualiza las estadisticas guardadas en este nodo.
            Anhade una visita al contador de visitas del nodo, anhade el resultado (win/lose) desde el punto de vista del playerJustMoved
            One additional visit and result additional wins. Result must be from the viewpoint of playerJustmoved.

            @input result: (int) 1 denota victoria, 0 para el resto de los casos.
            @output void
        """
        self.visits += 1
        self.wins += result

    """ Funciones para debuggear y modo verbose
    """
    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduce una busqueda con el algoritmo MCTS-UCT durante itermax iteraciones empezando desde rootstate.
        Assume 2 jugadores que se alternan, con resultados finales en el rango [0.0, 1.0].

        @input itermax: (int) numero de simulaciones (partidas) que se van a ejecutar antes de decidir que accion tomar.

        @output move: (int) accion que llevar a cabo este turno.
    """

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        '''
        Part 1.1: Fase Seleccion
        '''
        while node.untriedMoves == [] and node.childNodes != []:  # Mientras el nodo este completamente expandido y non sea terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)


        '''
        part 1.2: fase expansion
        '''
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        '''
        part 1.3: fase Simulacion
        '''
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        '''
        part 1.3: fase Retropropagacion
        '''
        # Backpropagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved))  # Update node with result from POV of node.playerJustMoved
            node = node.parentNode

        '''
        part 1.3: fase Seleccion de accion
        '''
        move = sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[-1].move

    # Output some information about the tree - can be omitted
    if (verbose):
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return move


""" END OF MCTS ALGORITHM
"""


def PlayGame(initialState, vsAI=False):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = initialState
    while not state.IsGameOver():  # while not terminal state
        print(str(state))
        if state.playerJustMoved == 1:
            # JUGADOR 2
            m = HumanInput(state)
        else:
            # JUGADOR 1
            m = UCT(rootstate=state, itermax=3000, verbose=False)  # play with values for itermax and verbose = True
        state.DoMove(m)
    PrintResults(state)    

def PrintResults(state):
    """ Imprime los resultados de la partida una vez terminada
        Esta funcion asume que la partida ya ha terminado
    """
    if state.GetResult(state.playerJustMoved) == 1.0:
        print(str(state))
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print(str(state))
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
    else:
        print("Nobody wins!")


def HumanInput(state):
    """  Toma input para el juego desde standard input. Permite jugar a humanos.
	 Haz nota de como los indices de las columans van de [0,6], pero el input se toma de [1,7]
	 Esto se hace para que sea mas comodo jugar desde el teclado
    """

    valid_moves = state.GetMoves()
    move = None
    while move not in valid_moves:
        interface_moves = [move + 1 for move in valid_moves]
        move = int(raw_input("Possible moves are: " + str(interface_moves) + ' '))
        move -= 1
    return move

if __name__ == "__main__":
    colorama.init()  # Initiates colorma for color terminal text. This is required for windows machines
    PlayGame(Connect4State(width=7, height=6)) # Comienza el juego!
