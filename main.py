from game import Game
from random_bot import RandomBot
from mcts_bot import MCTSBot

gamesPlayed = 0
betaWins = 0
ties = 0

for i in range(1000):
    game = Game(n=5, k=4)
    randomBot = RandomBot()
    # betaFive = RandomBot()
    betaFive = MCTSBot()

    betaStarts = (i % 2 == 0)

    if betaStarts:
        current, waiting = betaFive, randomBot
    else:
        current, waiting = randomBot, betaFive

    while game.isOn():
        x, y = current.getMove(game)
        game = game.makeMove(x, y)
        current, waiting = waiting, current


    winner = game.getWinner()
    gamesPlayed += 1
    if winner == 0:
        ties += 1
    if (betaStarts and winner == 1) or (not betaStarts and winner == -1):
        betaWins += 1
    if betaStarts:
        print('beta is 1')
    else:
        print('beta is -1')
    game.visualize()

print('score: ', betaWins / gamesPlayed)
print('ties: ', ties / gamesPlayed)