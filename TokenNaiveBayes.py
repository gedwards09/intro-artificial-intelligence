import numpy as np
from TokenAlphabet import TokenAlphabet
from TokenUnigramCounter import TokenUnigramCounter
from TokenDocument import TokenDocument

class TokenNaiveBayes:

    """
    Fits a Naive Bayes classifier to two text documents
    """

    def __init__(self, filenameLeft, filenameRight, priorLeft = 0.50):
        if priorLeft <= 0.0 or 1.0 <= priorLeft:
            raise Exception("TokenNaiveBayes.py:Probability must be between 0 \
and 1.")
        self._priorLeft = priorLeft
        self._counterLeft = TokenUnigramCounter(filenameLeft)
        self._counterRight = TokenUnigramCounter(filenameRight)

    def TokenPosteriorProb(self, token):
        pleft = self._counterLeft.GetTokenProb(token) * self._priorLeft
        pright = self._counterRight.GetTokenProb(token) \
                * ( 1 - self._priorLeft)
        denom = pleft + pright
        return pleft / denom

    def Classify(self, text):

        """
        RETURNS: 1 if the classifier predicts the text belongs to the source 
                 text, 0 if it belongs to the other text
        """

        logProbLeft = np.log(self._priorLeft)
        logProbRight = np.log(1 - self._priorLeft)
        for token in text:
            pLeft = self._counterLeft.GetTokenProb(token)
            logProbLeft += np.log(pLeft)
            pRight = self._counterRight.GetTokenProb(token)
            logProbRight += np.log(pRight)
        return 1 if logProbLeft >= logProbRight else 0

