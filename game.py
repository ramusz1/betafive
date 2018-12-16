import numpy as np

class Game:

    def __init__(self, board = None, n = 5, k = 3, player = 1, movesMade = 0):
        if board is None:
            self.board = np.zeros((n,n))
            self.n = n
        else:
            self.board = board
            self.n = board.shape[0]
        self.k = k
        self.player = player
        self.movesMade = movesMade
        self.maxMoves = n * n
        self.winner = None
        self._isOn = True

    def getBoard(self):
        return self.board

    def getPlayer(self):
        return self.player

    def visualize(self):
        print(self.board)

    def makeMove(self, x, y):
        if self.isValidMove(x, y):
            movesMade = self.movesMade + 1
            newBoard = self.board.copy()
            newBoard[x][y] = self.player
            nextPlayer = self.player * -1
            newGame = Game(board = newBoard, k = self.k, player = nextPlayer, movesMade = movesMade)
            newGame.checkGameState()
            return newGame
        else:
            raise ValueError("Invalid move")

    def isValidMove(self, x, y):
        if not self._isOn:
            return False
        return self.board[x][y] == 0

    def checkGameState(self):
        if not self._isOn:
            return
        for row in self.board:
            last = row[0]
            i = 1
            for piece in row[1:]:
                if piece != 0 and piece == last:
                    i += 1
                else:
                    i = 1
                    last = piece

                if i == self.k:
                    self.winner = piece
                    self._isOn = False

        emptySpots = self.maxMoves - self.movesMade
        if emptySpots == 0:
            self.winner = 0
            self._isOn = False

    def _swapPlayer(self):
        self.player *= -1

    def isOn(self):
        return self._isOn

    def getWinner(self):
        return self.winner

    def getLegalMoves(self):
        if not self._isOn:
            return []
        x,y = np.where(self.board == 0)
        return np.array([x,y]).T