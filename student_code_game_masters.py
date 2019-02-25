from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        if self.kb.kb_ask(parse_input("fact: (on disk4 ?X")) is False:
            disks = ["disk1", "disk2", "disk3"]
        
        else:
            disks = ["disk1", "disk2", "disk3", "disk4", "disk5"]
        
        peg1 = []
        peg2 = []
        peg3 = []
        
        for disk in disks:
            
            q = parse_input("fact: (on " + disk + " ?X)")
            a = self.kb.kb_ask(q)

            if str(a[0]) == "?X : peg1":
                peg1.append(int(disk[-1]))

            if str(a[0]) == "?X : peg2":
                peg2.append(int(disk[-1]))

            if str(a[0]) == "?X : peg3":
                peg3.append(int(disk[-1]))

        return (tuple(peg1), tuple(peg2), tuple(peg3))

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        save = self.getGameState()

        disk = str(movable_statement.terms[0])

        first = str(movable_statement.terms[1])
        goal = str(movable_statement.terms[2])
        
        firstnum = int(first[-1])
        goalnum = int(goal[-1])

        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + first + ")"))

        self.kb.kb_add(parse_input("fact: (on " + disk + " " + goal + ")"))

        if save[goalnum - 1]:
            self.kb.kb_retract(parse_input("fact: (top disk" + str(save[goalnum - 1][0]) + " " + goal + ")"))
        
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + goal + ")"))

        self.kb.kb_add(parse_input("fact: (top " + disk + " " + goal + ")"))

        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + first + ")"))

        save = self.getGameState()

        if save[firstnum - 1]:
            self.kb.kb_add(parse_input("fact: (top disk" + str(save[firstnum - 1][0])+ " " + first + ")"))
        
        else:
            self.kb.kb_add(parse_input("fact: (empty " + first + ")"))            

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        row1 = []
        row2 = []
        row3 = []

        for x in range(3):
            
            for y in range(3):
                a = parse_input("fact: (coordinate ?X pos" + str(x + 1) + " pos" + str(y + 1) + ")")
                tile = str(self.kb.kb_ask(a)[0])[-1]

                if tile == "y":
                    tile = -1
                
                if y == 0:
                    row1.append(int(tile))

                if y == 1:
                    row2.append(int(tile))

                if y == 2:
                    row3.append(int(tile))

        return (tuple(row1), tuple(row2), tuple(row3))

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        save = self.getGameState()

        tile = str(movable_statement.terms[0])
        firstx = str(movable_statement.terms[1])
        firsty = str(movable_statement.terms[2])
        goalx = str(movable_statement.terms[3])
        goaly = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (coordinate " + tile + " " + firstx + " " + firsty + ")"))
        self.kb.kb_retract(parse_input("fact: (coordinate empty " + goalx + " " + goaly + ")"))

        self.kb.kb_add(parse_input("fact: (coordinate " + tile + " " + goalx + " " + goaly + ")"))
        self.kb.kb_add(parse_input("fact: (coordinate empty " + firstx + " " + firsty + ")"))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
