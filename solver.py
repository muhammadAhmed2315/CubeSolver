from cube import *

class IDA_star():
    def __init__(self, heuristic, max_depth = 20):
        """
        heuristic is a dictionary representing the pre computed pattern database
        max_depth is an integer representing the max depth the game tree reaches (20 = God's Number)
        """
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        self.heuristic = heuristic
        self.moves = []

    def run(self, state):
        """
        Solves the cube, returning a list containing the number of moves taken to solve
        the cube
        """
        while True:
            status = self.search(state, 1)
            if status: return self.moves
            self.moves = []
            self.threshold = self.min_threshold
    
    def search(self, state, g_score):
        """
        Searches the game tree using the IDA* algorithm
        g_score is an integer representing the cost to reach the current node
        Returns a boolean indicating if the cube has been solved
        """
        cube = Cube(state=state)
        if cube.state in cube.goal:
            return True
        elif len(self.moves) >= self.threshold:
            return False
        min_val = float('inf')
        best_action = None
        next_action = None

        if next_action is not None:
            temp = next_action
        else:
            temp = best_action

        # look at neighbours of current node
        for a, configuration in cube.neighbors(cube.state):
            # if neighbor is solved, add move and return True
            if configuration in cube.goal:
                self.moves.append(a)
                return True
            cube_str = configuration
            # heuristic score is the heuristic_db value else self.max_depth
            h_score = self.heuristic[cube_str] if cube_str in self.heuristic else self.max_depth
            # final score = g_score + h_score
            f_score = g_score + h_score
            # if f_score < current min_val, we have a new min_value, and best action to take
            if f_score < min_val:
                min_val = f_score
                best_action = [(cube_str, a)]
            # if f_score == min_val but there is not current best action, initialise best action
            elif f_score == min_val:
                if best_action is None:
                    best_action = [(cube_str, a)]
            # otherwise append new configuration to best action as well so we have mutltiple possible
            # best moves we could now take
                else:
                    best_action.append((cube_str, a))
            # if there is a best_action
        if best_action is not None:
            if self.min_threshold is None or min_val < self.min_threshold:
                self.min_threshold = min_val
            next_action = random.choice(best_action)
            self.moves.append(next_action[1])
            status = self.search(next_action[0], g_score + min_val)
            if status: return status
        return False
