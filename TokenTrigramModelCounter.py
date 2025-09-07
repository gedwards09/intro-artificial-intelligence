from TokenAlphabet import TokenAlphabet
from TokenProbabilityArray import TokenProbabilityArray
from TokenUnigramCounter import TokenUnigramCounter

class TokenTrigramModelCounter(TokenUnigramCounter):

    """
      Constant used to initialize priors for regularization
      This implementation uses Jeffreys prior
    """
    s_smoothingConstant = 0.5

    # Override
    def _initCounters(self):
        szLanguage = TokenAlphabet.GetLanguageSize()
        self._unigramCounts = self._initTokenCounts(szLanguage)
        self._bigramTransitionCounts = [self._initTokenCounts(szLanguage)\
                for _ in range(szLanguage)]
        self._bigramCounts = self._initTokenCounts(szLanguage**2)
        self._trigramTransitionCounts = [self._initTokenCounts(szLanguage)\
                for _ in range(szLanguage**2)]

    # Override
    def _doCountToken(self, text, idx):
        curIdx = TokenAlphabet.GetTokenIndex(text[idx])
        self._unigramCounts[curIdx] += 1
        if idx <= 0:
            return
        prevIdx = TokenAlphabet.GetTokenIndex(text[idx-1])
        self._bigramTransitionCounts[prevIdx][curIdx] += 1
        if idx <= 1:
             return
        bigramIdx = TokenAlphabet.GetBigramIndex(text[(idx-2):idx])
        self._trigramTransitionCounts[bigramIdx][curIdx] += 1


    # Override
    def _calculateCumulativeProbs(self):
        self._unigramCumulativeProbs = self._calculateUnigramCumulativeProbs()
        self._bigramCumulativeTransitionProbs =\
                self._calculateBigramCumulativeTransitionProbs()
        self._bigramNormalizedCumulativeTransitionProbs =\
                self._calculateBigramCumulativeTransitionProbs(\
                    smoothing=TokenTrigramModelCounter.s_smoothingConstant)
        self._trigramCumulativeTransitionProbs =\
                self._calculateTrigramCumulativeTransitionProbs()
    
    def _calculateUnigramCumulativeProbs(self):
        return TokenProbabilityArray.\
                CalculateCumulativeProbsFromCounts(\
                    self._unigramCounts)
    
    def _calculateBigramCumulativeTransitionProbs(self, smoothing=0):
        szLanguage = TokenAlphabet.GetLanguageSize()
        cumulativeProbs = [None for _ in range(szLanguage)]
        for charIdx in range(szLanguage):
            counts = [count + smoothing\
                    for count in self._bigramTransitionCounts[charIdx]]
            cumulativeProbs[charIdx] = TokenProbabilityArray.\
                    CalculateCumulativeProbsFromCounts(\
                        counts)
        return cumulativeProbs
    
    def _calculateTrigramCumulativeTransitionProbs(self):
        szBigrams = (TokenAlphabet.GetLanguageSize())**2
        cumulativeProbs = [None for _ in range(szBigrams)]
        for bigramIdx in range(szBigrams):
            cumulativeProbs[bigramIdx] = TokenProbabilityArray.\
                    CalculateCumulativeProbsFromCounts(\
                        self._trigramTransitionCounts[bigramIdx])
        return cumulativeProbs

    # Override
    def _calculateProbs(self):
        self._unigramProbs = self._calculateUnigramProbs()
        self._bigramTransitionProbs = self._calculateBigramTransitionProbs()
        self._bigramNormalizedTransitionProbs =\
                self._calculateBigramNormalizedTransitionProbs()
        self._trigramTransitionProbs = self._calculateTrigramTransitionProbs()

    def _calculateUnigramProbs(self):
        cumulativeProbs = self._unigramCumulativeProbs
        return TokenProbabilityArray\
                .CalculateProbsFromCumulativeProbs(cumulativeProbs)

    def _calculateBigramTransitionProbs(self):
        cumulativeProbs = self._bigramCumulativeTransitionProbs
        return TokenTrigramModelCounter\
                ._calculateBigramProbsFromCumulativeProbs(cumulativeProbs)

    def _calculateBigramNormalizedTransitionProbs(self):
        cumulativeProbs = self._bigramNormalizedCumulativeTransitionProbs
        return TokenTrigramModelCounter\
                ._calculateBigramProbsFromCumulativeProbs(cumulativeProbs)

    # static
    # private
    def _calculateBigramProbsFromCumulativeProbs(cumulativeProbs):
        szLanguage = TokenAlphabet.GetLanguageSize()
        transitionProbs = [None for _ in range(szLanguage)]
        for idx in range(szLanguage):
            transitionProbs[idx] = TokenProbabilityArray\
                    .CalculateProbsFromCumulativeProbs(cumulativeProbs[idx])
        return transitionProbs
    
    def _calculateTrigramTransitionProbs(self):
        szBigrams = (TokenAlphabet.GetLanguageSize())**2
        transitionProbs = [None for _ in range(szBigrams)]
        cumulativeProbs = self._trigramCumulativeTransitionProbs
        for idx in range(szBigrams):
            transitionProbs[idx] = TokenProbabilityArray\
                    .CalculateProbsFromCumulativeProbs(cumulativeProbs[idx])
        return transitionProbs
    
    """
      Gets the bigram transition probabilities as a comma separated value table
    """
    def getTransitionProbs(self):
        return '\n'.join([self.getTransitionProbsFromCharacter(ch)\
                          for ch in TokenAlphabet.GetLanguage()])
    
    def getTransitionProbsFromCharacter(self, ch):
        charIdx = TokenAlphabet.GetTokenIndex(ch)
        return ','.join([str(p) for p in self._bigramTransitionProbs[charIdx]])
    
    def getNormalizedTransitionProbs(self):
        return '\n'\
                .join([self.getNormalizedTransitionProbsFromCharacter(ch)\
                        for ch in TokenAlphabet.GetLanguage()])
    
    def getNormalizedTransitionProbsFromCharacter(self, ch):
        charIdx = TokenAlphabet.GetTokenIndex(ch)
        return ','.join([str(p)\
                for p in self._bigramNormalizedTransitionProbs[charIdx]])