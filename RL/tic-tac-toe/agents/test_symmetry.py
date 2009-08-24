from symmetry_agent import SymmetryAgent

class TestSymmetry():
    
    def setup(self):
        self.state = [0,1,2,3,4,5,6,7,8]
        self.sym_a = SymmetryAgent()
        self.sym_a.board = [self.state[i:i+3] for i in range(0,9,3)]
        
    def teardDown(self):
        pass
    
    def test_direction(self):
        path = [[1,0],[0,0]]
        ret = self.sym_a.get_direction(path)
        assert ret == [0,1]
        path = [[2,1],[2,2]]
        ret = self.sym_a.get_direction(path)
        print ret
        assert self.sym_a.get_direction(path) == [-1, 0]
        path = [[1,0],[2,0]]
        ret = self.sym_a.get_direction(path)
        print ret
        assert ret == [0,1]
        
    def test_rotation(self):
        """
        Make sure the rotation calculations return correct values.
        """
        path = [[1,0],[2,0]]
        dir = self.sym_a.get_direction(path)
        ret = self.sym_a.get_rotation(path, dir)
        print ret
        assert ret == -1
        path = [[1,0],[0,0]]
        dir = self.sym_a.get_direction(path)
        ret = self.sym_a.get_rotation(path, dir)
        print ret
        assert ret == 1
        path = [[1,2],[0,2]]
        dir = self.sym_a.get_direction(path)
        ret = self.sym_a.get_rotation(path, dir)
        print ret
        assert ret == -1
        
    def test_go_round(self):
        """
        See if, given the first 2 points of a path, go_round properly completes the path.
        """
        ret = self.sym_a.go_around([[1,0],[2,0]])
        print ret
        assert ret == [4,3,6,7,8,5,2,1,0]
        ret = self.sym_a.go_around([[1,2],[2,2]])
        print ret
        assert ret == [4,5,8,7,6,3,0,1,2]
        ret = self.sym_a.go_around([[0,1],[0,0]])
        print ret
        assert ret == [4,1,0,3,6,7,8,5,2]
        
    def test_hash(self):
        #Simple hash test
        hash = self.sym_a.state_hash([0,1,2,3,4,5,6,7,8])
        print hash
        assert hash == 478521036
        #Test symmetry
        hash1 = self.sym_a.state_hash([0,1,0,1,1,2,2,1,2])
        hash2 = self.sym_a.state_hash([0,1,0,2,1,1,2,1,2])
        print hash1, hash2
        assert hash1 == hash2
        #Test rotation
        hash1 = self.sym_a.state_hash([0,1,1,2,0,1,1,2,0])
        hash2 = self.sym_a.state_hash([1,2,0,2,0,1,0,1,1])
        print hash1, hash2
        assert hash1 == hash2
        #Test double rotation
        hash1 = self.sym_a.state_hash([1,2,0,2,1,1,2,2,1])
        hash2 = self.sym_a.state_hash([1,2,2,1,1,2,0,2,1])
        print hash1, hash2
        assert hash1 == hash2
                                      
