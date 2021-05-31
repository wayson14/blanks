import copy
import random
import traceback

from flask import flash
from core.resources import *
from core.exception_module import *
import core.blanks_core as blanks_core


# material = raw input from a user
# move = checked input, valid move - ready to be processed further
# core = instance of a Core class


class Engine(object):
    def __init__(self):
        self.id_list = []
        pass

    def game_initialization(self, core):
        try:
            if core.dict_check == True:
                core.word_dict = core.handle_dict()

            for i in range(core.players):
                core.player[i].id = self.generate_id()
                core.player[i].deck = core.get_letters(7)
            core.turn += 1
        except BaseException as err:
            core.append(err)
        else:
            return True

    def turn(self, core, material):
        '''Returns given object (modified)'''

        ### initialization ###
        self.core = core

        if material == 'refreshing_passing':
            pass
        else:
            while core.run_flag == True:
                core.errors = []

                try:
                    self.checking_material(core, material)
                except BaseException as err:
                    core.errors.append((err, traceback.format_exc()))
                    break


                try:
                    self.start_proper_turn_type(core, material)
                except BaseException as err:
                    #core.errors.append((err, traceback.format_exc()))
                    flash(str(err), 'error')
                    break            
                
                if self.check_passes(core):
                    break

                core.player_turn += 1
                core.turn += 1
                if core.player_turn > core.players-1:
                    core.player_turn = 0
                break
        return core

    def checking_material(self, core, material):
        if material == ' ':
            core.move = core.premoves(core.turn)
            return True

        try:
            move = core.parse_input(material)

        except BaseException as err:
            raise err

        try:
            assert type(move) == list
        except BaseException as err:
            raise err
        else:
            core.move = move
            return True

    def generate_id(self):
        id = ''
        while True:
            for i in range(5):
                id += chr(random.randint(97, 123))

            if id not in self.id_list:
                break

        return id

    def start_proper_turn_type(self, core, material):
        core.turn_type = core.move[0]
        try:
            if core.turn_type == "n":
                self.normal_turn(core)
            elif core.turn_type == "p":
                self.pass_turn(core)
            elif core.turn_type == "s":
                self.surrender_turn(core)
            elif core.turn_type == "e":
                self.exchange_turn(core)
            else:
                raise ValueError("Turn type not specified!")
        except BaseException as err:
            raise err
        else:
            return True

    def normal_turn(self, core, move="move"):
        try:
            move = getattr(core, move)
            words = []
            word = move[1]
            deck = core.player[core.player_turn].deck

        # checking whether move is possible

            if core.space_check == True:
                core.check_space(move)
            if core.board_check == True:
                core.check_board(move)
            if core.blanks_check == True:
                core.blanks_info += core.blank_check(move, deck)
            if core.allignment_check == True:
                core.check_allignment(move)
            if core.letters_check == True:
                core.check_letters(word, deck)

        except BaseException as err:
            raise err

        try:
            # backuping board, placing word
            core.make_before_board()
            core.place_word(move)

            if core.dict_check == True:
                words += core.map_words(move)

                for i in words:
                    core.check_dictionary(i)

        except BaseException as err:

            core.board = core.before_board
            raise err

        try:
            # core.print_board(board="before_board")
            # core.print_board()

            score = core.score_word()
            core.player[core.player_turn].points.append(score)

            if core.letters_check == True:
                core.rm_letters(word, deck)
                core.player[core.player_turn].deck = deck +                    core.get_letters(7-len(deck))

            core.player[core.player_turn].moves.append(move)

        except BaseException as err:
            raise err

        return True

    def pass_turn(self, core, move="move"):
        try:
            p = core.player_turn
            core.moves.append('p')
            core.player[core.player_turn].moves.append(f"p")
            core.player[p].points.append(0)
        except BaseException as err:
            raise err
        return True

    def exchange_turn(self, core, move="move"):
        p = core.player_turn
        try:
            move = getattr(core, move)
        except BaseException as err:
            raise err
        
        try:

            w = move[1]

            core.return_letters(w, core.player[p].deck)
            r = core.get_letters(len(w))

            for i in r:
                core.player[p].deck.append(i)

            core.player[p].points.append(0)
            core.moves.append(f"!e {w}")
            core.player[core.player_turn].moves.append(f"e")

        except BaseException as err:
            raise err
        
        return True

    def surrender_turn(self, core, move="move"):
        p = core.player_turn

        core.player[p].points.append(0)
        core.player[core.player_turn].moves.append(f"s")
        
        
        self.finish(core)


    def check_passes(self,core):
        pass_count = 0
        for move in core.moves:
            if move == '!p':
                pass_count += 1
            else:
                pass_count = 0
            if pass_count > 2:
                print("passes")
                self.finish(core)
                return True
        return False

    def finish(self,core):
        core.run_flag = False
        core.info = core.choose_winner()
        flash(core.choose_winner(), 'info')
        

    #utility
    def convert_type(self, original, to_convert):
        original_type = type(original)
        if original_type == str:
            to_convert = str(to_convert)
        elif original_type == int:
            to_convert = int(to_convert)
        elif original_type == float:
            to_convert = float(to_convert)
        elif original_type == list:
            to_convert = list(to_convert)
        elif original_type == tuple:
            to_convert = tuple(to_convert)
        elif original_type == bool:
            to_convert = bool(to_convert)

        return to_convert
    
    def get_column(self, i, l):
        if i%10 < l:
            x = i%10+1
            return x
        elif i%(2*l) == 0:
            return 1
        else:
            x = (i-l)%10+1
            return x