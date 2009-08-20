
from base_agent import MenaceAgent

class SymmetryAgent(MenaceAgent):

    def state_hash(self, state):
        """
        Create a unique hash that is the same regardless of board homomorphisms.
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



