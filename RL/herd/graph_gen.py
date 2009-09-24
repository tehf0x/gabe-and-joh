'''
Created on Sep 24, 2009

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def hash_13(state):
    return state[0]*13**2 + state[1]*13 + state[2]

def graph_vals(state_values):
    x = [hash_13(state) for state in state_values.keys()]
    y = state_values.items()
    graph((x,), (y,), 'state 1')

def graph_vals_multi(state_values_multi):
    pass

def graph(x_m, y_m, titles, name):
    fig = Figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    
    plots = list()
    
    for i in range(len(x_m)):
        ax.plot(x_m[i],y_m[i], label=titles[i])
    
    ax.legend(titles)
    
    ax.set_xlabel("Value")
    ax.set_ylabel("State Number")

    # Make the PNG
    canvas = FigureCanvasAgg(fig)
    #Image resolution is dpi * size
    canvas.print_figure('%s.png' % name, dpi=150)

if __name__ == "__main__":
    x_m = (range(0,50,1),)
    y_m = (range(0,50,1),)
    graph(x_m, y_m,('one',), 'test')
