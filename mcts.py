# monte carlo tree search

'''
Explanation: ??? xD

'''

class GameState:

    def __init__(self, game):
        self.game = game
        self.nextMoves = None
        self.prevMove = None
        self.value = None
        self.needsEvaluation = True

    def isLeaf(self):
        return self.nextMoves is None

    def getMostPopularMove(self):
        mostPopular = max(self.nextMoves, key = lambda edge: edge.N)
        return mostPopular

    def setChildren(self, children):
        self.nextMoves = children

    def getHighestScoringMove(self):
        chosen = max(self.nextMoves, key = lambda edge: edge.getScore())
        ''''
        # softmax - for later - improves exploration
        score = np.array(list(map(Node.getScore, self.nextMoves)))
        e_score = np. exp(score - np.max(score))
        probs = e_score / e_score.sum()
        chosen = np.random.choice(self.nextMoves, p=probs)[0]
        '''
        return chosen

    def backup(self, value):
        self.value = value
        self.needsEvaluation = False
        self.prevmove.backup(value)

    def backup(self):
        self.prevMove.backup(self.value)

    def needsEvaluation(self):
        return self.needsEvaluation

class Move:

    puctConst = 1.4142
    totalN = 0

    def __init__(self, before, after, move, prob):
        self.before = before
        self.after = after

        self.move = move
        self.P = prob # prior probability
        self.N = 0 # visit count
        self.Q = 0 # action value
        self.V = 0 # score

    def getScore(self):
        return self.Q + self.getUpperBound()

    def getUpperBound(self):
        return self.P * Move.puctConst * np.sqrt(Move.totalN) / (1 + self.N)

    ## backup with value
    def backup(self, value):
        self.V += value
        self.N += 1
        self.Q = self.V / self.N
        if self.before.prevMove is not None:
            self.before.prevMove._backupNoValue(value)

    ## backup, but the value is for the opposite player
    def _backupNoValue(self, value):
        self.N += 1
        self.Q = self.V / self.N
        if self.before.prevMove is not None:
            self.before.prevMove.backup(value)

class MCTS:

    def __init__(self, evaluator):
        self.root = None
        self.simulations = 10
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
                leaf.backup(value)
            else:
                leaf.backup()

        self.bestMove = self.root.getMostPopularMove.move, self.root.player

    ## select a path to a leaf
    def select(self, node):
        if node.isLeaf():
            return node
        child = node.getHighestScoringMove().after
        return self.select(child)

    def evaluate(self, leaf):
        game = leaf.game
        legalMoves = game.getLegalMoves()
        probs, value = self.evaluator(game.board, game.player)
        self.expandTree(leaf, legalMoves, probs)
        return value

    def expandTree(self, leaf, legalMoves, probs):
        game = leaf.game
        legalMoves = self._applyProbabilitiesToMoves(legalMoves, probs, game.board.shape)
        children = self._getChildren(legalMoves, leaf)
        if 0 <= len(children):
            leaf.setChildren(children)

    @staticmethod
    def _applyProbabilitiesToMoves(moves, probs, boardShape):
        probs = probs.reshape(boardShape)
        probsOfLegalMoves = np.zeros(len(moves))
        for i, move in enumerate(moves):
            probsOfLegalMoves[i] = probs[move[0], move[1]]
        return np.stack((moves, probsOfLegalMoves), axis = 1)

    @staticmethod
    def _getChildren(legalMovesWithProbs, parent):
        # children = np.full(len(legalMovesWithProbs), None, dtype=Edge)
        children = []
        for i, (x, y, prob) in enumerate(legalMovesWithProbs):
            newGame = parent.game.makeMove(x,y)
            child = Node(newGame, player)
            edge = Edge(parent, child, (x,y), prob)
            child.parent = edge
            children.append(edge)
            # children[i] = edge

        return np.array(children)
        # return children

    def getBestMove(self):
        return self.bestMove

    ## go to the best child from root and discard everything but the child subtree
    def advance(self):
        pass