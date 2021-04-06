import unittest

import sys
sys.path.append("..")

from blanks_game.resources import *
from blanks_game.class_module import Game, Board, Player, Access


class TestGame(unittest.TestCase):



    def setUp(self):
        self.board_obj = Board()
        self.player_obj = Player(self.board_obj)
        self.game_obj = Game()

    def tearDown(self):
        pass

    def test_get_letters(self):
        print(self.game_obj.get_letters(7))


class TestBoard(unittest.TestCase):



    def setUp(self):


        self.maxDiff = None
        self.board_obj = Board()
        self.board_obj.create_letter_board()
        self.board_obj.create_bonus_board()

        #resetting reference table
        assert_letter_board = [[0] * 15 for i in range (15)]
        self.assert_letter_board = assert_letter_board


    def tearDown(self):

        #resetting reference table
        assert_letter_board = [[0] * 15 for i in range (15)]
        self.assert_letter_board = assert_letter_board


    def test_create_board(self):
        self.assertListEqual(self.board_obj.create_letter_board(), [[0] * 15 for i in range (15)])

    def test_add_bonuses_to_scnd_layer(self):
        self.assertListEqual(self.board_obj.create_bonus_board(), bonus_board)

    def test_add_letter(self):  

        self.assert_letter_board[7][7] = 'b' 
        self.assertListEqual(self.board_obj.add_letter("b", (7,7)), self.assert_letter_board)

        self.assert_letter_board[7][7] = '*' 
        self.assertListEqual(self.board_obj.add_letter("*", (7,7)), self.assert_letter_board)

        with self.assertRaises(TypeError):
            result = self.board_obj.add_letter(1,(0,1)) 
        
        with self.assertRaises(ValueError):
            result = self.board_obj.add_letter("1",(0,1)) 

        with self.assertRaises(IndexError):
            result = self.board_obj.add_letter("b", (15, -16))

        with self.assertRaises(IndexError):
            result = self.board_obj.add_letter("b", (15, 'a'))
            
    def test_rm_letter(self):  #clone of the add_letter()

        self.board_obj.add_letter("b",(7,7))
        self.assertListEqual(self.board_obj.rm_letter((7,7)), self.assert_letter_board)
        
        with self.assertRaises(IndexError):
            result = self.board_obj.rm_letter((15, -16))

    def test_check_letter_field(self):
        
        self.board_obj.add_letter("a",(7,7))
        self.assertEqual(self.board_obj.check_letter_field((7,7)),"a")

        with self.assertRaises(IndexError):
            result = self.board_obj.check_letter_field((15,-16))
    
    def test_check_bonus_field(self):

        self.assertEqual(self.board_obj.check_bonus_field((7,7)),"DW")
        self.assertEqual(self.board_obj.check_bonus_field((0,0)),"TW")
        self.assertEqual(self.board_obj.check_bonus_field((1,0)),"NM")


class TestPlayer(unittest.TestCase):
    
    def setUp(self):

        self.maxDiff = None
        self.board_obj = Board()

        self.board_obj.create_letter_board()
        self.board_obj.create_bonus_board()
        
        # self.board_obj.add_letter("*",(7,7))
        # print(self.board_obj.letter_board)
        self.player_obj = Player(self.board_obj)
        

    def tearDown(self):
        del(self.player_obj)
        
    def test_move_translate(self):

        #translate tests
        #horizontal bicycle
        self.assertEqual(self.player_obj.move_translate("bicycle", "horizontal",(0,0)),assert_bicycle)

        #clearing
        self.board_obj.create_letter_board()

        #vertical bracket
        self.assertEqual(self.player_obj.move_translate("bracket", "vertical",(0,0)),assert_bracket)

        #both
        self.assertEqual(self.player_obj.move_translate("bicycle", "horizontal",(0,0)),assert_bicycle_and_bracket)
    

        #input/raises tests
        with self.assertRaises(TypeError):
            result = self.player_obj.move_translate(12,"horizontal",(0,0))

        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle",12,(0,0))

        with self.assertRaises(TypeError):
            result = self.player_obj.move_translate("bicycle","horizontal","kolomolo")
        
        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle",12,(16,0))
        
        #space on board to edge
        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle","horizontal",(0,10))
        
        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle","vertical",(10,0))

        #letter on board compatibility
        self.board_obj.add_letter("a",(7,7))
        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle","horizontal",(7,4))

        with self.assertRaises(ValueError):
            result = self.player_obj.move_translate("bicycle","vertical",(4,7))



    def test_length_of_boards(self):
        self.assertEqual(len(self.board_obj.bonus_board),len(self.board_obj.letter_board))
        
    def test_check_letter_value(self):
        self.assertEqual(self.player_obj.check_letter_value("b"),3)


    def test_calc_word_score(self, *args,**kwargs):

        
        # before_board = self.player_obj.calc_word_score(self.player_obj.before_board, self.board_obj.letter_board)
        # self.assertEqual(before_board,assert_letter_board)

        self.player_obj.move_translate("bicycle","horizontal",(0,0))

        self.before = self.player_obj.before_move_board
        self.after = self.player_obj.after_move_board

        result = self.player_obj.calc_word_score(self.before, self.after)
        self.assertEqual(result, 95)

    
    # def test_turn(self):
    #     self.assertTrue(self.player_obj.turn())

if __name__ == '__main__':
    unittest.main()
