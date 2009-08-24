from menace_agent import MenaceAgent


class SymmetryAgent():

    def state_hash(self, state):
        """
        Create a unique hash that is the same regardless of board homomorphisms.
        """
	board = [state[i:i+3] for i in range(0,9,3)]

	paths = []
	for dir_x in (-1,1):
		for dir_y in (-1,1):
			paths.append([[1 + dir_x, 1], [1 + dir_x, 1 + dir_y]])
			paths.append([[1, 1+dir_y], [1 + dir_x, 1 + dir_y]])
	hashes = []

	for ((x1,y1),(x2,y2)) in paths:
		hashes.append([board[1][1], board[x1][y1], board[x2][y2]])
	print board

	self.go_round(board)
	return hashes

    def go_round(self, board):
		path = []
		pos = [1,2]
		dir = [-1,0] 
		mod = -1
		for step in range(8):
			print pos
			print dir
			print board[pos[0]][pos[1]]
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
		
		

""" 
        sym_hash = [0]*9
        sym_hash[0] = state[4] #Start with the middle of the board
        sequences = [[1, 2], [1, 0], [3, 0], [3, 6], [5, 2], [5, 8], [7, 8], [7, 6]]

        tmp_paths = [(state[i[0]]*10 + state[i[1]], i) for i in sequences]
        max_val = max(tmp_choices)[0]
        #Add the middle of the board to the paths
        [path[1].insert(0,4) for path in tmp_paths]
        paths = [path[1] for path in tmp_paths if path[0] == max_val]

        def construct_path(state, paths):
            path = []
            for path in paths:
                #Build out the first 3 steps of the path
                for step in path:
                    path.append(state[step])
                #And now go 'round the board

                step = path[-1]
                for i in range(6):
                    if(direction == 1):

                    if(step == 0):
                        step = 1
                    if(step ):
                        step = 7
                    if(step in (
"""

if __name__ == "__main__":
	sym = SymmetryAgent()
	print sym.state_hash([0,1,2,3,4,5,6,7,8])


