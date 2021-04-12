class BlanksExcpetion (BaseException):
    def __init__(self, message = ""):
        super().__init__(self)
        self.message = message
        

class EndOfBoardError (BlanksExcpetion):
    """ERROR: End of board.
    """
    def __init__(self, message = ""):
        super().__init__(self)
        self.message = message
 

        
 