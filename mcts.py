# monte carlo tree search

'''
Explanation: ??? xD

'''
import numpy as np

class GameState:

    def __init__(self, game):
        self.game = game
        self.nextMoves = None
        self.prevMove = None
        self.value = None
        self._needsEvaluation = True

    def isLeaf(self):
        return self.nextMoves is None

    def getMostPopularMove(self):
        mostPopular = max(self.nextMoves, key = lambda move: move.N)
        return mostPopular

    def setChildren(self, children):
        self.nextMoves = children

    def getHighestScoringMove(self):
        return max(self.nextMoves, key = lambda move: move.getScore())

    def backup(self, value):
        self.value = value
        self._needsEvaluation = False
        if self.prevMove is not None:
            if value == 0.5:
                self.prevMove.backupAll(value)
            elif value == 1:
                self.prevMove.backupLoser(value)
            else:
                self.prevMove.backupWinner(value)

    def needsEvaluation(self):
        return self._needsEvaluation

class Move:

    def __init__(self, before, after, move, prob):
        self.before = before
        self.after = after

        self.move = move
        self.P = prob # prior probability
        self.N = 0 # visit count
        self.Q = 0 # action value
        self.V = 0 # score

    def getScore(self):
        return self.Q

    def backupAll(self, value):
        self.V += value
        self.N += 1
        self.Q = self.V / self.N
        if self.before.prevMove is not None:
            self.before.prevMove.backupAll(value)

    ## backup with value
    def backupWinner(self, value):
        self.V += value
        self.N += 1
        self.Q = self.V / self.N
        if self.before.prevMove is not None:
            self.before.prevMove.backupLoser(value)

    ## backup, but the value is for the opposite player
    def backupLoser(self, value):
        self.N += 1
        self.Q = self.V / self.N
        if self.before.prevMove is not None:
            self.before.prevMove.backupWinner(value)

class MCTS:

    def __init__(self, evaluator):
        self.root = None
        self.simulations = 100
        self.evaluator = evaluator
        self.bestMove = None

    ## Get probabilities of each possible move
    def run(self, game):
        if self.root is None:
            self.root = GameState(game)

        for i in range(self.simulations):
            leaf = self.select(self.root)
            if leaf.needsEvaluation():
                value = self.evaluate(leaf)
            else:
                value = leaf.value
            leaf.backup(value)
        
        self.bestMove = self.root.getMostPopularMove().move

    ## select a path to a leaf
    def select(self, node):
        if node.isLeaf():
            return node
        child = node.getHighestScoringMove().after
        return self.select(child)

    def evaluate(self, leaf):
        game = leaf.game
        legalMoves = game.getLegalMoves()
        probs, value = self.evaluator(game)
        self.expandTree(leaf, legalMoves, probs)
        return value

    def expandTree(self, leaf, legalMoves, probs):
        game = leaf.game
        legalMoves = self._getLegalMovesWithProbs(legalMoves, probs, game.board.shape)
        children = self._getChildren(legalMoves, leaf)
        children = np.random.permutation(children)
        if 0 < len(children):
            leaf.setChildren(children)

    @staticmethod
    def _getLegalMovesWithProbs(moves, probs, boardShape):
        probs = probs.reshape(boardShape)
        legalMovesWithProbs = []
        for i, move in enumerate(moves):
            prob = probs[move[0], move[1]]
            yield move[0], move[1], prob

    @staticmethod
    def _getChildren(legalMovesWithProbs, parent):
        # children = np.full(len(legalMovesWithProbs), None, dtype=Edge)
        children = []
        for i, (x,y,prob) in enumerate(legalMovesWithProbs):
            newGame = parent.game.makeMove(x,y)
            child = GameState(newGame)
            edge = Move(parent, child, (x,y), prob)
            child.prevMove = edge
            children.append(edge)
            # children[i] = edge

        return np.array(children)
        # return children

    def dump(self):
        edges = list(self.root.nextMoves)
        edges.append(None)
        while edges:
            edge = edges[0]
            edges = edges[1:]
            if edge is None:
                print('\n')
                if edges:
                    edges.append(None)
            else:
                print(edge.N, end=' ')
                state = edge.after
                if state.nextMoves is not None:
                    edges += list(state.nextMoves)

    def getBestMove(self):
        return self.bestMove

    ## go to the best child from root and discard everything but the child subtree
    def advance(self):
        pass