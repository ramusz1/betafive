from mcts import MCTS
import numpy as np

class EvenEvaluator:
    
    def __call__(self, board, player):
        prob = 1 / board.size
        probs = np.full(board.size, prob)
        return probs, 0.5

class MCTSBot:

    def getMove(self, game):
        evaluator = EvenEvaluator()
        mcts = MCTS(evaluator)

        mcts.run(game)
        return mcts.getBestMove()