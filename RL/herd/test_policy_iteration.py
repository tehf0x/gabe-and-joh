'''
Test value iteration

Created on 24 Sep 2009

@author: joh
'''

from value_methods import policy_iteration

if __name__ == '__main__':
    values = []
    V, pi = policy_iteration(gamma=0.9, theta=0.01, value_list=values)
    
    assert values[-1] == V
    
    def vcmp(v1, v2):
        #print 'vcmp',v1,v2
        return cmp(v1[1], v2[1])
        
    V = sorted(V.items(), cmp=vcmp)
    
    for v in V:
        print v, "=>", pi[v[0]]
    
    
    print "%d policy evaluation steps were required." % (len(values))
    
    
