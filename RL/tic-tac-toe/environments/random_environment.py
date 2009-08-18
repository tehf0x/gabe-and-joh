from random
import WrapperEnvironment

class RandomEnvironment(WrapperEnvironment):

    def play(self):
        """
        Pick the first free spot, and play there.
        """
        open_spots = []
        for i in len(self.state):
            if self.state[i] == 0:
                open_spots.append[i]
        self.state[random.choice(open_spots)] = self.color


