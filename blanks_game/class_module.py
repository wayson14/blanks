from flask import Flask


class HomePage:
    def __init__(self):
        pass
    
    def show(self):
        return "This page is an instance called from a class."


class Access:
    def __init__(self):
        pass

    def authorization(self):
        return True

class Game:
    def __init__(self, *args, **kwargs):
        self.players = 2
        self.letter_set = "polish_standard"
        self.board_type = "standard"
        self.player_time = 10

    def set_board(self, *args, **kwargs):
        try:
            self.board_type = "standard"
            self.board = [[0] * 15 for i in range(15)]
            if self.board_type != "standard":
                pass
            else:
                for x in range (15):
                    for y in range (15):
                        board[x][y] = "0"
        except Exception as err:
            return err
        else:
            return self.board


    def render_board(board):
        pass