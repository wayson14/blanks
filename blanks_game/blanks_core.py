import sys

sys.path.append(".")

from flask import Flask
import copy
import random

import blanks_game.resources as resources

from .exception_module import *
from .func_module import *




class Core(object):
    """Class containing whole game engine.
"board", "bonuses", "players", "rarity_dict", "values_dict", "used_list"
    """
    def __init__(self, players = 2, rarity_dict = "pl_rarity_dict", values_dict = "pl_values_dict"):

        self.board = getattr(resources, "letter_board")
        self.bonuses = getattr(resources, "bonus_board")
        self.players = players
        self.rarity_dict = getattr(resources, rarity_dict)
        self.values_dict = getattr(resources, values_dict)
        self.used_list = []

    def parse_input(self, material):
        if ' ' in material:
            m = material.split(' ')
        else:
            m = material
        if m[0][0] != '!':
            
            #normal variation
            m[1] = "(" + chr(ord(m[1][0])-49) + "," + chr(ord(m[1][1]) - 1) + ")"
            m[1] = eval(m[1])
            if m[2] == "h":
                m[2] = "horizontal"
            else:
                m[2] = "vertical"
            
            l = len(m)
            for i in range(l):
                m.append(m[i])
            for i in range(l-1):
                del(m[i])            
            m[0] = 'n'
            return m

        else:
            if '!e' in m:
                return ["e", m[1]]
                #exchange variation

            elif '!p' in m:
                return ["p", "pass"]
                #pass variation

            elif '!s' in m:
                return ["s", "surrender"]
                #surrender variation


    def print_board(self, board = "board"):
        board = getattr(self, board)
        a = 0
        print()
        for y in board:

            if a == 0:
                print("  |", end="")
                for i in range(15):
                    if i <9:
                        print(f" {i+1} |", end="")
                    else:
                        print(f" {i-9} |", end="")
                print("")
                for i in range(63):
                    print('=', end="")
                print("")

            
            else:
                for i in range(63):
                    print('-', end="")
                print("")
            print(f"{chr(a+65)} || ", end="")
            for x in y:
                print(x, end=' | ')
            print()

            a += 1
        
        print("\n")

    def check_space(self,move):
        raise EndOfBoardError
    def check_if_possible(self, move):
        pass




    def place_word(self, move):
        raise ValueError("Error!!!!!")
        



