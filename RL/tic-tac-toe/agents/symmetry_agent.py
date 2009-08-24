from menace_agent import MenaceAgent


class SymmetryAgent():

    def state_hash(self, state):
        """
        Create a unique hash that is the same regardless of board homomorphisms.
        """
        self.board = [state[i:i+3] for i in range(0,9,3)]
        
        paths = []
        for dir_x in (-1,1):
            for dir_y in (-1,1):
                paths.append([[1 + dir_x, 1], [1 + dir_x, 1 + dir_y]])
                paths.append([[1, 1+dir_y], [1 + dir_x, 1 + dir_y]])
        
        pre_hashes = []
        for path in paths:
            pre_hashes.append(self.go_around(path))
            
        hashes = [int(''.join(map(str,pre))) for pre in pre_hashes]
            
        hashes.sort()
        
        return hashes[-1]
        
    def get_direction(self, path):
        """
        Figures out the initial direction vector that we need to go to continue the hash.
        """
        cur = path[1]
        #Hop once in every non-diagonal direction.  If it's not 
        #where we came from (but on the board), then it's where we're going.
        for i in (-1,0,1):
            for t in (-1,0,1):
                if abs(i) == abs(t): continue
                x_p = cur[0] + i
                y_p = cur[1] + t
                if (0 <= x_p <= 2 and 0 <= y_p <=2 and [x_p, y_p] != path[0]):
                    return [i, t]
        
    def get_rotation(self, path, dir):
        """
        Figure out the direction in which we are rotating to get the hash.
        Return 1 if counter-clockwise, -1 if clockwise.
        """
        if path[1] == [0,0]:
            if dir[0] == 1:
                return -1
            if dir[1] == 1:
                return 1
            
        if path[1] == [2,2]:
            #If we're going up
            if dir[0] == -1:
                return -1
            #If we're going left
            if dir[1] == -1:
                return 1
            
        if path[1] in [[2,0], [0,2]]:
            #If we'r going sideways
            if dir[0] == 0:
                return -1
            #If we're going up/down
            if dir[1] == 0:
                return 1
         
    def go_around(self, path):
        pos = path[1]
        dir = self.get_direction(path)
        mod = self.get_rotation(path, dir)
        #Start off in the middle:
        values = [self.board[1][1]]
        #And manually add the second element
        values.append(self.board[path[0][0]][path[0][1]])
        
        for step in range(7):
            values.append(self.board[pos[0]][pos[1]])
            if pos[0] + dir[0] > 2:
                dir = [0] * 2
                dir[1] = -1 * mod
            if pos[1] + dir[1] > 2:
                dir = [0] * 2
                dir[0] = 1 * mod
            if pos[0] + dir[0] < 0:
                dir = [0] * 2
                dir[1] = 1 * mod
            if pos[1] + dir[1] < 0:
                dir = [0] * 2
                dir[0] = -1 * mod
            pos[0] += dir[0]
            pos[1] += dir[1]
            
        return values

if __name__ == "__main__":
    sym = SymmetryAgent()
    sym.state_hash([0,1,2,3,4,5,6,7,8])

