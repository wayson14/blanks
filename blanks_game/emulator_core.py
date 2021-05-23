import sys

# sys.path.append("..")


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

            # initial letter give
            if core.turn == 0:
                core.word_dict = core.handle_dict()
                for i in range(core.players):
                    core.player[i].deck = core.get_letters(7)

            core.show_all_vars()

            # board & ui render
            core.print_ui(self.player_turn)
            core.print_board()

            # input from a player/saved
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

            # turn type
            core.turn_type = move[0]

            # catches exception from particular turn
            try:
                if core.turn_type == "n":
                    self.normal_turn()
                elif core.turn_type == "p":
                    self.pass_turn()
                elif core.turn_type == "s":
                    self.surrender_turn()
                elif core.turn_type == "e":
                    self.exchange_turn()
                else:
                    raise ValueError("Turn type not    specified!")
            except BaseException as err:
                core.error_display(err)
                continue

            self.player_turn += 1
            core.turn += 1

            if self.player_turn > core.players-1:
                self.player_turn = 0

    def normal_turn(self, move="move"):

        try:
            move = getattr(core, move)
            words = []
            word = move[1]
            deck = core.player[self.player_turn].deck

        # checking whether move is possible
            core.check_space(move)
            core.check_board(move)
            core.blanks_info += core.blank_check(move, deck)
            core.check_allignment(move)
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
            core.player[self.player_turn].points.append(score)

            core.rm_letters(word, deck)
            core.player[self.player_turn].moves.append(move)
            core.player[self.player_turn].deck = deck + \
                core.get_letters(7-len(deck))

        except BaseException as err:
            raise err

    def pass_turn(self, move="move"):
        p = self.player_turn
        core.moves.append('!p')
        core.player[self.player_turn].moves.append(f"!p")
        core.player[p].points.append(0)
        pass

    # TO BE CONTINUED

    def exchange_turn(self, move="move"):
        p = self.player_turn
        try:
            move = getattr(core, move)
        except BaseException as err:
            raise err

        w = move[1]

        core.return_letters(w, core.player[p].deck)
        r = core.get_letters(len(w))

        for i in r:
            core.player[p].deck.append(i)

        core.player[p].points.append(0)
        core.player[self.player_turn].moves.append(f"!e {w}")

    def surrender_turn(self, move="move"):
        p = self.player_turn

        core.player[p].points.append(0)
        core.player[self.player_turn].moves.append(f"!s")

        for p in range(core.players):
            print(f"PLAYER {p} MOVES: ")
            for i in range(len(core.player[p].moves)):
                print(
                    f"{core.player[p].moves[i]} | {core.player[p].points[i]}")

        self.run_flag = False


app = App()
core = Core()

app.run()
