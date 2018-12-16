from mcts import MCTS
import numpy as np

class SimpleEvaluator:
    
    def __call__(self, game):
        board = game.board
        prob = 1 / board.size
        probs = np.full(board.size, prob)
        originalPlayer = game.player
        winner = self.rollout(game)
        if winner == 0:
            return probs, 0.5
        score = (winner + originalPlayer) / 2
        return probs, score

    def rollout(self, game):
        while game.isOn():
            legalMoves = game.getLegalMoves()
            moveId = np.random.randint(len(legalMoves))
            move = legalMoves[moveId]
            game = game.makeMove(move[0],move[1])
        return game.getWinner()

class MCTSBot:

    def getMove(self, game):
        evaluator = SimpleEvaluator()
        mcts = MCTS(evaluator)

        mcts.run(game)
        # mcts.dump()
        return mcts.getBestMove()