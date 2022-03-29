# functions for game evaluation

from copy import deepcopy, copy
from FerrersGame import FerrersGame
import pandas as pd

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

#function to efficiently generate integer partitions: https://jeromekelleher.net/generating-integer-partitions.html
def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

#check that partition is not ''quadrated''-- we have already shown that all games of this type are P-position
#even number of even numbers
def isQuadrated(partition):
    if len(partition) % 2 == 0:
        for k in partition:
            if k % 2 != 0:
                return False
        return True
    else:
        return False



def main():

    #for i in range(1,21):
    #    dimensions = [i]
    #    for j in range(0,i):
    #        dimensions.append(1)
    #    dimensions = tuple(dimensions)
    #    
    sgValueDict = dict()
    for i in range(2,10):
        for j in range(2,10):
            
            rectPart = [i] * j

            #compute SG of rectangle partition
            part = tuple(rectPart)
            print(part)
            quadrated = isQuadrated(part)
            value = SGValueRecursive(FerrersGame(dimensions=part))
            sgValueDict[str(part)] = {"sg_value": value, "quadrated": quadrated}

            
            lastRowIndex = j-1
            up = 0
            while rectPart[lastRowIndex] > 1:
                rectPart[lastRowIndex] -= 1
                if up > 0:
                    rectPart[lastRowIndex-up] -= 1

                part = tuple(rectPart)
                print(part)
                quadrated = isQuadrated(part)
                value = SGValueRecursive(FerrersGame(dimensions=part))
                sgValueDict[str(part)] = {"sg_value": value, "quadrated": quadrated}
        
                up += 1
            
            
            

    #game = FerrersGame(dimensions=(4,))
    #print(SGValueRecursive(game))

    keys = sgValueDict.keys()

    df = pd.DataFrame.from_dict(sgValueDict, orient='index')
    print(df.head)
    df.to_csv("SGValuesDegenerateStaircases.csv")

    #with open("SGValuesTest1.txt", 'w') as f:
    #    for key in sgValueDict:
    #       f.write(str(key) + ": " + str(sgValueDict[key]) + '\n')

    
    
    

main()
