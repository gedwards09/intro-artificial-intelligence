class TokenAlphabet():

    """
    Utility functions for working with the token language
    """
    
    ## the language of characters in lexographic order ##
    s_language = " abcdefghijklmnopqrstuvwxyz"
    ## Size of the language in tokens ##
    s_szLanguage = 27
    ## Map from character to token number ##
    s_charIndex = None
    ## Map from bigram to unique identifier ##
    s_bigramIndex = {}

    # static
    def GetLanguage():
        return TokenAlphabet.s_language
    
    # static
    def GetLanguageSize():
        return TokenAlphabet.s_szLanguage

    # static
    def GetTokenIndex(ch):
        if TokenAlphabet.s_charIndex == None:
            TokenAlphabet._initCharIndex()
        if ch in TokenAlphabet.s_charIndex:
            return TokenAlphabet.s_charIndex[ch]
        else:
            raise Exception(f"Charcter {ch} not found")

    # static
    def _initCharIndex():
        dic = {}
        array = TokenAlphabet.s_language
        for i in range(len(array)):
            dic[array[i]]=i
        TokenAlphabet.s_charIndex = dic

    # static
    def GetBigramIndex(bigram):
        if bigram in TokenAlphabet.s_bigramIndex:
            return TokenAlphabet.s_bigramIndex[bigram]
        firstIdx = TokenAlphabet.GetTokenIndex(bigram[0])
        secondIdx = TokenAlphabet.GetTokenIndex(bigram[1])
        bigramIdx = firstIdx * TokenAlphabet.s_szLanguage + secondIdx
        TokenAlphabet.s_bigramIndex[bigram] = bigramIdx
        return bigramIdx
        
    # static
    def GetToken(idx):
        if 0 <= idx and idx <= TokenAlphabet.s_szLanguage:
            return TokenAlphabet.s_language[idx]
    
