#!/usr/bin/env python
"""
Utility to create graphs from experiment data

Usage: graph.py <returns|steps|policy> <title> <result1.pickle> [result2.pickle...]

@author: joh
"""
from pylab import meshgrid
from matplotlib.mlab import frange
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

class Plot:
    
    colors = ['#ff0000', '#0000ff', '#00cc00']
    
    def __init__(self, title=None, xlabel='x', ylabel='y', 
                 axis=(None, None, None, None), figsize=(6.5,5)):
        self.fig = Figure(figsize=figsize)
        if title:
            self.fig.suptitle(title)
        
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.axis = axis
        
        self.plot_counter = -1
    
    def plot(self, X, Y=None, label=None):
        self.plot_counter += 1
        ax = self.fig.add_subplot(111, xlabel=self.xlabel, ylabel=self.ylabel)
        
        if not Y:
            Y = X
            X = range(len(X))
        
        ax.plot(X, Y, '-', color=self.colors[self.plot_counter], markersize=4, label=label)
        
        axis = list(ax.axis())
        # Modify only the specified axis elements
        for i,v in enumerate(self.axis):
            if v:
                axis[i] = v
        
        ax.axis(tuple(axis))
        ax.legend(loc='best')
    
    def save(self, filename):
        filepath = 'graphs/%s' % filename
        
        canvas = FigureCanvasAgg(self.fig)
        # Image resolution is dpi * size
        canvas.print_figure(filepath, dpi=150)
        
        print 'Graph saved to %s' % (filepath)
        

class PolicyPlot(Plot):
    
    def __init__(self, title=None, xlabel='', ylabel='', 
                 axis=(None, None, None, None), figsize=(5,5)):
        
        Plot.__init__(self, title, xlabel, ylabel, axis, figsize)
    
    def plot(self, policy):
        rows = len(policy)
        cols = len(policy[0])
        
        X,Y = meshgrid(range(rows), range(cols))
        
        # U, V give the x and y components of the arrow vectors
        U = [[0]*cols for _ in range(rows)]
        V = [[0]*cols for _ in range(rows)]
        
        for row,r in enumerate(policy):
            row = rows - row - 1
            for col,c in enumerate(r):
                a = c[0]
                if a == 'N':
                    U[row][col] = 0
                    V[row][col] = 1
                elif a == 'S':
                    U[row][col] = 0
                    V[row][col] = -1
                elif a == 'E':
                    U[row][col] = 1
                    V[row][col] = 0
                elif a == 'W':
                    U[row][col] = -1
                    V[row][col] = 0
                else:
                    raise ValueError
                    
        ax = self.fig.add_subplot(111)
        ax.quiver(X, Y, U, V, pivot='middle')
        ax.grid(linestyle='-')
        ax.set_xticks(frange(0.5, cols))
        ax.set_yticks(frange(0.5, rows))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        xmin, xmax, ymin, ymax = ax.axis()
        ax.axis([xmin-0.5, xmax-1, ymin-0.5, ymax-1])

    

def graph_vals(x, y, name):
    hashed = [(state, value) for state, value in state_values.items()]
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


if __name__ == '__main__':
    
    import sys
    import os
    import pickle
    
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <type> <result1.pickle> [result2.pickle[ ...]]\n" % (sys.argv[0]))
        sys.exit(-1)
    
    type = sys.argv[1]
    
    datasets = {}
    
    for filename in sys.argv[2:]:
        dataset = pickle.load(open(filename))
        name = os.path.basename(filename).split('.', 1)[0]
        datasets[name] = dataset
    
    if type == 'returns':
        # Plot returns
        returns_plot = Plot(title='Returns', xlabel='Episodes', ylabel='Return', axis=(None,None,-20,15))
        for name, d in datasets.items():
            returns_plot.plot(d['returns'], label=name)
        
        returns_plot.save('returns.png')
    
    elif type == 'steps':
        # Plot steps
        steps_plot = Plot(title='Steps', xlabel='Episodes', ylabel='Steps', axis=(None,None,None,500))
        for name, d in datasets.items():
            steps_plot.plot(d['steps'], label=name)
        
        steps_plot.save('steps.png')
    
    elif type == 'policy':
        # Plot policy
        for name, d in datasets.items():
            #p = ['N','E','S','W']
            #rows = len(d['policy'])
            #cols = len(d['policy'][0])
            #d['policy'] = []
            #for r in range(rows):
            #    d['policy'].append([(p[(i+r) % 4], ) for i in range(cols)])
            #d['policy'] = [[('S',)]*len(d['policy'][0]) for _ in range(len(d['policy']))]
            
            plot = PolicyPlot(title=name + ' Policy')
            plot.plot(d['policy'])
            plot.save(name + '.policy.png')
            
        #dataset = datasets[sys.argv[2]]
        #if len(datasets) > 1:
        #    print 'WARNING: When pl
        
    
    else:
        sys.stderr.write("Invalid plot type: %s" % (type))
        sys.exit(-1)
    
    
    
    
    