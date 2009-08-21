import random
from rlglue.environment import EnvironmentLoader
from wrapper_environment import WrapperEnvironment

class RandomEnvironment(WrapperEnvironment):
    
    name = 'random'
    
    def play(self):
        """
        Pick the first free spot, and play there.
        """
        open_spots = []
        for i in range(len(self.state)):
            if self.state[i] == 0:
                open_spots.append(i)
        self.state[random.choice(open_spots)] = self.color

if __name__ == "__main__":
    EnvironmentLoader.loadEnvironment(RandomEnvironment())
