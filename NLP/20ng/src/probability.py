"""
...
"""
from nltk import ProbDistI

class NeyProbDist(ProbDistI):
    """
    Implements the Ney et al. discounting in a prob dist.
    """
    SUM_TO_ONE = True

    ABSOLUTE, LINEAR = (0,1)


    def __init__(self, freqdist, bins, n, n_0, factor=0.2, type = 0):
        """
        Use the Ney et al. estimate to create a prob dist.

        @type freqdist: C{FreqDist}
        @param freqdist: The frequency distribution that the
        probability estimates should be based on.

        @type factor: C{float}
        @param factor : the value for either C{delta} or C{alpha}
        depending on whether we're doing linear or absolute discounting.

        @type bins: C{int}

        @param bins: The number of sample values that can be generated
        by the experiment that is described by the probability
        distribution.  This value must be correctly set for the
        probabilities of the sample values to sum to one.  If
        {bins} is not specified, it defaults to C{freqdist.B()}.

        @type n: C{int}

        @param n: Number of training instances (*non*-distinct n-gram count)

        @type n_0: C{int}

        @param n_0: Number of bins with count 0: number of elements in
        the n-gram vocabulary that we have not encountered in the
        training data.

        @type factor: C{float}
        @param: Discount factor.

        @type type: C{int}
        @param: What type of discounting are we using.
        """
        if (bins == 0) or (bins is None and freqdist.N() == 0):
            name = self.__class__.__name__[:-8]
            raise ValueError('A %s probability distribution ' % name +
                             'must have at least one bin.')
            if (bins is not None) and (bins < freqdist.B()):
                name = self.__class__.__name__[:-8]
                raise ValueError('\nThe number of bins in a %s distribution ' % name +
                                 '(%d) must be greater than or equal to\n' % bins +
                                 'the number of bins in the FreqDist used ' +
                                 'to create it (%d).' % freqdist.N())

        if type not in (self.ABSOLUTE, self.LINEAR):
            raise ValueError('Unrecognize discounting type.')

        self._freqdist = freqdist
        self._bins = float(bins)
        self._n = float(n)
        self._n_0 = float(n_0)
        self._factor = float(factor)
        self._type = type


    def prob(self, sample):
        freq = float(self._freqdist[sample])

        #absolute discounting
        if self._type == self.ABSOLUTE:
            if(freq > 0):
                return (freq - self._factor) / self._n
            else:
                return (self._bins - self._n_0) * self._factor / (self._n_0 * self._n)
        #linear discounting
        else:
            if(freq > 0):
                return (1.0 - self._factor) * freq/self._n
            else:
                return self._factor / self._n_0

    def samples(self):
        return self._freqdist.samples()

