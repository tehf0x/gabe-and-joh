#Extended from source code found at
#http://en.literateprograms.org/Tic_Tac_Toe_(Python)?oldid=13355
#Gabe Arnold <gabe@squirrelsoup.net

# Copyright (c) 2009 the authors listed at the following URL, and/or
# the authors of referenced articles or incorporated external code:
# http://en.literateprograms.org/Tic_Tac_Toe_(Python)?action=history&offset=20080515043713
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Retrieved from: http://en.literateprograms.org/Tic_Tac_Toe_(Python)?oldid=13355

import operator, sys, random, time
from rlglue.environment import EnvironmentLoader
from wrapper_environment import WrapperEnvironment

def allEqual(list):
    """returns True if all the elements in a list are equal, or if the list is empty."""
    return not list or list == [list[0]] * len(list)

Empty = 0
Player_X = 2
Player_O = 1

class MiniMaxEnvironment(WrapperEnvironment):
    """Function for the computer player"""
    opponent = { Player_O : Player_X, Player_X : Player_O }
    player = WrapperEnvironment.color

    def judge(self, winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1

    def allEqual(list):
        """returns True if all the elements in a list are equal, or if the list is empty."""
        return not list or list == [list[0]] * len(list)

    def gameOver(self):
        """Returns true if one player has won or if there are no valid moves left."""
        return self.winner() or not self.getValidMoves()

    def winner(self):
        """Determine if one player has won the game. Returns Player_X, Player_O or None"""
        winning_rows = [[0,1,2],[3,4,5],[6,7,8], # vertical
                        [0,3,6],[1,4,7],[2,5,8], # horizontal
                        [0,4,8],[2,4,6]]         # diagonal
        for row in winning_rows:
            if self.state[row[0]] != Empty and self.allEqual([self.state[i] for i in row]):
                return self.state[row[0]]

    def getValidMoves(self):
        """Returns a list of valid moves. A move can be passed to getMoveName to
        retrieve a human-readable name or to makeMove/undoMove to play it."""
        return [pos for pos in range(9) if self.state[pos] == Empty]

    def evaluateMove(self, move, p=player):
        try:
            self.state[move] = self.color
            if self.gameOver():
                return self.judge(self.winner())
            outcomes = (evaluateMove(next_move, opponent[p]) for next_move in self.getValidMoves())

            if p == player:
                #return min(outcomes)
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o,min_element)
                return min_element
            else:
                #return max(outcomes)
                max_element = -1
                for o in outcomes:
                    if o == +1:
                        return o
                    max_element = max(o,max_element)
                return max_element

        finally:
            self.state[move] = 0

    def play(self):
        moves = [(move, self.evaluateMove(move)) for move in self.getValidMoves()]
        random.shuffle(moves)
        moves.sort(key = lambda (move, winner): winner)
        self.state[moves[-1][0]] == player

if __name__ == "__main__":
    EnvironmentLoader.loadEnvironment(MiniMaxEnvironment())
