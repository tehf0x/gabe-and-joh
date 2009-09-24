'''
Created on Sep 24, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def hash_13(state):
    return state[0]*13**2 + state[1]*13 + state[2]

def graph_state_values(state_values):
    x = [hash_13(state) for state in state_values.keys()]
    y = state_values.items()

def graph(x, y, name):
    fig = Figure(figsize=(5,5))
    
    ax = fig.add_subplot(111)

    ax.plot(x,y, 'r-')
    ax.grid(False)

    ax.set_xlabel("Value")
    ax.set_ylabel("State Number")

    # Make the PNG
    canvas = FigureCanvasAgg(fig)
    # The size * the dpi gives the final image size
    #   a4"x4" image * 80 dpi ==> 320x320 pixel image
    canvas.print_figure('%s.png' % name, dpi=150)

if __name__ == "__main__":
    graph(range(0,100), range(0,100), 'test')
