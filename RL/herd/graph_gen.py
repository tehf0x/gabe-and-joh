'''
Created on Sep 24, 2009

Generate plots rapidly and prettily.

@author: Gabe Arnold <gabe@squirrelsoup.net>
'''
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def hash_13(state):
    return state[0]*13**2 + state[1]*13 + state[2]

def graph_vals(state_values, name):
    hashed = [(hash_13(state), value) for state, value in state_values.items()]
    hashed = sorted(hashed, cmp = lambda a,b: cmp(a[0],b[0]))
    x = [el[0] for el in hashed]
    y = [el[1] for el in hashed]
    graph((x,), (y,), ('state 1',), name)


def graph(x_m, y_m, titles, name):
    fig = Figure(figsize=(6.5,5))
    ax = fig.add_subplot(111)
    
    plots = list()
    
    for i in range(len(x_m)):
        ax.plot(x_m[i],y_m[i], 'b.', markersize=4, label=titles[i])
    
    #ax.legend(titles, loc='lower right')
    axes = ax.axis()
    ax.axis((-75, 2200, -5, 140))
    ax.set_xlabel('State')
    ax.set_ylabel('Value')
    fig.suptitle(name)

    # Make the PNG
    canvas = FigureCanvasAgg(fig)
    #Image resolution is dpi * size
    canvas.print_figure('graphs/%s.png' % name, dpi=150)

