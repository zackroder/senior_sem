# functions for game evaluation

from copy import deepcopy, copy
from FerrersGame import FerrersGame

sgValues = {}


#returns all possible moves from a given game state
def allPossibleMoves(gameObj):
    possibleMoves = []
    gameBoard = gameObj.returnGameState()

    for i in range(len(gameBoard)):
        #indices of rows that can move
        rowIndices = range(0, len(gameBoard[i]))
        colIndices = range(0, gameBoard[i][0])
        
        #add all possible moves to a list as tuple ("c"/"r", i)
        for index in rowIndices:
            possibleMoves.append((i, "r", index))
        for index in colIndices:
            possibleMoves.append((i, "c", index))
        

    return possibleMoves

#returns all possible children of a given game board
def possibleChildGames(gameObj):
    gameBoard = gameObj.returnGameState()
    possibleMoves = allPossibleMoves(gameObj)

    children = []
    for i in range(len(possibleMoves)):
        children.append(FerrersGame(subgames=copy(gameBoard)))
        children[i].move(*possibleMoves[i])
    
    return children

#returns minimum excluded value of a list of a numbers
def mex(numbers):
    mex = 0
    while (mex in numbers):
        mex += 1
    return mex

#nim sum operator - takes list of nimbers, returns nim-sum
def nimSum(nimbers):
    nimsum = 0 #0 is XOR identity; 0 XOR A = A
    for i in nimbers:
        nimsum = nimsum ^ i
    
    return nimsum

#computes SG value of gameObj
def SGValueRecursive(gameObj):
    children = possibleChildGames(gameObj)
    #print(children)

    if gameObj in sgValues.keys():
        return sgValues[gameObj]

    elif len(children) == 0:
        sgValues[gameObj] = 0
        return 0 #p position
    else:
        childrenValues = []
        for child in children:
            childBoard = child.returnGameState()
            #print("child board: " + str(childBoard))
            #if game is made of multiple subgames, nim-sum them
            #print("BOARD: " + str(childBoard))
            if len(childBoard) > 1:
                #print("nim addition begin")
                nimbersToNimSum = []
                #print("NIM SUM")
                #print(childBoard)
                for subgame in childBoard:
                    subgameObj = FerrersGame(subgames = [copy(subgame)])
                    nimbersToNimSum.append(SGValueRecursive(subgameObj))
                
                #print("nim sum " + str(nimbersToNimSum))
                childrenValues.append(nimSum(nimbersToNimSum))
                
            else:
                childrenValues.append(SGValueRecursive(child))
        
        sgValue = mex(childrenValues)
        sgValues[gameObj] = sgValue
        return sgValue

    
            


def main():
    superGame = []
    for i in range(20):
        superGame.append(20)
    superGame = tuple(superGame)
    game = FerrersGame(superGame)
    
    print(SGValueRecursive(game))
    keys = sgValues.keys()

    with open("SGValues.txt", 'w') as f:
        for key in keys:
            f.write(str(key.subgames) + ": " + str(sgValues[key]) + '\n')

    
    
    

main()