import sys

sys.path.append(".")

from flask import Flask
import copy
import random

import blanks_game.resources as resources

from blanks_game.exception_module import *



class Player():
    def __init__(self, core):
        self.core = core
        self.points = []
        self.deck = []
        self.time = 0
    

class Core(object):
    """Class containing whole game engine.
"board", "bonuses", "players", "rarity_dict", "values_dict", "used_list"
    """
    def __init__(self, players = 2, rarity_dict = "pl_rarity_dict", values_dict = "pl_values_dict"):

        self.turn = 0
        self.moves = []
        self.move = ''
        self.last = ''

        self.board = getattr(resources, "letter_board")
        self.bonuses = getattr(resources, "bonus_board")
        self.empty_board = copy.deepcopy(getattr(resources, "letter_board"))
        
        self.players = players

        self.rarity_dict = getattr(resources, rarity_dict)
        self.values_dict = getattr(resources, values_dict)
        self.letter_dict = ["bicycle"] #watch out, it's huuge 42 MB
        self.dict_path = "blanks_game/slowa.txt"
        
        self.ava_list = []
        self.used_list = []

        self.assert_bicycle = resources.assert_bicycle

        self.before_board = self.board
        self.material = ''
        self.turn_type =''

        
        self.create_players()
        for i in self.rarity_dict.keys():
            for j in range (self.rarity_dict[i]):
                self.ava_list.append(i)

        #self.player
    
    
    ### UTILITY & GUI ###
    def get_input(self):
        print(f"Move pattern: <[!n/p/s]> <letters> <position(A-O|1-15)> <direction (h/v)>")
        material = input(f"Write your move: ")
        self.material = material
        return material
    
    def clear_board(self):
        self.board = [[0] * 15 for i in range (15)]
    
    def parse_input(self, material):
        if ' ' in material:
            m = material.split(' ')
        else:
            m = material
        if m[0][0] != '!':
            
            if len(m[1]) == 2:
                s = chr(ord(m[1][1]))
                #print(f"s: {s}")
            else:
                s = chr(ord(m[1][1]))+chr(ord(m[1][2]))
                #print(f"s: {s}")
                

            #print(m[1])
            if ord(m[1][0]) < 107:
                #normal variation
                m[1] = "(" + chr(ord(m[1][0])-49) + "," + str(int(s) - 1) + ")"
                m[1] = eval(m[1])
                #print(f"m[1]: {m[1]}")
            else:
                if m[1][0] == "k":
                    x = '10'
                elif m[1][0] == "l":
                    x = '11'
                elif m[1][0] == "m":
                    x = '12'
                elif m[1][0] == "n":
                    x = '13'
                elif m[1][0] == "o":
                    x = '14'
                else: 
                    raise WrongArgumentError(f"Wrong arguments: {m[1]}")

                m[1] = eval('('+x+','+str(int(s) - 1)+')')
                print(f"m[1]: {m[1]}")

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
            try:
                if '!e' in m:
                    return ["e", m[1]]
                    #exchange variation

                elif '!p' in m:
                    return ["p", "pass"]
                    #pass variation

                elif '!s' in m:
                    return ["s", "surrender"]
                    #surrender variation
                
                else:
                    raise WrongArgumentError(f"argument: {move[1]}")
            except WrongArgumentError as err:
                raise err
                            
    def print_board(self, board = "board"):
        board = getattr(self, board)
        a = 0
        print()
        for y in board:

            if a == 0:
                print("  ||", end="")
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
                if x != 0:
                    print(x, end=' | ')
                else:
                    print(' ', end=' | ')
            print()

            a += 1
        
        print("\n")
    
    def print_ui(self, p):
        print(f"|ACTUAL PLAYER: {p} || DECK: {self.player[p].deck} || SCORE: {self.player[p].points} |")
        print(f"SCOREBOARD: {[self.player[i].points for i in range (self.players)]}")
    
    def error_display(self, err):
        for i in range(25):
            print("=", end='')
        print("\n")
        print(err)
        print()
        for i in range(25):
            print("=", end='')
        print("\n")

    ### PLAYER & DICT MANIPULATION ###
    def create_players(self):
        self.player = [Player(self) for p in range(self.players)]

    def handle_dict(self, dict_path = "dict_path"):
        dict_path = getattr(self, dict_path)
        letter_dict = self.letter_dict
        f = open(dict_path, 'rt')
        n = 0
        for line in f.readlines():
            n+=1
            letter_dict.append(line[0:-1])
        #print(n)
        f.close()
        return letter_dict    
    
    
    ### VALIDITY CHECK ###
    def check_space(self, move):

        #debug
        # print()
        # print(f"x: {move[2][1]+1}")
        # print(f"y: {move[2][0]+1}")
        # print()

        
        
        try:
            if move[3] == "horizontal":
                e = int(move[2][1]) + len(move[1])
                #print(f"horizontal end point: {e}")

                
                if e > 15:
                    raise EndOfBoardError(f"Horizontal Error, word {e - 15} letter too long")
            elif move[3] == "vertical":
                e = move[2][0] + len(move[1])
                #print(f"vertical end point: { e - 15}")
                if move[2][0] + len(move[1]) > 15:
                    raise EndOfBoardError(f"Vertical Error, word {e - 15} too long" )
            #print()
        except BaseException as err:
            raise err

        return True

    def check_allignment(self, move, board = "board"):
        word = move[1]
        start = move[2]
        direction = move[3]

        board = copy.deepcopy(getattr(self, board))

        try:
            if board == self.empty_board:

                for i in range(len(word)):
                    if direction == "horizontal":
                        if start[1]+i == 7 and start[0] == 7:
                            return True
                        
                    else:
                        if start[0]+i == 7 and start[1]  == 7:
                            return True
                raise NotCentrallyAllignedError("Not centrally alligned!")


            else:
                for i in range(len(word)):
                    if direction == "horizontal":
                        if board[start[0]][start[1]+len(word)+1] != 0:
                            return True
                        if board[start[0]][start[1]-1] != 0:
                            return True
                        if board[start[0]+1][start[1]+i] != 0:
                            return True
                        if board[start[0]-1][start[1]+i] != 0:
                            return True
                    elif direction == "vertical":
                        if board[start[0]-1][start[1]] != 0:
                            return True
                        if board[start[0]+len(word)+1][start[1]] != 0:
                            return True
                        if board[start[0]+i][start[1]+1] != 0:
                            return True
                        if board[start[0]+i][start[1]-1] != 0:
                            return True
                raise NotStickingError("Lack of neighbouring words")

                        
        except BaseException as err:
            raise err

    def check_board(self, move, board = "board"):
        
        word = move[1]
        start = move[2]
        direction = move[3]

        board = getattr(self, board)


        try:

            if direction == "horizontal":
                for x in range(len(word)):
                    if board[start[0]][start[1]+x] != word[x] and board[start[0]][start[1]+x] != 0:
                        raise AlreadyFilledError(f"Horizontal, {x+1} letter doesn't match.")
            if direction == "vertical":
                for y in range(len(word)):
                    if board[start[0]+y][start[1]] != word[y] and board[start[0]+y][start[1]] != 0:
                        raise AlreadyFilledError(f"Vertical, {y+1} letter doesn't match.")
        except BaseException as err:
            raise err

        return True

    def check_letters(self, word, deck):
        a = copy.deepcopy(deck)
        for char in word:
            if char in a:
                del(a[a.index(char)])
            else:
                raise DeckLetterLackError(f"You miss letter: {char}")
        
        return True

    def check_dictionary(self, word, letter_dict = []):

        letter_dict = self.letter_dict
        #print(f"Word: {word}, Dict: {letter_dict[letter_dict.index(word)]}")

        if not word in letter_dict:

            raise LackOfWordInDictionary(f"{word} hasn't been found in used dicitonary.")
        else:
            return True

    def map_grid(self, pos):
        right = self.map_line((0,1),pos)
        left = self.map_line((0,-1),pos) 
        up = self.map_line((-1,0),pos)
        down = self.map_line((1,0),pos) 
        print()
        print(f"Start element: {self.board[pos[0]][pos[1]]}, its pos (program): {pos}")
        print(
f'''right: {right} {self.board[right[0]][right[1]]}
left: {left} {self.board[left[0]][left[1]]}
up: {up} {self.board[up[0]][up[1]]}
down: {down} {self.board[down[0]][down[1]]}''')
        return [right, left, up, down]

    def map_line(self, direction, pos):
        #directions:
        #(0, 1) - right
        #(0, -1) - left
        #(1, 0) - up
        #(-1, 0) - down

        new_pos = []
        x = self.board[pos[0]][pos[1]]
        # if x != 0:
        #     print(f'Element: {x} is on pos(programist indexing): {pos}')

        if self.board[pos[0]][pos[1]] == 0:
            new_pos.append(pos[0]-direction[0]) 
            new_pos.append(pos[1]-direction[1])
            return new_pos

        else:
            new_pos.append(pos[0]+direction[0]) 
            new_pos.append(pos[1]+direction[1])
            return self.map_line(direction, new_pos)

    def form_words(self, pos_list):
        words = ['','']

        #x range
        x = pos_list[0][1]-pos_list[1][1]+1

        #y range
        y = pos_list[3][0]-pos_list[2][0]+1
        print(x, y)


    ### BOARD MANIPULATION & SCORING ###
    # makes a copy of a board used to evaluate word score
    def make_before_board(self):

        self.before_board = copy.deepcopy(self.board)
        return True

    def place_word(self, move, board = "board"):
        
        word = move[1]
        start = move[2]
        direction = move[3]

        board = getattr(self, board)

        if direction == "horizontal":
            for x in range(len(word)):
                board[start[0]][start[1]+x] = word[x] 

        if direction == "vertical":
            for y in range(len(word)):
                board[start[0]+y][start[1]] = word[y] 
        self.board = board
        return True
    
    def score_recur_check(self, direction, pos):
        #directions:
        #(0, 1) - right
        #(0, -1) - left
        #(1, 0) - up
        #(-1, 0) - down

        new_pos = []
        new_pos.append(pos[0]+direction[0]) 
        new_pos.append(pos[1]+direction[1])

        x = self.board[pos[0]][pos[1]]
        if x != 0:
            pass
            #print(x, new_pos)
        if self.board[pos[0]][pos[1]] == 0:
            return -1
        
        elif self.board[pos[0]][pos[1]] == '*':
            return 0 + self.score_recur_check(direction, new_pos)

        else:
            return 1 + self.score_recur_check(direction, new_pos)

    def score_word(self): 

        before_board = self.before_board
        board = self.board

        # print("BEFORE BOARD:", board)
        # print("BOARD:", before_board)

        values_dict = self.values_dict
        fifty = False
        score = 0
        r_score = 0
        bonus_list = []
        placed = []
        dw_count = 0
        tw_count = 0
        letter = ''
        first = False
        start = []

        for y in range (len(before_board)):
            for x in range (15):
                if before_board[y][x] != board[y][x]:
                    if not first:
                        start.append(y)
                        start.append(x)
                        first = True
                    bonus_list.append(self.bonuses[y][x])
                    placed.append(board[y][x])
       
        self.last = self.last.join(placed)

        for i in range(len(placed)):
            if self.move[3] == "vertical":
                if i == 0:
                    r_score += self.score_recur_check((-1,0), start)
                    r_score += self.score_recur_check((0,-1), start)
                    r_score += self.score_recur_check((0,1), start)
                elif i <len(placed) - 1:
                    r_score += self.score_recur_check((0,1), start)
                    r_score += self.score_recur_check((0,-1), start)
                else:
                    r_score += self.score_recur_check((1,0), start)
                    r_score += self.score_recur_check((0,-1), start)
                    r_score += self.score_recur_check((0,1), start)
                start[0] +=1
            else:
                if i == 0:
                    r_score += self.score_recur_check((1,0), start)
                    r_score += self.score_recur_check((-1,0), start)
                    r_score += self.score_recur_check((0,-1), start)
                elif i <len(placed) - 1:
                    r_score += self.score_recur_check((1,0), start)
                    r_score += self.score_recur_check((-1,0), start)
                else:
                    r_score += self.score_recur_check((-1,0), start)
                    r_score += self.score_recur_check((1,0), start)
                    r_score += self.score_recur_check((0,1), start)
                start[1] +=1
                    
            letter = placed[i] 
            for key in values_dict.keys():
                if letter in key:
                    letter_value = values_dict[key]
                    break
            else:
                raise IndexError("Dictionary doesn't contain such value")

            if bonus_list[i] == "DL":
                score += letter_value*2
            elif bonus_list[i] == "TL":
                score += letter_value*3
            elif bonus_list[i] == "DW":
                score += letter_value
                dw_count += 1
            elif bonus_list[i] == "TW":
                score += letter_value
                tw_count += 1
            else:
                score += letter_value
            if i == 6:
                fifty = True
        score = score * (2**dw_count) * (3**tw_count)  
        if fifty:
            score += 50
        return score + r_score



    ### DECK AND AVA/USED LISTS ###
    # deck -> used
    def rm_letters(self, word, deck):
        for char in word:
            del(deck[deck.index(char)])
            self.used_list.append(char)
        return deck

    # avaivable -> deck
    def get_letters(self, count):
        to_return = []
        for i in range (count):
            chosen = random.choice(range(len(self.ava_list)))
            to_return.append(self.ava_list[chosen])
            del(self.ava_list[chosen])
        
        return to_return

    # deck -> avaivable
    def return_letters(self, word, deck):
        returned = []
        for char in word:

            del(deck[deck.index(char)])
            self.ava_list.append(char)
            returned.append(char)
        return returned



    ### TESTING ###
    def premoves(self, i):
        pre = resources.premoves
        if len(pre) > i:
            return pre[i]
        else: 
            return ["s"]
    #dead method
    def extract_placed(self):
        before_board = self.before_board
        board = self.board
        placed = []

        for y in range (len(before_board)):
            for x in range (15):
                if before_board[y][x] != board[y][x]:
                    placed.append(board[y][x])
       
        self.last = self.last.join(placed)
        return self.last

    
    

