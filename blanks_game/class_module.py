import sys

sys.path.append(".")

from flask import Flask
import copy
import random
from .func_module import *
from .resources import * 

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

class Game(object):
    
    def __init__(self, players = 2, time = 0, letter_set = pl_letter_set, used_dic = pl_letter_dict, *args, **kwargs):
        self.letter_set = letter_set
        self.used_dic = used_dic
        self.letter_sack = [] #filled 4 lines below
        self.used_letter_sack = []
        self.players = players
        self.time = time
        for i in self.letter_set.keys():
            for j in range (self.letter_set[i]):
                self.letter_sack.append(i)
    

    def get_letters(self, count):
        to_return = []
        for i in range (count):
            chosen = random.choice(range(len(self.letter_sack)))
            to_return.append(self.letter_sack[chosen])
            
            del(self.letter_sack[chosen])
        
        return to_return

    def use_letters(self, word):
        to_use = []
        for char in word:
            to_use.append(char)
            self.used_letter_sack.append(char)

        return to_use
    


        






class Board(Game):
    def __init__(self):
        pass

    def create_letter_board(self):#creates letter board 
        letter_board = [[0] * 15 for i in range (15)]
        self.letter_board = letter_board
        return self.letter_board


        
    def create_bonus_board(self):#creates bonus board 
        """
        Bonus Board: 
        "TW" - triple word
        "DW" - double word
        "TL" - triple letter
        "DL" - double letter
        "NM" - no multiplier
        """
        self.bonus_board = bonus_board
        return self.bonus_board

    def add_letter(self, letter, point, *args, **kwargs):
        board = self.letter_board
        if type(letter) != str:
            raise TypeError
        if not letter.isalpha() and letter != '*':
            raise ValueError 

        board[point[0]][point[1]] = letter
        return board

    def rm_letter(self, point, *args, **kwargs):
        board = self.letter_board
        board[point[0]][point[1]] = 0
        return board

    def check_letter_field(self,point, *args, **kwargs):
        board = self.letter_board
        return board[point[0]][point[1]]

    def check_bonus_field(self,point, *args, **kwargs):
        board = self.bonus_board
        return board[point[0]][point[1]]

    def get_board(self, kind = 'letter'):
        if kind == 'bonus':
            print(self.bonus_board)
            return self.bonus_board

        else:
            print(self.letter_board)
            return self.letter_board

    

class Player(Game):
    def __init__(self, board_obj, game_obj, *args, **kwargs):
        self.board_obj = board_obj
        self.game_obj = game_obj
        self.deck = game_obj.get_letters(7)
        self.moves_value = []
        self.moves_board = []
        self.used_dic = pl_letter_dict
    
    def check_if_enough_space(self, word, space):
        if len(word) > space:
            return False
        else: 
            return True
    
    def check_if_possible(self, word, space, direction, start_point):
        if not self.check_if_enough_space(word,space):
            return "wrong place"

        for char in word:
            if char not in self.deck:
                return "used not owned letters" 


        s = start_point
        i = 0
        l = None
        for char in word:
            if direction == "vertical":
                l = self.board_obj.check_letter_field([s[0]+i,s[1]])
                if  l != char and l != 0:
                    return "different word already placed"
            elif direction == "horizontal":
                l = self.board_obj.check_letter_field([s[0],s[1]+i])
                if  l != char and l != 0:
                    return "diffreent word already placed"
            i += 1
        
        return True
    
    def ui_turn(self):
        
        move_list = []
        
        texts = ["WORD: ", "DIRECTION: (h/v) ", "POSITION: "]
        for text in texts:
            move_list.append(input(text))

        return move_list


        



    def move_translate(self, word, direction, start_point , *args, **kwargs):
        s = start_point
        i = 0
        space = 100

        #copying pre move board
        self.before_move_board = copy.deepcopy(self.board_obj.letter_board)

        if direction =="vertical":
            space = 15 - start_point[0]
        elif direction == "horizontal":
            space = 15 - start_point[1]
        
        if self.check_if_possible(word,space,direction,start_point) != True:
            error = self.check_if_possible(word,space,direction,start_point) 
            raise ValueError

        for char in word:
            # print(char)
            if direction == "vertical":
                self.board_obj.add_letter(char,[s[0]+i,s[1]])
                i += 1
            elif direction == "horizontal":
                self.board_obj.add_letter(char,[s[0],s[1]+i])
                i += 1
            
            else:
                raise ValueError
        
        #copying after move board
        self.after_move_board = copy.deepcopy(self.board_obj.letter_board)


        # print("FROM move_translate: ",self.board_obj.letter_board)
        return self.board_obj.letter_board
    
    def check_letter_value(self, letter):
        for key in self.used_dic.keys():
            if letter in key:
                return self.used_dic[key]

    def calc_word_score(self, before_board, after_board, dic=pl_letter_dict, *args, **kwargs):

        self.used_dic = dic
        fifty = False
        total = 0
        bonus_list = []
        changed = []
        dw_count = 0
        tw_count = 0
        for row in range (len(before_board)):
            for pos in range (15):
                if before_board[row][pos] != after_board[row][pos]:
                    bonus_list.append(self.board_obj.bonus_board[row][pos])
                    changed.append(after_board[row][pos])
 
        for i in range(len(changed)):

            letter_value = self.check_letter_value(changed[i])#to be changed for dictionary with letter values
            if bonus_list[i] == "DL":
                total += letter_value*2
            elif bonus_list[i] == "TL":
                total += letter_value*3
            elif bonus_list[i] == "DW":
                total += letter_value
                dw_count += 1
            elif bonus_list[i] == "TW":
                total += letter_value
                tw_count += 1
            else:
                total += letter_value
            if i == 6:
                fifty = True
        total = total * (2**dw_count) * (3**tw_count)  
        if fifty:
            total += 50
        return total

    
    def check_win(self):
            
        if end:
            pass


    def turn(self, *args, **kwargs):
        turn_flag = True
        while turn_flag == True:
            print(f"DECK: {self.deck} POINTS: {self.moves_value} PLAYER: {self.p}")
            turn_flag = False

            kind = input("Turn type: (normal, pass, exchange)")
            
            
            if kind == "normal":

                try:
                    move = self.ui_turn()

                    word = move[0]
                    direction = move[1]
                    start_point = eval(move[2])

                    if direction == "h":
                        direction = "horizontal"
                    else:
                        direction = "vertical"
                except:
                    turn_flag = True
                    continue
                # word = "rower"
                # direction = "horizontal"
                # start_point = (6,6)

                try:

                    self.move_translate(word, direction, start_point, *args, **kwargs)
                    value = self.calc_word_score(self.before_move_board,self.after_move_board)

                    self.moves_value.append(value)
                    self.moves_board.append(self.after_move_board)

                    used = self.game_obj.use_letters(word)
                    got = self.game_obj.get_letters(len(word))

                    for char in used:
                        if char in self.deck:
                            del self.deck[self.deck.index(char)]
                    
                    for char in got:
                        print(self.deck)
                        self.deck.append(char)
                
                except ValueError:
                    turn_flag = True
                    print("Check if you passed values correctly!")
                
                except:
                    turn_flag = True
                    print("An error has occured, check values and try again!")
            
            if kind == "pass":
                print("passed turn")
                try:
                    self.moves_value.append(0)
                except:
                    turn_flag = True
                    continue

            if kind =="exchange":
                try:
                    to_exchange = input("Which letters do you want to exchange: ")

                    for char in to_exchange:
                        del self.deck[self.deck.index(char)]

                    got = self.game_obj.get_letters(len(to_exchange))
                    for char in got:
                        print(self.deck)
                        self.deck.append(char)

                    self.moves_value.append("-")
                except:
                    turn_flag = True
                    continue
        

        
        return True


