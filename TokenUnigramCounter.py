from AbstractTokenCounter import AbstractTokenCounter
from TokenAlphabet import TokenAlphabet
from TokenProbabilityArray import TokenProbabilityArray

class TokenUnigramCounter(AbstractTokenCounter):

    # Override
    def _initCounters(self):
        self._tokenCounts = self._initTokenCounts()

    def _initTokenCounts(self, length):
        return [0 for _ in range(length)]

    # Override
    def _countTokens(self):
        text = self.getText()
        szText = self.getTextSize()
        for idx in range(0, szText):
            self._doCountToken(text, idx)

    def _doCountToken(self, text, idx):
        tokenID = TokenAlphabet.GetTokenIndex(text[idx])
        self._tokenCounts[tokenID] += 1


    # Override
    def _calculateCumulativeProbs(self):
        self._tokenCumulativeProbs = TokenProbabilityArray.\
                CalculateCumulativeProbsFromCounts(self._tokenCounts)

    # Override
    def _calculateProbs(self):
        self._tokenProbs = self._calculateTokenProbs()

    def _calculateTokenProbs(self):
        cumulativeProbs = self._tokenCumulativeProbs
        return TokenProbabilityArray\
                .CalculateProbsFromCumulativeProbs(cumulativeProbs)
    
    def GetTokenProb(self, token):
        tokenIdx = TokenAlphabet.GetTokenIndex(token)
        return self._tokenProbs[tokenIdx]
    
    """
      Gets the token probabilities as comma-delimited string
    """
    def getTokenProbs(self):
        return ','.join([str(p) for p in self._tokenProbs])