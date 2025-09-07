from TokenDocument import TokenDocument
from ICounter import ICounter

class AbstractTokenCounter(TokenDocument, ICounter):

    def __init__(self, filename):
        super().__init__(filename)
        self._initCounters()
        self._countTokens()
        self._calculateCumulativeProbs()
        self._calculateProbs()

