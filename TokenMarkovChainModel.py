from random import random

from TokenAlphabet import TokenAlphabet
from TokenProbabilityArray import TokenProbabilityArray
from TokenTrigramModelCounter import TokenTrigramModelCounter

class TokenMarkovChainModel(TokenTrigramModelCounter):

    """
      Builds and simulates a simple trigram Markov chain model based on a 
      source document. The class trains a model which can be used to generate
      new sentences based on the source text.
    """
    
    """
      Generate sentences using the bigram Markov chain model
    """
    def generateBigramSentence(self, length, first =' '):
        sentence = first
        currentToken = first
        for i in range(length-1):
            currentToken = self.generateBigramToken(currentToken)
            sentence += currentToken
        return sentence
    
    """
      Generate sentences using the trigram Markov chain model. Switches to the
      bigram model if the prior bigram was never observed in the source text.
    """
    def generateTrigramModelSentence(self, length, first=' '):
        # generate the 2nd token from the first token using the bigram model
        second = self.generateNormalizedBigramToken(first)
        sentence = first + second
        for i in range(2, length):
            bigram = first + second
            bigramIdx = TokenAlphabet.GetBigramIndex(bigram)
            if self._bigramCounts[bigramIdx] > 0:
                current = self.generateTrigramToken(bigram)
            else:
                # if the previous bigram has never occured generate the next 
                # token use the normalized bigram model
                current = self.generateNormalizedBigramToken(second)
            sentence += current
            first = second
            second = current
        return sentence
    
    """
      Generate next token from the current bigram using the unnormalized bigram
      model
    """
    def generateBigramToken(self, current):
        charIdx = TokenAlphabet.GetTokenIndex(current)
        cumulativeProbs = self._bigramCumulativeTransitionProbs[charIdx]
        return TokenMarkovChainModel\
                .GenerateTokenFromCumulative(cumulativeProbs)

    """
      Generate next token from the current bigram using the normalized bigram
      model
    """
    def generateNormalizedBigramToken(self, current):
        charIdx = TokenAlphabet.GetTokenIndex(current)
        cumulativeProbs =\
                self._bigramNormalizedCumulativeTransitionProbs[charIdx]
        return TokenMarkovChainModel\
                .GenerateTokenFromCumulative(cumulativeProbs)
    
    """
      Generate next token from the current bigram using the trigram model
    """
    def generateTrigramToken(self, bigram):
        idx = TokenAlphabet.GetBigramIndex(bigram)
        cumulativeProbs = self._trigramCumulativeTransitionProbs[idx]
        return TokenMarkovChainModel\
                .GenerateTokenFromCumulative(cumulativeProbs)
    

    """
      Generate the next token from a cumulative distribution
    """
    # static
    def GenerateTokenFromCumulative(cumulativeProbs):
        randValue = random()
        nextIdx = TokenProbabilityArray.\
                BinarySeach(cumulativeProbs, randValue)
        return TokenAlphabet.GetToken(nextIdx)


