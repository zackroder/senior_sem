from copy import copy, deepcopy

class FerrersGame:
    __slots__ = 'a', '__dict__'
    def __init__(self, dimensions = (), currPlayer = 1, subgames = None):
        self.subgames = []
        if subgames:
            self.subgames = subgames
        else:
            self.subgames = []
            self.subgames.append(dimensions)
        self.currPlayer = currPlayer

    def __hash__(self):
        return hash(tuple(self.subgames))

    def __eq__(self, other):
        return (self.subgames) == (other.subgames)
    
    def visualizeFerrers(self, subGameIndex):
        if not self.subgames:
            print("EMPTY")
        else:
            for i in self.subgames[subGameIndex]:
                print ("O " * i)
                print("\n")

    def returnGameState(self):
        return self.subgames

    def showGameState(self):
        print("-----------CURRENT GAME STATE----------")
        print("Player " + str(self.currPlayer) + "'s turn")
        if len(self.subgames) == 1:
            self.visualizeFerrers(self.subgames[0])
        else:
            count = 0
            for game in self.subgames:
                print("~SUBGAME " + str(count) + "~")
                self.visualizeFerrers(game)
                count += 1
    
    #returns true
    def gameOver(self):
        if len(self.subgames) == 0:
            return True
        else:
            return False
    
    def playerTurnSwap(self):
        if self.currPlayer == 1:
            self.currPlayer = 2
        else:
            self.currPlayer = 1

    #choose subgame to move on, whether to pull row or column, and index of row/column
    def move(self, subgameNum, rowOrCol, index):
        if rowOrCol == "r":
            #if first or last row, no need to split
            if index in (0, (len(self.subgames[subgameNum]) - 1)):
                newGame = list(self.subgames[subgameNum])
                newGame.pop(index)

                if len(newGame) != 0:
                    self.subgames[subgameNum] = tuple(newGame)
                else:
                    self.subgames.pop(subgameNum)
            
            #otherwise, need to split up game
            else:
                subgame1 = self.subgames[subgameNum][:index]
                subgame2 = self.subgames[subgameNum][index+1:]
                
                #remove old game tuple
                self.subgames.pop(subgameNum)
                #add new games
                if len(subgame1) != 0:
                    self.subgames.append(tuple(subgame1))
                if len(subgame2) != 0:
                    self.subgames.append(tuple(subgame2))

        elif rowOrCol == "c":
            newGame = list(self.subgames[subgameNum])
            #if first or last column, no need to split
            if index in (0, self.subgames[subgameNum][0]-1):
                for i in range(len(newGame)-1, -1, -1):
                    if newGame[i] > index:
                        newGame[i] -= 1
                        if newGame[i] == 0:
                            newGame.pop(i)
                #empty game board discard
                if len(newGame) == 0:
                    self.subgames.pop(subgameNum)
                else:
                    self.subgames[subgameNum] = tuple(newGame)
            
            else:
                subgame1 = []
                subgame2 = []
                for i in self.subgames[subgameNum]:
                    if i > (index+1):
                        subgame1.append(index)
                        subgame2.append(i - index - 1)
                    elif i == (index+1):
                        subgame1.append(i-1)
                        #subgame 2, col index won't be at row i
                    elif i < (index + 1):
                        subgame1.append(i)
                
                self.subgames.pop(subgameNum)
                if len(subgame1) != 0:
                    self.subgames.append(tuple(subgame1))
                if len(subgame2) != 0:
                    self.subgames.append(tuple(subgame2))

        #check if game is over; if play should continue, return True and swap player; if it isn't, return False
        if not self.gameOver():
            self.playerTurnSwap()
            return True
        else:
            return False




    def testGame(self):
        keepPlaying = True
        while keepPlaying:
            self.showGameState()
            if len(self.subgames) != 1:
                subGameNum = int(input("Number of subgame to move on: "))
            else:
                subGameNum = 0
            rowOrCol = str(input("Row (r) or col (c): "))
            index = int(input("Index: "))
            continueGame = self.move(subGameNum, rowOrCol, index)
            if not continueGame:
                keepPlaying = False

        print ("Player " + str(self.currPlayer) + " wins!")

                   

        
        
