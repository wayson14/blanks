import unittest

import sys
sys.path.append("..")

from core.resources import *
from core.blanks_core import *
from core.exception_module import *

class TestCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = Core()
        cls.atributes = ["board", "bonuses", "players", "rarity_dict", "values_dict", "used_list"]
        
    def setUp(self):
        pass
        

    def tearDown(self):
        pass

    def test_setUpClass(self):
        self.assertIsInstance(self.core, Core)

    #utility section
    def test_clear_board(self):
        self.core.clear_board()
        self.assertListEqual(self.core.board, letter_board)

    def test_instances(self):
        for atribute in self.atributes:
            self.assertTrue(hasattr(self.core, atribute))

    def test_get_input(self):
        self.assertListEqual(self.core.parse_input("rower a6 h"), ["n", "rower", (0,5), "horizontal"])
        self.assertListEqual(self.core.parse_input("rower c8 v"), ["n", "rower", (2,7), "vertical"])
        self.assertListEqual(self.core.parse_input("!e asdfh"), ["e", "asdfh"])
        self.assertListEqual(self.core.parse_input("!s"), ["s", "surrender"])
    
    def test_print_board(self):
        #self.core.print_board()
        pass

    #checking section

    def test_map_words(self):
        self.core.board = assert_row_and_column
        x = self.core.map_words(["n", "row", (7,8), "horizontal"])
        print()
        print(x)

        self.core.board = letter_board


    def test_check_space(self):
        with self.assertRaises(EndOfBoardError):
            result = self.core.check_space(["n", "rower", (14,14), "horizontal"])
        with self.assertRaises(EndOfBoardError):
            result = self.core.check_space(["n", "rower", (14,14), "vertical"])
        self.assertTrue(self.core.check_space(["n", "rower", (6,6), "vertical"]))

    def test_check_board(self):
        with self.assertRaises(AlreadyFilledError):
            result = self.core.check_board(["n", "rower", (0,0), "vertical"], "assert_bicycle")
        with self.assertRaises(AlreadyFilledError):
            result = self.core.check_board(["n", "rower", (0,0), "horizontal"], "assert_bicycle")
        self.assertTrue(self.core.check_board(["n", "rower", (1,0), "vertical"], "assert_bicycle"))

    def test_check_letters(self):
        with self.assertRaises(DeckLetterLackError):
            result = self.core.check_letters("rower",["a"])
        with self.assertRaises(DeckLetterLackError):
            result = self.core.check_letters("rower",["r","o","w"])
        with self.assertRaises(DeckLetterLackError):
            result = self.core.check_letters("rower",["r","o","w","e"])
    
        self.assertTrue(self.core.check_letters("rower",["r","o","w","e","r"]))

    # def test_check_dictionary(self):
    #     self.core.handle_dict()
    #     self.assertTrue(self.core.check_dictionary("żyźniejszy"))

    def test_blank_check(self):
        self.assertEqual(self.core.blank_check(["n", "rower", (0,0), "vertical"], ["*","o","w","e","r"]), [[(4,0),'r']])

        self.assertListEqual(self.core.blank_check(["n", "rower", (0,0), "vertical"], ["*","o","w","*","r"]), [[(3,0),'e'], [(4,0),'r']])

        self.assertListEqual(self.core.blank_check(["n", "rower", (0,0), "horizontal"], ["*","o","w","*","r"]), [[(0,3),'e'], [(0,4),'r']])
        
        

    #manipulation section
    def test_place_word(self):
        self.core.place_word(["n", "bicycle", (0,0), "horizontal"])
        self.assertListEqual(self.core.board, assert_bicycle)
        self.core.place_word(["n", "bracket", (0,0), "vertical"])
        self.assertListEqual(self.core.board, assert_bicycle_and_bracket)

    def test_score_word(self):
        self.core.clear_board()
        self.core.before_board = self.core.board
        self.core.move = ["n", "bicycle", (0,0), "horizontal"]
        self.core.board = assert_bicycle
        self.assertEqual(self.core.score_word(), 95)


    def test_score_recur_check(self):
        self.core.board = assert_bicycle
        self.assertEqual(self.core.score_recur_check((0,1),(0,0)), 6)
        self.core.board = assert_bracket
        self.assertEqual(self.core.score_recur_check((1,0),(0,0)), 6)
        self.core.board = resources.letter_board


    def test_make_before_board(self):
        self.assertListEqual(self.core.before_board, letter_board)

    def test_rm_letters(self):
        self.assertListEqual(self.core.rm_letters("ab", ["a","b","c"]), ["c"])
        self.assertListEqual(self.core.rm_letters("abb", ["a","b","b","b","c"]), ["b","c"])

    def test_get_letters(self):
        self.assertEqual(len(self.core.get_letters(5)), 5)
        self.assertEqual(len(self.core.get_letters(0)), 0)

    def test_return_letters(self):
        self.assertListEqual(self.core.return_letters("a",["a","b"]), ["a"] )


    #instances and objective section
    def test_create_players(self):
        self.core.create_players()
        for i in range(self.core.players):
            self.assertTrue(hasattr(self.core, "player"))


if __name__ == '__main__':
    unittest.main()