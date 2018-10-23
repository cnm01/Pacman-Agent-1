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

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like I just died!"


    def getAction(self, state):
        self.start(state)
        # print self.food

        #traverse exteriors walls
        if self.stage1 == True:
            if api.whereAmI(state) not in self.visited:
                return self.traverseExterior(state)
        self.stage1 = False
        #reached starting point

        self.update(state)

        # #go towards nearest food
        # if self.foodWithin1(state):
        #     return self.followFood(state)
        #
        return self.goTowardsNearestFood(state)

        print self.smallest(state)
        # print self.nearestFoodPath(state, [api.whereAmI(state)])
        # print self.nearestFood(state, api.whereAmI(state))

        # print self.nearestFood(state)

        return Directions.STOP


    def start(self, state):
        if self.last == Directions.STOP:
            if Directions.WEST in api.legalActions(state):
                self.last = Directions.WEST
                return self.last
            self.last = random.choice(api.legalActions(state).remove(Directions.STOP))
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

    #return coords of nearest food
    # def nearestFood(self, state):
    #     cur = api.whereAmI(state)
    #     lowest = self.food[0]
    #     for f in self.food:
    #         x = cur[0] - f[0]
    #         if x < 0:
    #             x = x*-1
    #         y = cur[1] - f[1]
    #         if y < 0:
    #             y = y*-1
    #         if x+y < lowest[0]+lowest[1]:
    #             lowest = f
    #     return f


    # def nearestFood(self, state, pos):
    #     print "current pos: ", pos
    #     if pos in self.food:
    #         print "food found in ", pos
    #         return pos
    #     else:
    #         for x in self.possibleMoves(state, pos):
    #             print "calling nearestFood() on possible move of ", pos, " which is :", x
    #             return self.nearestFood(state, x)

    #returns coordinate of westmost/southmost food
    def smallest(self, state):
        temp = self.food[0]
        for x in self.food:
            if x[0] < temp[0]:
                temp = x
            elif x[0] == temp[0]:
                if x[1] < temp[1]:
                    temp = x
        print "smallest is ", temp
        return temp

    # def goToSmallest(self, state):




    def nearestFoodPath(self, state, path):
        if path[-1] in self.food:
            return path
        else:
            for x in self.possibleMoves(state, path[-1]):
                return self.nearestFoodPath(state, path.append(x))


    #pass current position as array containing 1 element
    # def pathToFood(self, state, path):
    #     if path[len(path)-1] in self.food:
    #         return path
    #     else:
    #         for x in self.possibleMoves(state, path[len(path)-1]):
    #             self.pathToFood(state, path.append(x))


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

    #go to nearest food
    def goTowardsNearestFood(self, state):
        print "Attemping to go to smallest food"
        self.update(state)
        cur = api.whereAmI(state)
        coord = self.smallest(state)
        print coord
        legal = api.legalActions(state)
        # print self.nearestFood(state)

        #if North
        if coord[1] > cur[1]:
            print "food is north"
            if Directions.NORTH in legal:
                self.last = Directions.NORTH
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if East
        if coord[0] > cur[0]:
            print "food is east"
            if Directions.EAST in legal:
                self.last = Directions.EAST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if South
        if coord[1] < cur[1]:
            print "food is south"
            if Directions.SOUTH in legal:
                print "south legal, going south"
                self.last = Directions.SOUTH
                return self.last
            elif self.last in legal:
                print "south not legal, going straight"
                return self.last
            else:
                print "south not legal, straight not legal, random choice"
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last

        #if West
        if coord[0] < cur[0]:
            print "food is west"
            if Directions.WEST in legal:
                self.last = Directions.WEST
                return self.last
            elif self.last in legal:
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                return self.last


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
