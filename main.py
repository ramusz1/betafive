from game import Game
from random_bot import RandomBot
from mcts_bot import MCTSBot

randomWins = 0
betaWins = 0

for i in range(300):
    game = Game()
    randomBot = RandomBot()
    betaFive = RandomBot()
    # betaFive = MCTSBot()

    randomStarts = (i % 2 == 0)

    if randomStarts:
        current, waiting = randomBot, betaFive
    else:
        current, waiting = betaFive, randomBot

    while game.isOn():
        x, y = current.getMove(game)
        game = game.makeMove(x, y)
        current, waiting = waiting, current

    winner = game.getWinner()
    if winner == 0:
        continue
    if (randomStarts and winner == 1) or (not randomStarts and winner == -1):
        randomWins += 1
    else:
        betaWins += 1
    game.visualize()

print('score: ', betaWins / (randomWins + betaWins) )