import json
from sim import Simulator, Interface



# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.predicted_actions = []
        self.interface = Interface()

    def ids(self, start_s):
        i = 1
        while(True):
            result = self.ldfs(start_s, i)
            if result != "CUTOFF":
                return result
            i = i + 1

    def ldfs(self, start_s, limit = 1):
        frontier = [[start_s, []]]
        result = "FAILURE"
        while(len(frontier) > 0):
            node = frontier.pop(-1)
            if(self.interface.goal_test(node[0])):
                return node[1]
            if(len(node[1]) > limit):
                result = "CUTOFF"
            for act in self.interface.valid_actions(node[0],[]):
                lst = node[1].copy()
                lst.append(act)
                frontier.append([Simulator(node[0].coordinates, node[0].stick_together), lst])
        return result
    
    def a_star(self, start_s, heuristic):
        frontier = list()
        frontier.append([start_s, 0, []])
        while (len(frontier) > 0):
            frontier = sorted(frontier, key=lambda x:x[1])
            node = frontier.pop(0)
            if(self.interface.goal_test(node[0])):
                return node[2]
            for act in self.interface.valid_actions(node[0]):
                frontier.put([Simulator(node[0].coordinates.copy(),node[0].stick_together), len(node[0][2]) + 1 + heuristic(node[0]), node[2].append[act]])
        return "FAILURE"

    # the act function takes a json string as input
    # and outputs an action string
    # action example: [1,2,-2]
    # the first number is the joint number (1: the first joint)
    # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
    # the third number is the degree (1: 90 degree, -2: -180 degree, -1000: -90000 degree)
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***
        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        # TODO implement your agent here
        alg = self.ids
        if self.predicted_actions == []:
            initial_state=Simulator(sensor_data['coordinates'], sensor_data['stick_together'])
            self.predicted_actions = alg(initial_state)
        
        action = self.predicted_actions.pop()

        # action example: [1,2,-2]
        return action
