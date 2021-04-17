import sys

#sys.path.append("..")


from blanks_game.resources import *
from blanks_game.blanks_core import *
from blanks_game.exception_module import *


class App(object):
    def __init__(self):
        self.run_flag = True

        self.player_turn = 0

        pass
        
    

    def run(self):

        
        while(self.run_flag == True):
            
            #initial letter give
            if core.turn == 0:
                core.letter_dict = core.handle_dict()
                for i in range(core.players):
                    core.player[i].deck = core.get_letters(7)
            

            #board & ui render
            core.print_ui(self.player_turn)
            core.print_board()

            #input from a player/saved 
            material = core.get_input()
            if material == '':
                move = core.premoves(core.turn)
                core.turn += 1
            else:
                try:
                    core.turn += 1
                    move = core.parse_input(material)
                except BaseException as err:
                    print("ERROR", err)
                    return
            try:
                assert type(move) == list
            except BaseException as err:
                print("ERROR", err)
                return
            else:
                core.move = move

            

            #turn type
            turn_type = move[0]
                

            #catches exception from particular turn
            try:
                if turn_type == "n":
                    self.normal_turn()
                elif turn_type == "p":
                    self.pass_turn()
                elif turn_type == "s":
                    self.surrender_turn()
                elif turn_type == "e":
                    self.surrender_turn()
                else:
                    raise ValueError("Turn type not    specified!")
            except BaseException as err:
                core.error_display(err)
                continue
            
            self.player_turn += 1
            
            if self.player_turn > core.players-1:
                self.player_turn = 0
        
    def normal_turn(self, move = "move"):

        move = getattr(core, move)
        
        word = move[1]
        deck = core.player[self.player_turn].deck

        #checking whether move is possible
        try:
            core.check_space(move)
            core.check_board(move)
            core.check_allignment(move)
            core.check_letters(word, deck)
            core.check_dictionary(word)
            
        except BaseException as err:
            raise err

        core.make_before_board()
        core.place_word(move)

        score = core.score_word()
        core.player[self.player_turn].points.append(score)

        core.rm_letters(word, deck)
        core.player[self.player_turn].deck = deck + core.get_letters(len(word))

    def pass_turn(self, move = "move"):
        core.turn += 1
        self.player_turn += 1


app = App()
core = Core()

app.run()
