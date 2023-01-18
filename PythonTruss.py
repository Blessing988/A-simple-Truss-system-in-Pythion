#Importing relevant libraries and functions
import matplotlib.pyplot as plt
from numpy import sqrt, transpose, linalg, array, dot
import numpy
numpy.set_printoptions(3, suppress=True)

#Creating a Node class
class Node(object):
    total_nodes = {}       #A dictionary which houses all the nodes
    directionCosines = {}  #A dictionary which houses the direction cosines
    Reactions = {}         # A dictionary which holds all the reactions
    total_members = {}     # A dictionary which holds all the members
    numJoint = 0           # Initiating the number of joints

    def __init__(self, id, x, y, sy=0,sx=0,fx=0,fy=0):


        self.id = id
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.fx = fx
        self.fy = fy
        Node.numJoint += 1
        Node.total_nodes[self.id] = (self.x, self.y, self.sy, self.sx, self.fx,self.fy)
        Node.Reactions[self.id] = (self.sy, self.sx)

#Creating a Member class
class Member(object):

    def __init__(self, id , start, end, A = 1, E = 1):
        self.id = id
        self.start = start
        self.end = end
        self.A = A
        self.E = E

        x1 = start.x
        x2 = end.x
        y1 = start.y
        y2 = end.y
        
        #Calculating the length of a member
        self.length = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        #Calculating direction cosines in each member
        self.cosStart = (x2 - x1)/self.length
        self.sinStart = (y2 - y1)/self.length
        self.cosEnd = (x1 - x2)/self.length
        self.sinEnd = (y1 - y2)/self.length

        #Adding each member and its direction cosine to the directionCosine dictionary
        Node.directionCosines[self.id] = (self.cosStart, self.sinStart, self.cosEnd, self.sinEnd)
        #Adding each member and its start and end to the total_members dictionary
        Node.total_members[self.id] = (self.start.id, self.end.id, self.A, self.E)

#Creating Analysis class
class Analysis:
    """
    This class solves the truss by the generating the Total Equilibrium Matrix
    It also has a function which plots the truss
    """
    Matrix = [] #This would contain the loads each Node
    Equilibrium_Matrix = [] # A matrix of total directionCosines


    def calculate(self):
        """
        This calculates all the forces in each member and also the reactions at each support
        :return: The total Equilibrium Matrix consisting of the direction cosines of both the forces and the reactions
        """

        ####### Code which appends all the loads at the joints to the Matrix list#######
        for i in Node.total_nodes.keys():
            for j in Node.total_nodes[i][-2:]:
                Analysis.Matrix.append([-j])

        #Appending the directionCosines of the Members to the Equilibrium Matrix
        for i in Node.total_members.keys():
            Equilibrium = []
            for j in Node.total_nodes.keys():
                if j == Node.total_members[i][0]:
                    for v in Node.directionCosines[i][:2]:
                        Equilibrium.append(v)
                elif j == Node.total_members[i][1]:
                    for v in Node.directionCosines[i][-2:]:
                        Equilibrium.append(v)
                else:
                    for v in Node.directionCosines[i][:2]:
                        Equilibrium.append(0)
            Analysis.Equilibrium_Matrix.append(Equilibrium)


        ####### Generating the ReactionCosines for the Vertical Reactions ###########
        for i in Node.Reactions.keys():
            ReactionMatrix = []
            for j in Node.total_nodes.keys():
                R = []
                if i == j and Node.Reactions[i] != (0, 0):
                    v = Node.Reactions[i][0]
                    vb = [0, v]
                    for j in vb:
                        R.append(j)
                elif i != j and Node.Reactions[i] != (0, 0):
                    vb = [0, 0]
                    for j in vb:
                        R.append(j)
                for j in R:
                    ReactionMatrix.append(j)
                else:
                    continue
            if Node.Reactions[i] != (0, 0):
                Analysis.Equilibrium_Matrix.append(ReactionMatrix)
            else:
                continue

        ####### Generating the directionCosines(reaction cosines) for the horizontal reactions
        for i in Node.Reactions.keys():
            ReactionMatrix = []
            for j in Node.total_nodes.keys():
                R = []
                if i == j and Node.Reactions[i] != (0, 0) and Node.Reactions[i][1] != 0:
                    v = Node.Reactions[i][0]
                    vb = [v, 0]
                    for j in vb:
                        R.append(j)
                elif i != j and Node.Reactions[i] != (0, 0) and Node.Reactions[i][1] != 0:
                    vb = [0, 0]
                    for j in vb:
                        R.append(j)
                for j in R:
                    ReactionMatrix.append(j)
                else:
                    continue
            if Node.Reactions[i] != (0, 0) and Node.Reactions[i][1] != 0 :
                Analysis.Equilibrium_Matrix.append(ReactionMatrix)
            else:
                continue

        # Making Calculations
        Total_Eq_Matrix = transpose(Analysis.Equilibrium_Matrix)
        inverse = linalg.inv(Total_Eq_Matrix)
        P = array(Analysis.Matrix)
        result = inverse.dot(P)
        print(result)

    def plot(self):
        """
        This function takes the coordinates(x and y coordinates) of the nodes and the members to plot the truss
        :return: Plots the truss
        """

        for i in Node.total_members.keys():
            M = Node.total_members[i]
            x1 = Node.total_nodes[M[0]][0]
            x2 = Node.total_nodes[M[0]][1]
            y1 = Node.total_nodes[M[1]][0]
            y2 = Node.total_nodes[M[1]][1]
            plt.plot([x1, y1], [x2, y2], "ko")
            plt.plot([x1, y1], [x2, y2])
        plt.show()
