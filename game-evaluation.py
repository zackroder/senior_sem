# functions for game evaluation

from FerrersGame import FerrersGame

#returns all possible moves from a given game state (singular game board, not multiple games)
def allPossibleMoves(gameBoard):
    possibleMoves = []
    #indices of rows that can move
    rowIndices = range(0, len(gameBoard))
    colIndices = range(0, len(gameBoard))
    
    #add all possible moves to a list as tuple ("c"/"r", i)
    for index in rowIndices:
        possibleMoves.append(("r", index))
    for index in colIndices:
        possibleMoves.append(("c", index))

    return possibleMoves

def main():
    game = FerrersGame((4,4,4,4))
    game.visualizeFerrers(game.returnGameState()[0])

    print(allPossibleMoves(game.returnGameState()[0]))

main()