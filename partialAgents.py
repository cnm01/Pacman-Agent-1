# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up!"
        name = "Pacman"
        self.visited = []
        self.food = []
        self.last = Directions.STOP
        # self.ghostAroundCorner = False
        self.prevBuffer = [(-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5),(-1,-6),(-1,-7),(-1,-8)]
        # self.escapeBuffer = []
        self.destuckCtr = 0
        self.deGhostCtr = 0



    # This is what gets run in between multiple games
    def final(self, state):
        self.visited = []
        self.food = []
        self.last = Directions.STOP
        # self.ghostAroundCorner = False
        self.prevBuffer = [(-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5),(-1,-6),(-1,-7),(-1,-8)]
        # self.escapeBuffer = []
        self.destuckCtr = 0
        self.deGhostCtr = 0
        print " __________________"
        print "|                  |"
        print "|    Game Over!    |"
        print "|                  |"
        print " ------------------"


    def getAction(self, state):
        self.update(state)
        self.updateBuffer(state)




        #run from ghosts
        if self.ghostWithin3(state):
            return self.runFromGhost(state)

        if self.deGhosting(state):
            return self.deGhost(state);


        #if stuck go straight
        if self.isStuck(state) or self.destucking(state):
            return self.deStuck(state)
        self.escapeBuffer = []


        #go to food if within 1
        if self.foodWithin1(state):
            return self.followFood(state)



        # go to closest food||smallest food
        if self.foodSeen(state):
            return self.goTowardsClosestFood(state)


        # # map to lowest food
        # if self.foodSeen(state):
        #     # print "path to smallest food : ", self.pathToSmallestFood(state, [api.whereAmI(state)])
        #     # return self.goToSmallestFood
        #     return self.seekFood(state)

        return self.randomlyTraverse(state)


######################################################



    def foodSeen(self, state):
        if len(self.food) > 0: return True
        else: return False

    def update(self, state):
        cur = api.whereAmI(state)
        food = api.food(state)
        if cur not in self.visited:
            self.visited.append(cur)
        for x in food:
            if x not in self.food:
                self.food.append(x)
        if cur in self.food:
            self.food.remove(cur)

    def updateBuffer(self, state):
        cur = api.whereAmI(state)
        self.prevBuffer.insert(0,cur)
        temp = self.prevBuffer[:8]
        self.prevBuffer = temp



    # def isStuck(self, state):
    #     cur = api.whereAmI(state)
    #     if self.prevBuffer.count(cur) >= 2:
    #         return True
    #     return False

    def isStuck(self, state):
        cur = api.whereAmI(state)
        buf = set()
        for x in self.prevBuffer:
            buf.add(x)
        if len(buf) <= 4:
            self.destuckCtr = 5
            return True
        return False

    def smallestFood(self, state):

        temp = self.food[0]
        for x in self.food:
            if x[0] < temp[0]:
                temp = x
            elif x[0] == temp[0]:
                if x[1] < temp[1]:
                    temp = x
        return temp

    def foodWithin1(self, state):
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))

        for x in range(1,6):
            #South
            if (cur[0], cur[1]-x) in foodAndCapsules:
                return True
            #West
            if (cur[0]-x, cur[1]) in foodAndCapsules:
                return True
            #North
            if (cur[0], cur[1]+x) in foodAndCapsules:
                return True
            #East
            if (cur[0]+x, cur[1]) in foodAndCapsules:
                return True
        return False

    # #assign fake ghost to run away from
    # def destucking(self, state):
    #     cur = api.whereAmI(state)
    #     ghosts = self.escapeBuffer
    #
    #     for x in range(1,6):
    #         #South
    #         if (cur[0], cur[1]-x) in ghosts:
    #             return True
    #         #West
    #         if (cur[0]-x, cur[1]) in ghosts:
    #             return True
    #         #North
    #         if (cur[0], cur[1]+x) in ghosts:
    #             return True
    #         #East
    #         if (cur[0]+x, cur[1]) in ghosts:
    #             return True
    #     return False

    def destucking(self, state):
        if self.destuckCtr > 0:
            self.destuckCtr-=1
            return True
        return False

    def deGhosting(self, state):
        if self.deGhostCtr > 0:
            self.deGhostCtr-=1
            return True
        return False



    def ghostWithin3(self, state):
        cur = api.whereAmI(state)
        ghosts = api.ghosts(state)

        for x in range(1,6):
            #South
            if (cur[0], cur[1]-x) in ghosts:
                self.deGhostCtr = 2
                return True
            #West
            if (cur[0]-x, cur[1]) in ghosts:
                self.deGhostCtr = 2
                return True
            #North
            if (cur[0], cur[1]+x) in ghosts:
                self.deGhostCtr = 2
                return True
            #East
            if (cur[0]+x, cur[1]) in ghosts:
                self.deGhostCtr = 2
                return True
        return False

    def runFromGhost(self, state):
        self.update(state)

        print "Running from ghosts"

        cur = api.whereAmI(state)
        ghosts = api.ghosts(state)
        legal = api.legalActions(state)
        legal.remove(Directions.STOP)

        for x in range(1,4):
            #South
            if (cur[0], cur[1]-x) in ghosts:
                if Directions.SOUTH in legal:
                    if len(legal) > 1: legal.remove(Directions.SOUTH)
                    self.last = random.choice(legal)
                    return self.last
            #West
            if (cur[0]-x, cur[1]) in ghosts:
                if Directions.WEST in legal:
                    if len(legal) > 1: legal.remove(Directions.WEST)
                    self.last = random.choice(legal)
                    return self.last
            #North
            if (cur[0], cur[1]+x) in ghosts:
                if Directions.NORTH in legal:
                    if len(legal) > 1: legal.remove(Directions.NORTH)
                    self.last = random.choice(legal)
                    return self.last
            #East
            if (cur[0]+x, cur[1]) in ghosts:
                if Directions.EAST in legal:
                    if len(legal) > 1: legal.remove(Directions.EAST)
                    self.last = random.choice(legal)
                    return self.last


        self.last = random.choice(legal)
        return self.last

    def assignEscapeBuffer(self, state):
        if choice == Directions.NORTH:
            self.escapeBuffer = [(cur[0], cur[1]+1)]
        elif choice == Directions.EAST:
            self.escapeBuffer = [(cur[0]+1, cur[1])]
        elif choice == Directions.SOUTH:
            self.escapeBuffer = [(cur[0], cur[1]-1)]
        elif choice == Directions.WEST:
            self.escapeBuffer = [(cur[0]+1, cur[1])]

    # #places a ghost near pacman to get pacman to ru away from stuck position
    # def deStuck(self, state):
    #     self.update(state)
    #
    #     cur = api.whereAmI(state)
    #     legal = api.legalActions(state)
    #     legal.remove(Directions.STOP)
    #     choice = random.choice(legal)
    #
    #     legal = api.legalActions(state)
    #     legal.remove(Directions.STOP)
    #
    #     for x in range(1,4):
    #         #South
    #         if (cur[0], cur[1]-x) in self.escapeBuffer:
    #             print "ghost south"
    #             if Directions.SOUTH in legal:
    #                 if len(legal) > 1: legal.remove(Directions.SOUTH)
    #                 self.last = random.choice(legal)
    #                 print "going ", self.last
    #                 return self.last
    #         #West
    #         if (cur[0]-x, cur[1]) in self.escapeBuffer:
    #             print "ghost west"
    #             if Directions.WEST in legal:
    #                 if len(legal) > 1: legal.remove(Directions.WEST)
    #                 self.last = random.choice(legal)
    #                 print "going ", self.last
    #                 return self.last
    #         #North
    #         if (cur[0], cur[1]+x) in self.escapeBuffer:
    #             print "ghost north"
    #             if Directions.NORTH in legal:
    #                 if len(legal) > 1: legal.remove(Directions.NORTH)
    #                 self.last = random.choice(legal)
    #                 print "going ", self.last
    #                 return self.last
    #         #East
    #         if (cur[0]+x, cur[1]) in self.escapeBuffer:
    #             print "ghost east"
    #             if Directions.EAST in legal:
    #                 if len(legal) > 1: legal.remove(Directions.EAST)
    #                 self.last = random.choice(legal)
    #                 print "going ", self.last
    #                 return self.last
    #
    #
    #     self.last = random.choice(legal)
    #     print "going ", self.last
    #     return self.last


    # #goes towards southwest corner untill unstuck
    # def deStuck(self, state):
    #     self.update(state)
    #
    #     cur = api.whereAmI(state)
    #     legal = api.legalActions(state)
    #     legal.remove(Directions.STOP)
    #
    #     if Directions.WEST in legal:
    #         print "UNSTICKING BY GOING WESTTTTT"
    #         self.last = Directions.WEST
    #         return self.last
    #     if Directions.SOUTH in legal:
    #         print "UNSTICKING BY GOING SOUTHHHH"
    #         self.last = Directions.SOUTH
    #         return self.last
    #     if self.last in legal:
    #         print "UNSTICKING BY GOING STRAIGHTTTT"
    #         return self.last
    #
    #     legal.remove(self.oppositeDirection(state, self.last))
    #     self.last = random.choice(legal)
    #     print "UNSTICKING BY GOING RANDOMMMM"
    #     return self.last

    #deStucks by going straight
    def deStuck(self, state):
        self.update(state)

        print "Getting unstuck"


        cur = api.whereAmI(state)
        legal = api.legalActions(state)
        legal.remove(Directions.STOP)
        if len(legal) > 1:
            if self.oppositeDirection(state, self.last) in legal:
                legal.remove(self.oppositeDirection(state, self.last))
        if self.last in legal:
            return self.last
        self.last = random.choice(legal)
        return self.last

    #deGhosts by going straight
    def deGhost(self, state):
        self.update(state)

        print "Avoiding ghosts"

        cur = api.whereAmI(state)
        legal = api.legalActions(state)
        legal.remove(Directions.STOP)
        if len(legal) > 1:
            legal.remove(self.oppositeDirection(state, self.last))
        if self.last in legal:
            return self.last
        self.last = random.choice(legal)
        return self.last



    ## finds cloests food by manhattan distance ignoring walls
    # def closestFoodIs(self, state):
    #     self.update(state)
    #
    #     cur = api.whereAmI(state)
    #     closest = self.food[0]
    #
    #     temp1 = closest[0] - cur[0]
    #     if temp1 < 0: temp1 = temp1*-1
    #     temp2 = closest[1] - cur[1]
    #     if temp2 < 0: temp2 = temp2*-1
    #     closestDistance = temp1+temp2
    #
    #     for i in self.food:
    #         x = i[0] - cur[0]
    #         if x < 0: x = x*-1
    #         y = i[1] - cur[1]
    #         if y < 0: y = y*-1
    #         distance = x+y
    #
    #         if distance < closestDistance:
    #             closest = i
    #     return closest

    #finds colest food by readth first search, taking into account walls
    def closestFoodIs(self, state):

        cur = api.whereAmI(state)
        queue = [cur]
        visitedd = [cur]

        while queue:
            if queue[0] in self.food:
                return queue[0]
            else:
                front = queue[0]
                queue.pop(0)
                for x in self.possibleMoves(state, front):
                    if x not in visitedd:
                        visitedd.append(x)
                        queue.append(x)





    #go to closest food
    def goTowardsClosestFood(self, state):
        self.update(state)

        print "Seeking closest food"

        cur = api.whereAmI(state)
        coord = self.closestFoodIs(state)
        # print coord
        legal = api.legalActions(state)

        #if southwest
        if coord[0] < cur[0] and coord[1] < cur[1]:
            self.last = self.goTowardsSmallestFood(state)
            return self.last
            if Directions.SOUTH in legal and Directions.WEST in legal:
                self.last = random.choice([Directions.SOUTH, Directions.WEST])
                return self.last

        #if northwest
        if coord[0] < cur[0] and coord[1] > cur[1]:
            self.last = self.goTowardsSmallestFood(state)
            return self.last
            if Directions.NORTH in legal and Directions.WEST in legal:
                self.last = random.choice([Directions.NORTH, Directions.WEST])
                return self.last
        #if northeast
        if coord[0] > cur[0] and coord[1] > cur[1]:
            self.last = self.goTowardsSmallestFood(state)
            return self.last
            if Directions.NORTH in legal and Directions.EAST in legal:
                self.last = random.choice([Directions.NORTH, Directions.EAST])
                return self.last
        #if southeast
        if coord[0] > cur[0] and coord[1] < cur[1]:
            self.last = self.goTowardsSmallestFood(state)
            return self.last
            if Directions.SOUTH in legal and Directions.EAST in legal:
                self.last = random.choice([Directions.SOUTH, Directions.EAST])
                return self.last

        #if West
        if coord[0] < cur[0]:
            #if wall inbetween food and cur
            if (cur[0]-1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    self.last = Directions.NORTH
                    return self.last
                if Directions.SOUTH in api.walls(state):
                    self.last = Directions.SOUTH
                    return self.last
            if Directions.WEST in legal:
                self.last = Directions.WEST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                return self.last

        #if East
        if coord[0] > cur[0]:
            #if wall inbetween food and cur
            if (cur[0]+1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    self.last = Directions.NORTH
                    return self.last
                if Directions.SOUTH in api.walls(state):
                    self.last = Directions.SOUTH
                    return self.last
            if Directions.EAST in legal:
                self.last = Directions.EAST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                return self.last

        #if South
        if coord[1] < cur[1]:

            #if wall inbetween food and cur
            if (cur[0], cur[1]-1) in api.walls(state):
                if Directions.WEST in legal:
                    self.last = Directions.WEST
                    return self.last
                if Directions.EAST in api.walls(state):
                    self.last = Directions.EAST
                    return self.last
            if Directions.SOUTH in legal:
                self.last = Directions.SOUTH
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                return self.last

        #if North
        if coord[1] > cur[1]:

            #if wall inbetween food and cur
            if (cur[0], cur[1]+1) in api.walls(state):
                if Directions.WEST in legal:
                    self.last = Directions.WEST
                    return self.last
                if Directions.EAST in api.walls(state):
                    self.last = Directions.EAST
                    return self.last
            if Directions.NORTH in legal:
                self.last = Directions.NORTH
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                return self.last

        legal.remove(Directions.STOP)
        if len(legal) > 1:
            legal.remove(self.oppositeDirection(state, self.last))
        self.last = random.choice(legal)
        return self.last

    #return left coord of direction passed as param
    def leftCoordOf(self, state, coord, dir):
        if dir == Directions.NORTH:
            return (coord[0]-1, coord[1])
        if dir == Directions.SOUTH:
            return (coord[0]+1, coord[1])
        if dir == Directions.EAST:
            return (coord[0], coord[1]+1)
        if dir == Directions.WEST:
            return (coord[0], coord[1]-1)

    #return left direction of direction passed as param
    def leftDirOf(self, state, dir):
        if dir == Directions.NORTH:
            return Directions.WEST
        if dir == Directions.SOUTH:
            return Directions.EAST
        if dir == Directions.EAST:
            return Directions.NORTH
        if dir == Directions.WEST:
            return Directions.SOUTH



    ## follow close by food, if multiple food, choose leftmost
    def followFood(self, state):
        print "Following adjacent food"
        self.update(state)
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))


        for x in range(1,6):

            #if left available, go left
            if self.leftCoordOf(state, cur, self.last) in foodAndCapsules:
                if self.leftDirOf(state, self.last) in api.legalActions(state):
                    self.last = self.leftDirOf(state, self.last)
                    return self.last


            #South
            if (cur[0], cur[1]-x) in foodAndCapsules:
                self.last = Directions.SOUTH
                return self.last
            #West
            if (cur[0]-x, cur[1]) in foodAndCapsules:
                self.last = Directions.WEST
                return self.last
            #North
            if (cur[0], cur[1]+x) in foodAndCapsules:
                self.last = Directions.NORTH
                return self.last
            #East
            if (cur[0]+x, cur[1]) in foodAndCapsules:
                self.last = Directions.EAST
                return self.last

    #go to smallest food
    def goTowardsSmallestFood(self, state):
        self.update(state)

        print "Seeking smallest food"

        cur = api.whereAmI(state)
        coord = self.smallestFood(state)
        legal = api.legalActions(state)

        #if West
        if coord[0] < cur[0]:
            #if wall inbetween food and cur
            if (cur[0]-1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    self.last = Directions.NORTH
                    return self.last
                if Directions.SOUTH in api.walls(state):
                    self.last = Directions.WEST
                    return self.last
            if Directions.WEST in legal:
                self.last = Directions.WEST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if East
        if coord[0] > cur[0]:
            #if wall inbetween food and cur
            if (cur[0]+1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    self.last = Directions.NORTH
                    return self.last
                if Directions.SOUTH in api.walls(state):
                    self.last = Directions.SOUTH
                    return self.last
            if Directions.EAST in legal:
                self.last = Directions.EAST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if North
        if coord[1] > cur[1]:
            #if wall inbetween food and cur
            if (cur[0], cur[1]+1) in api.walls(state):
                if Directions.EAST in legal:
                    self.last = Directions.EAST
                    return self.last
                if Directions.WEST in api.walls(state):
                    self.last = Directions.WEST
                    return self.last
            if Directions.NORTH in legal:
                self.last = Directions.NORTH
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if South
        if coord[1] < cur[1]:

            #if wall inbetween food and cur
            if (cur[0], cur[1]-1) in api.walls(state):
                if Directions.EAST in legal:
                    self.last = Directions.EAST
                    return self.last
                if Directions.WEST in api.walls(state):
                    self.last = Directions.WEST
                    return self.last
            if Directions.SOUTH in legal:
                self.last = Directions.SOUTH
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last




    def possibleMoves(self,state, pos):
        walls = api.walls(state)
        moves = []

        #south
        if (pos[0], pos[1]-1) not in walls:
            moves.append((pos[0], pos[1]-1))
        #west
        if (pos[0]-1, pos[1]) not in walls:
            moves.append((pos[0]-1, pos[1]))
        #north
        if (pos[0], pos[1]+1) not in walls:
            moves.append((pos[0], pos[1]+1))
        #east
        if (pos[0]+1, pos[1]) not in walls:
            moves.append((pos[0]+1, pos[1]))

        return moves


    # #depth first search
    # def pathToSmallestFood(self,state, path):
    #     target = [self.smallestFood(state)]
    #
    #
    #     if len(path) > 0:
    #
    #         if path[-1] in target:
    #             print "path found"
    #             return path
    #         else:
    #             for x in self.possibleMoves(state, path[-1]):
    #                 print "possible moves : ", self.possibleMoves(state, path[-1])
    #                 print "looking at : ", x
    #
    #                 if x not in self.visited:
    #                     # print x
    #                     path.append(x)
    #                     self.visited.append(x)
    #                     return self.pathToSmallestFood(state, path)
    #             print "dead end"
    #             print "failed path : ", path
    #
    #             self.visited.append(path[-1])
    #             path.remove(path[-1])
    #             return self.pathTosmallestFood(state, path)
    #     print "No paths found"
    #     print "##############"


    def oppositeDirection(self, state, dir):
        if dir == Directions.NORTH: return Directions.SOUTH
        if dir == Directions.SOUTH: return Directions.NORTH
        if dir == Directions.EAST: return Directions.WEST
        if dir == Directions.WEST: return Directions.EAST

    def randomDirection(self, state):
        moves = api.legalActions(state)
        moves.remove(Directions.STOP)
        if len(moves > 1): moves.remove(self.oppositeDirection(state, self.last))
        self.last = moves.random.choice(moves)
        return self.last

    def randomlyTraverse(self, state):
        self.update(state)

        print "Randomly traversing"

        legal = api.legalActions(state)
        legal.remove(Directions.STOP)
        #avoid backtracking if possible
        if len(legal) > 1:
            if self.oppositeDirection(state, self.last) in legal:
                legal.remove(self.oppositeDirection(state, self.last))
        return random.choice(legal)
















    ###
