import numpy as np

class RandomBot:

    def getMove(self, game):
        legalMoves = game.getLegalMoves()
        moveId = np.random.randint(len(legalMoves))
        move = legalMoves[moveId,:]
        return move