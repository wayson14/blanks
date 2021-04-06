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
    
    def __init__(self):
        self.letter_set = pl_letter_set
        self.letter_sack = []
        self.used_letter_sack = []
        for i in self.letter_set.keys():
            for j in range (self.letter_set[i]):
                self.letter_sack.append(i)
        

    def get_letters(self, count):
        to_return = []
        for i in range (count):
            chosen = random.choice(range(len(self.letter_sack)))
            to_return.append(self.letter_sack[chosen])
            self.used_letter_sack.append(self.letter_sack[chosen])
            del(self.letter_sack[chosen])
        
        
        return to_return
        






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
    def __init__(self, board_obj, *args, **kwargs):
        self.board_obj = board_obj
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
            return False
        s = start_point
        i = 0
        l = None
        for char in word:
            if direction == "vertical":
                l = self.board_obj.check_letter_field([s[0]+i,s[1]])
                if  l != char and l != 0:
                    return False
            elif direction == "horizontal":
                l = self.board_obj.check_letter_field([s[0],s[1]+i])
                if  l != char and l != 0:
                    return False
            i += 1
        
        return True
        



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
        
        if not self.check_if_possible(word,space,direction,start_point):
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
        pass
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

    
    
    def turn(self, word, direction, start_point, *args, **kwargs):

        self.move_translate(word, direction, start_point, *args, **kwargs)
        value = self.calc_word_score(self.before_move_board,self.after_move_board)

        self.moves_value.append(value)
        self.moves_board.append(self.after_move_board)

        return True


