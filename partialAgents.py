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



    # This is what gets run in between multiple games
    def final(self, state):
        self.visited = []
        self.food = []
        self.last = Directions.STOP
        print " __________________"
        print "|                  |"
        print "|    Game Over!    |"
        print "|                  |"
        print " ------------------"


    def getAction(self, state):
        self.update(state)

        #go to adjacent food
        if self.foodWithin1(state):
            return self.followFood(state)

        # go to closest food
        if self.foodSeen(state):
            return self.goTowardsClosestFood(state)


        # # map to lowest food
        # if self.foodSeen(state):
        #     # print "path to smallest food : ", self.pathToSmallestFood(state, [api.whereAmI(state)])
        #     # return self.goToSmallestFood
        #     return self.seekFood(state)

        return Directions.STOP


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

    def smallestFood(self, state):

        temp = self.food[0]
        for x in self.food:
            if x[0] < temp[0]:
                temp = x
            elif x[0] == temp[0]:
                if x[1] < temp[1]:
                    temp = x
        print "smallest is ", temp
        return temp
        print "no food on map"

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

    def closestFoodIs(self, state):
        self.update(state)

        cur = api.whereAmI(state)
        closest = self.food[0]

        temp1 = closest[0] - cur[0]
        if temp1 < 0: temp1 = temp1*-1
        temp2 = closest[1] - cur[1]
        if temp2 < 0: temp2 = temp2*-1
        closestDistance = temp1+temp2

        for i in self.food:
            x = i[0] - cur[0]
            if x < 0: x = x*-1
            y = i[1] - cur[1]
            if y < 0: y = y*-1
            distance = x+y

            if distance < closestDistance:
                closest = i
        return closest





    #go to closest food
    def goTowardsClosestFood(self, state):
        print "--------------------------"

        self.update(state)

        # if foodWithin1

        print "Attemping to go to closest food"
        cur = api.whereAmI(state)
        coord = self.closestFoodIs(state)
        # print coord
        legal = api.legalActions(state)
        print "closest food: ", self.closestFoodIs(state)

        #if southwest
        if coord[0] < cur[0] and coord[1] < cur[1]:
            print "sw"
            return self.goTowardsSmallestFood(state)
            if Directions.SOUTH in legal and Directions.WEST in legal:
                self.last = random.choice([Directions.SOUTH, Directions.WEST])
                return self.last

        #if northwest
        if coord[0] < cur[0] and coord[1] > cur[1]:
            print "nw"
            return self.goTowardsSmallestFood(state)
            if Directions.NORTH in legal and Directions.WEST in legal:
                self.last = random.choice([Directions.NORTH, Directions.WEST])
                return self.last
        #if northeast
        if coord[0] > cur[0] and coord[1] > cur[1]:
            print "ne"
            return self.goTowardsSmallestFood(state)
            if Directions.NORTH in legal and Directions.EAST in legal:
                self.last = random.choice([Directions.NORTH, Directions.EAST])
                return self.last
        #if southeast
        if coord[0] > cur[0] and coord[1] < cur[1]:
            print "se"
            return self.goTowardsSmallestFood(state)
            if Directions.SOUTH in legal and Directions.EAST in legal:
                self.last = random.choice([Directions.SOUTH, Directions.EAST])
                return self.last

        #if West
        if coord[0] < cur[0]:
            print "food is west"
            #if wall inbetween food and cur
            if (cur[0]-1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    return Directions.NORTH
                if Directions.SOUTH in api.walls(state):
                    return Directions.SOUTH
            if Directions.WEST in legal:
                self.last = Directions.WEST
                print "going west"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                print "going random direction: ", self.last
                return self.last

        #if East
        if coord[0] > cur[0]:
            print "food is east"
            #if wall inbetween food and cur
            if (cur[0]+1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    return Directions.NORTH
                if Directions.SOUTH in api.walls(state):
                    return Directions.SOUTH
            if Directions.EAST in legal:
                self.last = Directions.EAST
                print "going east"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                print "going random direction: ", self.last
                return self.last

        #if South
        if coord[1] < cur[1]:
            print "food is south"
            #if wall inbetween food and cur
            if (cur[0], cur[1]-1) in api.walls(state):
                if Directions.WEST in legal:
                    return Directions.WEST
                if Directions.EAST in api.walls(state):
                    return Directions.EAST
            if Directions.SOUTH in legal:
                self.last = Directions.SOUTH
                print "going south"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                print "going random direction: ", self.last
                return self.last

        #if North
        if coord[1] > cur[1]:
            print "food is north"
            #if wall inbetween food and cur
            if (cur[0], cur[1]+1) in api.walls(state):
                if Directions.WEST in legal:
                    return Directions.WEST
                if Directions.EAST in api.walls(state):
                    return Directions.EAST
            if Directions.NORTH in legal:
                self.last = Directions.NORTH
                print "going north"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                if len(legal) > 1: legal.remove(self.oppositeDirection(state, self.last))
                self.last = random.choice(legal)
                print "going random direction: ", self.last
                return self.last

        legal.remove(Directions.STOP)
        if len(legal) > 1:
            print "current : ", cur
            print "only 1 option", legal
            legal.remove(self.oppositeDirection(state, self.last))
        self.last = random.choice(legal)
        print "going random direction: ", self.last
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
        print "following adjacent food"
        self.update(state)
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))


        for x in range(1,6):

            #if left available, go left
            if self.leftCoordOf(state, cur, self.last) in foodAndCapsules:
                if self.leftDirOf(state, self.last) in api.legalActions(state):
                    self.last = self.leftDirOf(state, self.last)
                    print "going left"
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
        print "--------------------------"

        self.update(state)


        print "Attemping to go to smallest food"
        cur = api.whereAmI(state)
        coord = self.smallestFood(state)
        # print coord
        legal = api.legalActions(state)
        print "smallest food: ", self.smallestFood(state)

        #if West
        if coord[0] < cur[0]:
            print "food is west"
            #if wall inbetween food and cur
            if (cur[0]-1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    return Directions.NORTH
                if Directions.SOUTH in api.walls(state):
                    return Directions.WEST
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

        #if East
        if coord[0] > cur[0]:
            print "food is east"
            #if wall inbetween food and cur
            if (cur[0]+1, cur[1]) in api.walls(state):
                if Directions.NORTH in legal:
                    return Directions.NORTH
                if Directions.SOUTH in api.walls(state):
                    return Directions.SOUTH
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

        #if North
        if coord[1] > cur[1]:
            print "food is north"
            #if wall inbetween food and cur
            if (cur[0], cur[1]+1) in api.walls(state):
                if Directions.EAST in legal:
                    return Directions.EAST
                if Directions.WEST in api.walls(state):
                    return Directions.WEST
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

        #if South
        if coord[1] < cur[1]:
            print "food is south"
            #if wall inbetween food and cur
            if (cur[0], cur[1]-1) in api.walls(state):
                if Directions.EAST in legal:
                    return Directions.EAST
                if Directions.WEST in api.walls(state):
                    return Directions.WEST
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




    def possibleMoves(self,state, pos):
        walls = api.walls(state)
        moves = []
        if (pos[0]+1, pos[1]) not in walls and (pos[0]+1, pos[1]) not in self.visited:
            moves.append((pos[0]+1, pos[1]))
        if (pos[0]-1, pos[1]) not in walls and (pos[0]-1, pos[1]) not in self.visited:
            moves.append((pos[0]-1, pos[1]))
        if (pos[0], pos[1]+1) not in walls and (pos[0], pos[1]+1) not in self.visited:
            moves.append((pos[0], pos[1]+1))
        if (pos[0], pos[1]-1) not in walls and (pos[0], pos[1]-1) not in self.visited:
            moves.append((pos[0], pos[1]-1))
        return moves


    #depth first search
    def pathToSmallestFood(self,state, path):
        target = [self.smallestFood(state)]

        print "-----"
        if len(path) > 0:
            print "cur : ", path[-1]
            print "-----"

            if path[-1] in target:
                print "path found"
                return path
            else:
                for x in self.possibleMoves(state, path[-1]):
                    print "possible moves : ", self.possibleMoves(state, path[-1])
                    print "looking at : ", x

                    if x not in self.visited:
                        # print x
                        path.append(x)
                        self.visited.append(x)
                        return self.pathToSmallestFood(state, path)
                print "dead end"
                print "failed path : ", path

                self.visited.append(path[-1])
                path.remove(path[-1])
                return self.pathTosmallestFood(state, path)
        print "No paths found"
        print "##############"

    # def seekFood(self, state):


    def oppositeDirection(self, state, dir):
        if dir == Directions.NORTH: return Directions.SOUTH
        if dir == Directions.SOUTH: return Directions.NORTH
        if dir == Directions.EAST: return Directions.WEST
        if dir == Directions.WEST: return Directions.EAST
















    ###
