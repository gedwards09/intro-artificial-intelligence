from TokenAlphabet import TokenAlphabet

class TokenProbabilityArray:

    """
    Utility functions for cumulative probability arrays
    """

    """ minmum probability to observe any token """
    s_minProb = 0.0001

    # static
    def CalculateCumulativeProbsFromCounts(countsArray, minProb = s_minProb):

        """
        Turns an array of counting statistics into a cumulative probability 
        distribution under the following constraints:
        1. Differential probabilities should be rounded to nearest significant  
           decimal (default: 0.0001).
        2. Differential probabilities which round to 0.0 (including counts of 
           zero!) should be rounded UP to a uniform minimum probability 
           (default: 0.0001).
        3. Differential probabilities should sum to 1.0000, exactly.
        """

        szLanguage = TokenAlphabet.GetLanguageSize()
        cumulativeProbs = [0 for _ in range(szLanguage)]
        total = sum(countsArray)
        if total == 0:
            # to assign uniform probability
            total = max(round(1/minProb), 0)
        minCount = total * minProb
        rareTokenCount = sum([1 if count < minCount else 0\
                                for count in countsArray])
        minCount = minCount / (1 - rareTokenCount * minProb)
        # we adjust any rare or unseen occurances to the minimum count
        adjustment = sum([(minCount - count) if count < minCount else 0\
                            for count in countsArray])
        total += adjustment
        runningTotal = 0
        runningCumulativeProb = 0
        for charIdx in range(szLanguage):
            if countsArray[charIdx] < minCount:
                runningCumulativeProb += minProb
                runningTotal += minProb * total
            else:
                runningTotal += countsArray[charIdx]
                runningCumulativeProb = round(runningTotal / total, 4)
            cumulativeProbs[charIdx] = runningCumulativeProb
        return cumulativeProbs
    
    # static
    def CalculateProbsFromCumulativeProbs(cumulativeProbs):
        probs = [0 for _ in range(TokenAlphabet.GetLanguageSize())]
        for idx in range(len(cumulativeProbs)):
            raw = cumulativeProbs[idx]
            raw -= cumulativeProbs[idx-1] if idx > 0 else 0
            probs[idx] = round(raw, 4)
        return probs
    
    # static
    def BinarySeach(cumulativeProb, value):
        return TokenProbabilityArray\
                ._coreBinarySearch(\
                    cumulativeProb, value, 0, len(cumulativeProb))
    
    # static
    def _coreBinarySearch(cumulativeProb, value, left, right):
        if left >= right:
            return left
        mid = (left + right)//2
        prob = cumulativeProb[mid]
        if prob < value:
            return TokenProbabilityArray\
                    ._coreBinarySearch(cumulativeProb, value, mid+1, right)
        elif prob == value:
            return mid
        else:
            return TokenProbabilityArray.\
                    _coreBinarySearch(cumulativeProb, value, left, mid)