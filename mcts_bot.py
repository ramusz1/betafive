from mcts import MCTS

class EvenEvaluator:
    
    def __call__(self, board, player):
        prob = 1 / board.size
        probs = np.fill(board.size, prob)
        return probs, 0.5

class MCTSBot:

    def getMove(self, game):
        evaluator = EvenEvaluator()
        self.mcst = MCTS(evaluator)

        self.mcts.run(game)
        return self.mcts.getBestMove()