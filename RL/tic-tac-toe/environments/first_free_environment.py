from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from wrapper_environment import WrapperEnvironment

class FirstFreeEnvironment(WrapperEnvironment):

    def play(self):
        """
        Pick the first free spot, and play there.
        """
        for i in range(len(self.state)):
            if self.state[i] == 0:
                self.state[i] == self.color
        return

if __name__ == "__main__":
    EnvironmentLoader.loadEnvironment(FirstFreeEnvironment())
