"""
Corpus based candidate matching and scoring

Created on 8 Sep 2009

@author: Johannes H. Jensen <joh@pseudoberries.com>
"""

import nltk

class FreqDist(nltk.FreqDist):
    """ Frequency distribution with some additional functionality """
    
    def load(self, file):
        """ Load frequency counts from file """
        self.loads(file.read())
    
    def loads(self, s):
        for line in s.split("\n"):
            if not line:
                continue
            
            parts = line.split()
            
            sample = tuple(parts[:-1])
            if len(sample) == 1:
                sample = sample[0]
            
            count = parts[-1]
            
            self[sample] = int(count)
    
    def dumps(self):
        s = ""
        for sample, count in self.items():
            if isinstance(sample, tuple):
                sample = ' '.join(sample)
                
            s += "%s\t%d\n" % (sample, count)
            
        return s
    
    def dump(self, file):
        """ Save frequency counts from file """
        file.write(self.dumps())
    
    def known(self, sample_list):
        """ Return a subset of sample_list where each element is known """
        return set(s for s in sample_list if self.has_key(s))
    
    def freq_cmp(self, s1, s2):
        f1 = self[s1]
        f2 = self[s2]
        if f1 < f2:
            return -1
        elif f1 == f2:
            return 0
        else: # f1 < f2
            return 1
    
    def sort_samples(self, samples, reverse=True):
        """ Sort list of words by frequency in the corpus """
        return sorted(samples, cmp=self.freq_cmp, reverse=reverse)
