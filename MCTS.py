# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a
# state.GetRandomMove() or state.DoRandomRollout() function.
#
# Example GameState classes for Nim, OXO and Connect4 are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in
# the UCTPlayGame() function at the bottom of the code.
#
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012 - 2017.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
#
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai

from __future__ import division
from math import *
import random

import colorama
from colorama import Fore


class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """

    def __init__(self):
        self.playerJustMoved = 2  # At the root pretend the player just moved is player 2 - player 1 has the first move

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ Get all possible moves from this state.
        """

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass

class Connect4State:
    """ A state of the game of Connect4, i.e. the game board.
        The board is a 2D array where 0 = empty (.), 1 = player 1 (X), 2 = player 2 (O).
        In connect4 players alternately drop pieces down one of the 7 columns
        of a board with 6 rows - aiming that the piece dropped creates a row, column or
        diagonal of 4 pieces.
    """

    def __init__(self, width=7, height=6):
        self.playerJustMoved = 2  # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = []  # 0 = empty, 1 = player 1, 2 = player 2
        self.winner = 0 # No winner yet

        self.width = width
        self.height = height
        for y in range(self.width):
            self.board.append([0] * self.height) # six zeroes in each column

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = Connect4State(width=self.width, height=self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = [self.board[col][:] for col in range(self.width)]
        return st

    def DoMove(self, movecol):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """

        assert movecol >= 0 and movecol <= self.width and self.board[movecol][self.height - 1] == 0
        row = self.height - 1
        while row >= 0 and self.board[movecol][row] == 0:
            row -= 1 # find the first occupied row (or 0 for the bottom of the board

        row += 1 # the first empty space in movecol

        self.playerJustMoved = 3 - self.playerJustMoved # new player
        self.board[movecol][row] = self.playerJustMoved # drop the counter
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved # record the win

    def GetMoves(self):
        """ Get all possible moves from this state - i.e. all columns with at least one empty space.
        """
        if self.winner != 0:
            return [] # no moves since someone has already won (in DoMove())
        return [col for col in range(self.width) if self.board[col][self.height - 1] == 0] # columns a list of columns with space

    def DoesMoveWin(self, x, y):
        """ Does the move at (x,y) win by forming a row, column or diagonal of length at least 4?
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

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        return playerjm == self.winner

    def __repr__(self):
        s = ""
        for x in range(self.height - 1, -1, -1):
            for y in range(self.width):
                s += [Fore.WHITE + '.', Fore.RED + 'X', Fore.YELLOW + 'O'][self.board[y][x]]
                s += Fore.RESET
            s += "\n"
        return s


class Node:
    """ A node in the game tree. self.wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. Result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

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
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved))  # Update node with result from POV of node.playerJustMoved
            node = node.parentNode

        # Selection # return the move that was most visited
        # move = sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move
        move = sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[-1].move

    # Output some information about the tree - can be omitted
    if (verbose):
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return move 


def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    # state = OXOState() # uncomment to play OXO
    # state = NimState(5)  # uncomment to play Nim with the given number of starting chips
    state = Connect4State(width=7, height=6)
    while (state.GetMoves() != []):  # while not terminal state
        print(str(state))
        if state.playerJustMoved == 1:
            # m = UCT(rootstate=state, itermax=10, verbose=False)  # play with values for itermax and verbose = True
            m = human_input(state)
        else:
            m = UCT(rootstate=state, itermax=20000, verbose=False)  # play with values for itermax and verbose = True
        print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print(str(state))
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print(str(state))
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
    else:
        print("Nobody wins!")


def human_input(state):
    valid_moves = state.GetMoves()
    move = ''
    while move not in valid_moves:
        move = int(raw_input("Possible moves are: " + str(valid_moves) + ' '))
    return move


if __name__ == "__main__":
    colorama.init()  # Initiates colorma for color terminal text. This is required for windows machines
    """ Play a single game to the end using UCT for both players."""
    UCTPlayGame()
