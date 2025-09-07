import re
from TokenAlphabet import TokenAlphabet

class TokenDocument:

    """
    Reads a source document into a token string.
    Strips any non-token characters, replaces consecutive spaces with a single
    space, and ends the token string with a single space character
    """

    def __init__(self, filename):
        self._text = self._readFile(filename)
        self._size = len(self._text)

    def _readFile(self, filename):
        with open(filename, 'r') as file:
            return self._read(file.read())

    def _read(self, text):
        return TokenDocument._cleanText(text)

    # static
    # private
    def _cleanText(text):
        # Make everything lower case
        text = text.lower()
        # remove all characters except for letters and spaces
        text = re.sub(r"(\t\n\r)+", " ", text)
        inAlphabet = lambda ch: ch in TokenAlphabet.GetLanguage()
        text = ''.join([ch for ch in text if inAlphabet(ch)])
        # Replace consecutive spaces by a single space
        text = re.sub(r"[\t\n\r ]+", " ", text)
        # If last character is not a space, add space as the last token
        if text[-1] != " ":
            text += " "
        return text
    
    def getText(self):
        return self._text
    
    def getToken(self, idx):
        if idx < 0 or self._size <= idx:
            raise Exception("TokenDocument.py:getToken: Out of bounds index.")
        return self._text[idx]
    
    def getTextSize(self):
        return self._size
    
    def printText(self, width=80, maxLines=None):
        TokenDocument.Print(self._text, width=width, maxLines=maxLines)

    # static
    def Print(text, width=80, maxLines=None):
        words = text.split(' ')
        line = ''
        szLine = 0
        lineCount = 0
        for word in words:
            if maxLines != None and maxLines <= lineCount:
                break
            szWord = len(word)
            if szLine + szWord + 1 > width:
                print(line)
                line = word
                szLine = szWord
                lineCount += 1
            elif line == '':
                line = word
                szLine = szWord
            else:
                line = ' '.join([line, word])
                szLine += 1 + szWord
        if maxLines == None or lineCount < maxLines:
            print(line)

