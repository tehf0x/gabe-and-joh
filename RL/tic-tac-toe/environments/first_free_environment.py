import WrapperEnvironment

class FirstFreeEnvironment(WrapperEnvironment):

    def play(self):
        """
        Pick the first free spot, and play there.
        """
        for i in len(self.state):
            if self.state[i] == 0:
                self.state[i] == self.color
        return
