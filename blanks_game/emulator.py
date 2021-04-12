import sys

#sys.path.append("..")

from blanks_game.class_module import *
from blanks_game.func_module import *
from blanks_game.resources import *

class App(object):
    def __init__(self):
        self.run_flag = True
        self.game_flag = True

        self.game_obj = Game()
        self.board_obj = Board()
        self.player_obj = [Player(self.board_obj, self.game_obj) for i in range(self.game_obj.players)]

        self.board_obj.create_bonus_board()
        self.board_obj.create_letter_board()
        


    # def initial_settings():

    #     choice = input("Quick setup = Q \nNormal setup = N")
    #     if choice == 'n' or 'N':
    #         pass
    #         #to be continued
    #     else:
    #         self.game_obj = Game()
    #         self.board_obj = Board()
    #         self.player_obj = [Player(self.board_obj, self.game_obj) for i in range(self.game_obj.players)]

    #         self.board_obj.create_bonus_board()
    #         self.board_obj.create_letter_board()

    #     return True



    def run(self):
        
        #self.initial_settings()

        while(self.run_flag == True):
            for p in range(self.game_obj.players):
                for x in self.board_obj.letter_board:
                    print(x)
                self.player_obj[p].p = p
                self.player_obj[p].turn(kind = "normal")
            
            if self.player_obj.check_win():
                run_flag == False




app_obj = App()
app_obj.run()
