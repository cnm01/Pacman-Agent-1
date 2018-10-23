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
        self.last = Directions.STOP
        self.visited = []
        self.food = []
        self.stage1 = True
        self.startPos = None
        self.startDir = None
        self.counter = 0


    # This is what gets run in between multiple games
    def final(self, state):
        print "Game Over!"


    def getAction(self, state):
        self.counter+=1
        # print "Move: ", self.counter

        if self.isStarting(state) == True:
            # print "running start()----------------"
            return self.start(state)

        # print "start pos is: ", self.startPos
        # print "current pos is: ", api.whereAmI(state)

        # print "cur != startPos : ", api.whereAmI(state) != self.startPos
        # print "self.last != startDir : ", self.last != self.startDir
        # print "cur == startPos --------------- : ", api.whereAmI(state) == self.startPos
        # print "self.last == startDir  -----------------: ", self.last == self.startDir

        #traverse exteriors walls
        ############################assuming start on exterior wall, not in corner
        #traverses exterior walls until it reaches start point, and faces same dir it started at that point
        if self.stage1 == True:
            if api.whereAmI(state) != self.startPos:
                print "traversing exterior"
                print "--------------------------"
                return self.traverseExterior(state)
            elif api.whereAmI(state) == self.startPos and self.last == self.startDir:
                # print "EXITING STAGE 1------------------------"
                self.stage1 = False
        #reached starting point

        self.update(state)

        #go to smallest coordinate food on map (westmost then southmost)
        #if no food on map, traverse exterior(?)
        ###################assumes food will be found eventually when traversing exterior
        return self.goTowardsSmallestFood(state)

        # print self.smallest(state)

        return Directions.STOP

    def isStarting(self, state):
        if self.counter <= 1:
            return True
        else:
            return False


    def start(self, state):

        if self.last ==Directions.STOP:
            self.startPos = api.whereAmI(state)
            # print "Starting()"
            if Directions.WEST in api.legalActions(state):
                self.last = Directions.WEST
                self.startDir = self.last
                # print "start: west"
                return self.last
            elif Directions.EAST in api.legalActions(state):
                self.last = Directions.EAST
                self.startDir = self.last
                # print "start: east"
                return self.last
            elif Directions.SOUTH in api.legalActions(state):
                self.last = Directions.SOUTH
                self.startDir = self.last
                # print "start: south"
                return self.last
            else:
                self.last = Directions.NORTH
                self.startDir = self.last
                # print "start: north"
                return self.last

    def traverseExterior(self, state):
        self.update(state)

        if Directions.LEFT[self.last] in api.legalActions(state):
            self.last = Directions.LEFT[self.last]
            return self.last
        if self.last in api.legalActions(state):
            self.last = self.last
            return self.last
        if Directions.RIGHT[self.last] in api.legalActions(state):
            self.last = Directions.RIGHT[self.last]
            return self.last
        if Directions.LEFT[Directions.LEFT[self.last]] in api.legalActions(state):
            self.last = Directions.LEFT[Directions.LEFT[self.last]]
            return self.last


    #returns coordinate of westmost/southmost food
    def smallest(self, state):
        if len(self.food) > 0:
            temp = self.food[0]
            for x in self.food:
                if x[0] < temp[0]:
                    temp = x
                elif x[0] == temp[0]:
                    if x[1] < temp[1]:
                        temp = x
            # print "smallest is ", temp
            return temp
        print "no food on map"



    def possibleMoves(self, state, pos):
        walls = api.walls(state)
        moves = []
        if (pos[0]+1, pos[1]) not in walls:
            moves.append((pos[0]+1, pos[1]))
        if (pos[0], pos[1]-1) not in walls:
            moves.append((pos[0], pos[1]-1))
        if (pos[0]-1, pos[1]) not in walls:
            moves.append((pos[0]-1, pos[1]))
        if (pos[0], pos[1]+1) not in walls:
            moves.append((pos[0], pos[1]+1))
        return moves

    #go to smallest food
    def goTowardsSmallestFood(self, state):
        print "--------------------------"

        self.update(state)

        if len(self.food) > 0:

            print "Attemping to go to smallest food"
            cur = api.whereAmI(state)
            coord = self.smallest(state)
            # print coord
            legal = api.legalActions(state)
            print "smallest food: ", self.smallest(state)

            #if North
            if coord[1] > cur[1]:
                print "food is north"
                if Directions.NORTH in legal:
                    self.last = Directions.NORTH
                    print "going north"
                    return self.last
                elif self.last in legal:
                    print "going straight"
                    return self.last
                else:
                    legal.remove(Directions.STOP)
                    self.last = random.choice(legal)
                    print "going random direction"
                    return self.last

            #if East
            if coord[0] > cur[0]:
                print "food is east"
                if Directions.EAST in legal:
                    self.last = Directions.EAST
                    print "going east"
                    return self.last
                elif self.last in legal:
                    print "going straight"
                    return self.last
                else:
                    legal.remove(Directions.STOP)
                    self.last = random.choice(legal)
                    "going random direction"
                    return self.last

            #if South
            if coord[1] < cur[1]:
                print "food is south"
                if Directions.SOUTH in legal:
                    self.last = Directions.SOUTH
                    print "going south"
                    return self.last
                elif self.last in legal:
                    print "going straight"
                    return self.last
                else:
                    legal.remove(Directions.STOP)
                    self.last = random.choice(legal)
                    print "going random direction"
                    return self.last

            #if West
            if coord[0] < cur[0]:
                print "food is west"
                if Directions.WEST in legal:
                    self.last = Directions.WEST
                    print "going west"
                    return self.last
                elif self.last in legal:
                    print "going straight"
                    return self.last
                else:
                    legal.remove(Directions.STOP)
                    self.last = random.choice(legal)
                    print "going random direction"
                    return self.last

        print "no food found, traversing exterior"
        return self.traverseExterior(state)


    def followFood(self, state):
        print "following adjacent food"
        self.update(state)
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))


        for x in range(1,6):
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



    def update(self, state):
        self.addFood(state)
        self.updateVisited(state)
        self.removeFood(state)

    def updateVisited(self, state):
        coord = api.whereAmI(state)
        if coord not in self.visited:
            self.visited.append(coord)

    def addFood(self, state):
        for x in api.food(state):
            if x not in self.food:
                self.food.append(x)

    def removeFood(self, state):
        for x in self.food:
            if x in self.visited:
                self.food.remove(x)















































    ###
