
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True

        moves = self.gm.getMovables()

        currstate = self.currentState

        if moves:
            for move in moves:
                
                self.gm.makeMove(move)
                nextstate = GameState(self.gm.getGameState(), currstate.depth + 1, move)
                
                if nextstate not in self.visited:
                    nextstate.parent = currstate
                    currstate.children.append(nextstate)
                
                self.gm.reverseMove(move)

            while currstate.nextChildToVisit < len(currstate.children):
                
                nextstate = currstate.children[currstate.nextChildToVisit]
                
                if nextstate in self.visited:
                    currstate.nextChildToVisit = currstate.nextChildToVisit + 1

                else:
                    currstate.nextChildToVisit = currstate.nextChildToVisit + 1
                    
                    self.visited[nextstate] = True
                    self.gm.makeMove(nextstate.requiredMovable)
                    self.currentState = nextstate
                    
                    break

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.states = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition:
            return True

        moves = self.gm.getMovables()
        currstate = self.currentState

        if not currstate.children:
            for move in moves:
                
                self.gm.makeMove(move)
                nextstate = GameState(self.gm.getGameState(), currstate.depth + 1, move)

                if nextstate not in self.visited:
                    nextstate.parent = currstate
                    self.visited[nextstate] = False
                    currstate.children.append(nextstate)

                self.gm.reverseMove(move)

        for c in currstate.children:
            
            if not self.visited[c]:
                if c not in self.states:
                    self.states.append(c)

        nextstate = self.states.popleft()
        path = deque()
        
        tempstate = nextstate

        while tempstate.parent is not None:
            path.append(tempstate.requiredMovable)
            tempstate = tempstate.parent

        while self.currentState.parent is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        while path:
            self.gm.makeMove(path.pop())

        self.currentState = nextstate

        if self.currentState.state == self.victoryCondition:
            return True
        
        return False



