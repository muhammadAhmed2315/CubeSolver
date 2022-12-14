from sty import fg
from sty import Style, RgbFg
import random
from tqdm import tqdm

fg.orange = Style(RgbFg(255, 134, 36))
fg.red = Style(RgbFg(255, 0, 0))
fg.green = Style(RgbFg(0, 255, 0))
fg.yellow = Style(RgbFg(255, 255, 0))
fg.white = Style(RgbFg(255, 255, 255))

HEURISTIC_FILE = 'heuristic.json'
REGENERATE_HEURISTIC_DB = False

class Cube():
    def __init__(self, state=None):
        if state:
            self.state = state
        else:
            self.state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        self.goal = [
            'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB', 
            'DDDDDDDDDLLLLLLLLLFFFFFFFFFUUUUUUUUURRRRRRRRRBBBBBBBBB', 
            'FFFFFFFFFUUUUUUUUURRRRRRRRRBBBBBBBBBDDDDDDDDDLLLLLLLLL', 
            'LLLLLLLLLBBBBBBBBBUUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDD', 
            'BBBBBBBBBUUUUUUUUULLLLLLLLLFFFFFFFFFDDDDDDDDDRRRRRRRRR', 
            'LLLLLLLLLFFFFFFFFFDDDDDDDDDRRRRRRRRRBBBBBBBBBUUUUUUUUU', 
            'DDDDDDDDDRRRRRRRRRBBBBBBBBBUUUUUUUUULLLLLLLLLFFFFFFFFF', 
            'RRRRRRRRRBBBBBBBBBDDDDDDDDDLLLLLLLLLFFFFFFFFFUUUUUUUUU', 
            'FFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBBUUUUUUUUURRRRRRRRR', 
            'UUUUUUUUULLLLLLLLLBBBBBBBBBDDDDDDDDDRRRRRRRRRFFFFFFFFF', 
            'BBBBBBBBBDDDDDDDDDRRRRRRRRRFFFFFFFFFUUUUUUUUULLLLLLLLL', 
            'RRRRRRRRRFFFFFFFFFUUUUUUUUULLLLLLLLLBBBBBBBBBDDDDDDDDD'
        ]
        self.solution = None

    def reset(self):
        """Resets cube state to default state"""
        self.state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    def visualise(self):
        """Prints out a 2D visualisation of the net of the cube"""
        colors_dict = {}
        colors_dict["U"] = fg.white + "□" + fg.rs
        colors_dict["F"] = fg.green + "□" + fg.rs
        colors_dict["R"] = fg.red + "□" + fg.rs
        colors_dict["B"] = fg.blue + "□" + fg.rs
        colors_dict["L"] = fg.orange + "□" + fg.rs
        colors_dict["D"] = fg.yellow + "□" + fg.rs

        for i in range(9):
            if i in [0, 3, 6]:
                print("       ", end="")
                print(colors_dict[self.state[i]] + " ", end="")
            elif i in [2, 5, 8]:
                print(colors_dict[self.state[i]] + " ", end="")
                print()
            else:
                print(colors_dict[self.state[i]] + " ", end="")
        print()
        for i in range(3):
            for j in range(3):
                print(colors_dict[self.state[(36 + (i*3)) + j]] + " ", end="")
            print(" ", end="")
            for j in range(3):
                print(colors_dict[self.state[(18 + (i*3)) + j]] + " ", end="")
            print(" ", end="")
            for j in range(3):
                print(colors_dict[self.state[(9 + (i*3)) + j]] + " ", end="")
            print(" ", end="")
            for j in range(3):
                print(colors_dict[self.state[(45 + (i*3)) + j]] + " ", end="")
            print()
        print()
        for i in range(27, 36):
            if i in [27, 30, 33]:
                print("       ", end="")
                print(colors_dict[self.state[i]] + " ", end="")
            elif i in [29, 32, 35]:
                print(colors_dict[self.state[i]] + " ", end="")
                print()
            else:
                print(colors_dict[self.state[i]] + " ", end="")

    def transpose(self, face, direction): # 0 for 90 cc and 1 for 90 acc
        """
        Rotates a face of the cube
        Direction: 0 => rotate 90 degrees clockwise
        Direction: 1 => rotate 90 degrees anticlockwise
        Returns the value of the rotated face
        """
        face = [[face[i] for i in range(3)], 
                [face[i] for i in range(3,6)], 
                [face[i] for i in range(6,9)]]
        if direction == 0:
            face = list(map(list, zip(*face)))
            face[0] = face[0][::-1]
            face[1] = face[1][::-1]
            face[2] = face[2][::-1]
        elif direction == 1:
            face[0] = face[0][::-1]
            face[1] = face[1][::-1]
            face[2] = face[2][::-1]
            face = list(map(list, zip(*face)))
        face = "".join(face[0]) + "".join(face[1]) + "".join(face[2])
        return face

    def U(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = self.transpose(temp[:9], 0) + temp[45:48] + temp[12:18] + temp[9:12] + temp[21:27]
        answer += temp[27:36] + temp[18:21] + temp[39:45] + temp[36:39] + temp[48:54]

        if custom_state: return answer
        else: self.state = answer

    def U_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = self.transpose(temp[:9], 1) + temp[18:21] + temp[12:18] + temp[36:39] + temp[21:27]
        answer += temp[27:36] + temp[45:48] + temp[39:45] + temp[9:12] + temp[48:54]

        if custom_state: return answer
        else: self.state = answer

    def E(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:12] + temp[21:24] + temp[15:21] + temp[39:42] + temp[24:39] + temp[48:51]
        answer += temp[42:48] + temp[12:15] + temp[51:54]

        if custom_state: return answer
        else: self.state = answer

    def E_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:12] + temp[48:51] + temp[15:21] + temp[12:15] + temp[24:39] + temp[21:24]
        answer += temp[42:48] + temp[39:42] + temp[51:54]

        if custom_state: return answer
        else: self.state = answer

    def D(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:15] + temp[24:27] + temp[18:24] + temp[42:45] + self.transpose(temp[27:36], 0)
        answer += temp[36:42] + temp[51:54] + temp[45:51] + temp[15:18]
        
        if custom_state: return answer
        else: self.state = answer

    def D_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:15] + temp[51:54] + temp[18:24] + temp[15:18] + self.transpose(temp[27:36], 1)
        answer += temp[36:42] + temp[24:27] + temp[45:51] + temp[42:45]
        
        if custom_state: return answer
        else: self.state = answer

    def L(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[53] + temp[1:3] + temp[50] + temp[4:6] + temp[47] + temp[7:9] + temp[9:18]
        answer += temp[0] + temp[19:21] + temp[3] + temp[22:24] + temp[6] + temp[25:27]
        answer += temp[18] + temp[28:30] + temp[21] + temp[31:33] + temp[24] + temp[34:36]
        answer += self.transpose(temp[36:45], 0)
        answer += temp[45:47] + temp[33] + temp[48:50] + temp[30] + temp[51:53] + temp[27]
        
        if custom_state: return answer
        else: self.state = answer

    def L_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[18] + temp[1:3] + temp[21] + temp[4:6] + temp[24] + temp[7:9] + temp[9:18]
        answer += temp[27] + temp[19:21] + temp[30] + temp[22:24] + temp[33] + temp[25:27]
        answer += temp[53] + temp[28:30] + temp[50] + temp[31:33] + temp[47] + temp[34:36]
        answer += self.transpose(temp[36:45], 1)
        answer += temp[45:47] + temp[6] + temp[48:50] + temp[3] + temp[51:53] + temp[0]
        
        if custom_state: return answer
        else: self.state = answer

    def M_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[0] + temp[19] + temp[2:4] + temp[22] + temp[5:7] + temp[25] + temp[8]
        answer += temp[9:19] + temp[28] + temp[20:22] + temp[31] + temp[23:25] + temp[34] + temp[26]
        answer += temp[27] + temp[52] + temp[29:31] + temp[49] + temp[32:34] + temp[46] + temp[35]
        answer += temp[36:45]
        answer += temp[45] + temp[7] + temp[47:49] + temp[4] + temp[50:52] + temp[1] + temp[53]
        
        if custom_state: return answer
        else: self.state = answer

    def M(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[0] + temp[52] + temp[2:4] + temp[49] + temp[5:7] + temp[46] + temp[8]
        answer += temp[9:19] + temp[1] + temp[20:22] + temp[4] + temp[23:25] + temp[7] + temp[26]
        answer += temp[27] + temp[19] + temp[29:31] + temp[22] + temp[32:34] + temp[25] + temp[35]
        answer += temp[36:45]
        answer += temp[45] + temp[34] + temp[47:49] + temp[31] + temp[50:52] + temp[28] + temp[53]
        
        if custom_state: return answer
        else: self.state = answer

    def R(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[0:2] + temp[20] + temp[3:5] + temp[23] + temp[6:8] + temp[26]
        answer += self.transpose(temp[9:18], 0)
        answer += temp[18:20] + temp[29] + temp[21:23] + temp[32] + temp[24:26] + temp[35]
        answer += temp[27:29] + temp[51] + temp[30:32] + temp[48] + temp[33:35] + temp[45]
        answer += temp[36:45] + temp[8] + temp[46:48] + temp[5] + temp[49:51] + temp[2] + temp[52:54]
        
        if custom_state: return answer
        else: self.state = answer

    def R_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[0:2] + temp[51] + temp[3:5] + temp[48] + temp[6:8] + temp[45]
        answer += self.transpose(temp[9:18], 1)
        answer += temp[18:20] + temp[2] + temp[21:23] + temp[5] + temp[24:26] + temp[8]
        answer += temp[27:29] + temp[20] + temp[30:32] + temp[23] + temp[33:35] + temp[26]
        answer += temp[36:45] + temp[35] + temp[46:48] + temp[32] + temp[49:51] + temp[29] + temp[52:54]
        
        if custom_state: return answer
        else: self.state = answer

    def B(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[11] + temp[14] + temp[17] + temp[3:9]
        answer += temp[9:11] + temp[35] + temp[12:14] + temp[34] + temp[15:17] + temp[33]
        answer += temp[18:33] + temp[36] + temp[39] + temp[42]
        answer += temp[2] + temp[37:39] + temp[1] + temp[40:42] + temp[0] + temp[43:45]
        answer += self.transpose(temp[45:54], 0)
        
        if custom_state: return answer
        else: self.state = answer

    def B_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[42] + temp[39] + temp[36] + temp[3:9]
        answer += temp[9:11] + temp[0] + temp[12:14] + temp[1] + temp[15:17] + temp[2]
        answer += temp[18:33] + temp[17] + temp[14] + temp[11]
        answer += temp[33] + temp[37:39] + temp[34] + temp[40:42] + temp[35] + temp[43:45]
        answer += self.transpose(temp[45:54], 1)
        
        if custom_state: return answer
        else: self.state = answer

    def S(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:3] + temp[43] + temp[40] + temp[37] + temp[6:9]
        answer += temp[9] + temp[3] + temp[11:13] + temp[4] + temp[14:16] + temp[5] + temp[17]
        answer += temp[18:30] + temp[16] + temp[13] + temp[10] + temp[33:36]
        answer += temp[36] + temp[30] + temp[38:40] + temp[31] + temp[41:43] + temp[32] + temp[44]
        answer += temp[45:54]
        
        if custom_state: return answer
        else: self.state = answer

    def S_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state
        
        answer = temp[:3] + temp[10] + temp[13] + temp[16] + temp[6:9]
        answer += temp[9] + temp[32] + temp[11:13] + temp[31] + temp[14:16] + temp[30] + temp[17]
        answer += temp[18:30] + temp[37] + temp[40] + temp[43] + temp[33:36]
        answer += temp[36] + temp[5] + temp[38:40] + temp[4] + temp[41:43] + temp[3] + temp[44]
        answer += temp[45:54]
        
        if custom_state: return answer
        else: self.state = answer

    def F(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:6] + temp[44] + temp[41] + temp[38]
        answer += temp[6] + temp[10:12] + temp[7] + temp[13:15] + temp[8] + temp[16:18]
        answer += self.transpose(temp[18:27], 0)
        answer += temp[15] + temp[12] + temp[9] + temp[30:36]
        answer += temp[36:38] + temp[27] + temp[39:41] + temp[28] + temp[42:44] + temp[29] + temp[45:54]
        
        if custom_state: return answer
        else: self.state = answer

    def F_apostrophe(self, custom_state=None):
        if custom_state: temp = custom_state
        else: temp = self.state

        answer = temp[:6] + temp[9] + temp[12] + temp[15]
        answer += temp[29] + temp[10:12] + temp[28] + temp[13:15] + temp[27] + temp[16:18]
        answer += self.transpose(temp[18:27], 1)
        answer += temp[38] + temp[41] + temp[44] + temp[30:36]
        answer += temp[36:38] + temp[8] + temp[39:41] + temp[7] + temp[42:44] + temp[6] + temp[45:54]
        
        if custom_state: return answer
        else: self.state = answer

    def apply_algorithm(self, algorithm):
        """Applies an inputted algorithm (in the form of a list) to the cube"""
        func_list = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'",
                     "M", "E", "S", "M'", "E'", "S'"]
        func_list2 = [self.F, self.R, self.U, self.L, self.B, self.D,
            self.F_apostrophe, self.R_apostrophe, self.U_apostrophe,
            self.L_apostrophe, self.B_apostrophe, self.D_apostrophe,
            self.M, self.E, self.S, self.M_apostrophe, self.E_apostrophe,
            self.S_apostrophe]

        final_dict = {}
        length = len(func_list)
        for i in range(length):
            final_dict[func_list[i]] = func_list2[i].__name__

        for move in algorithm:
            if any(char.isnumeric() for char in move):
                turn = getattr(self, final_dict[move[0]])
                turn()
                turn()
            else:
                turn = getattr(self, final_dict[move])
                turn()

    def scramble(self, input_range=15):
        """
        Scrambles the cube a given number of times
        Returns a string of the moves that were applied to the cube
        """
        answer = ""
        scramble_length = random.randint(input_range - 5 , input_range + 5)
        func_list = [self.F, self.R, self.U, self.L, self.B, self.D, self.M, self.E, self.S,
            self.F_apostrophe, self.R_apostrophe, self.U_apostrophe, self.L_apostrophe, 
            self.B_apostrophe, self.D_apostrophe, self.M_apostrophe, self.E_apostrophe,
            self.S_apostrophe]
        func_list2 = ["F", "R", "U", "L", "B", "D", "M", "E", "S", "F'", "R'", "U'", "L'", "B'", 
                      "D'", "M'", "E'", "S'"]

        for i in range(input_range):
            move = random.choice(func_list)
            move()
            answer += str(move.__name__) + " "

        final_dict = {}
        func_list_len = len(func_list)
        for i in range(func_list_len):
            final_dict[func_list[i].__name__] = func_list2[i]
            
        final_answer = ""
        answer = answer.strip()
        answer = answer.split(" ")
        for char in answer:
            final_answer += final_dict[char] + " "
        
        return final_answer

    def neighbors(self, state):
        """
        Returns a list of states that are one move away from the inputted state
        The list is made of tuples, with the first value representing the move that
        was made, and the second value representing the state that was reached after
        applying said move
        """
        opposites1 = {"F": "F'", "R": "R'", "U": "U'", "B": "B'", "L": "L'", "D": "D'",
                     "F'": "F", "R'": "R", "U'": "U", "B'": "B", "L'": "L", "D'": "D",
                     "M": "M'", "E": "E'", "S": "S'", "M'": "M", "E'": "E", "S'": "S"}

        opposites2 = {"F": "B'", "F'": "B", "R": "L'", "R'": "L", "U": "D'", "U'": "D",
                      "B'": "F", "B": "F'", "L'": "R", "L": "R'", "D'": "U", "D": "U'"}
        # (action, resulting state)
        candidates = [
            ("F", self.F(state)), ("F'", self.F_apostrophe(state)),
            ("R", self.R(state)), ("R'", self.R_apostrophe(state)),
            ("U", self.U(state)), ("U'", self.U_apostrophe(state)),
            ("B", self.B(state)), ("B'", self.B_apostrophe(state)),
            ("L", self.L(state)), ("L'", self.L_apostrophe(state)),
            ("D", self.D(state)), ("D'", self.D_apostrophe(state)),
            ("M", self.M(state)), ("M'", self.M_apostrophe(state)),
            ("E", self.E(state)), ("E'", self.E_apostrophe(state)),
            ("S", self.S(state)), ("S'", self.S_apostrophe(state)),
            ]

        return candidates

    def build_heuristic_db(self):
        """
        Builds a pattern database of ~10.5 million states, and the number of moves
        required to reach each state, using breadth-first search
        Returns a dictionary where each key is a state, and each value is the number
        of moves required to reach the state
        """
        self.reset()

        # Initialize frontier to just the starting position
        start = (self.state, 0)
        frontier = []
        frontier.append(start)
        heuristic_db = {self.state: 0}
        # Keep looping until solution found
        with tqdm(total=36012942, desc='Heuristic DB') as pbar:
            while True:
                # If nothing left in frontier, then no path
                if not frontier:
                    print(len(heuristic_db))
                    return heuristic_db

                # Choose a node from the frontier
                configuration, rotations = frontier.pop()

                if rotations == 6:
                    continue

                # Add neighbors to frontier
                for action, state in self.neighbors(configuration):
                    if state not in heuristic_db or heuristic_db[state] > rotations + 1:
                        heuristic_db[state] = rotations + 1
                    frontier.append((state, rotations + 1))
                    pbar.update(1)
