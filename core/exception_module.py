class BlanksExcpetion (BaseException):
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)
        
        
class WrongArgumentError (BlanksExcpetion):
    """ERROR: Specified invalid arguments
    """
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)
        

class EndOfBoardError (BlanksExcpetion):
    """ERROR: End of board."""
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)
        

class NotCentrallyAllignedError (BlanksExcpetion):
    """ERROR: Firs move should be centrally alligned."""
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)

class LackOfWordInDictionary(BlanksExcpetion):
    """ERROR: Word should be in dicionary of avaivable words"""
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)

class NotStickingError (BlanksExcpetion):
    """ERROR: You need to stick to other word unless it's your first move."""
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)

class AlreadyFilledError (BlanksExcpetion):
    """ERROR: Different letter lies on this field.
    """
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)
        
 
class DeckLetterLackError (BlanksExcpetion):
    """ERROR: Lack of letters to make a word on a deck.
    """
    def __init__(self, message = ""):
        self.message = message
        super().__init__(self.message)
        
 
        
 