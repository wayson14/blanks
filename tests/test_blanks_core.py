import unittest

import sys
sys.path.append("..")

from blanks_game.resources import *
from blanks_game.blanks_core import *
from blanks_game.exception_module import *

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

    def test_instances(self):
        for atribute in self.atributes:
            self.assertTrue(hasattr(self.core, atribute))

    def test_get_input(self):
        self.assertListEqual(self.core.parse_input("rower a6 h"), ["n", "rower", (0,5), "horizontal"])
        self.assertListEqual(self.core.parse_input("rower c8 v"), ["n", "rower", (2,7), "vertical"])
        self.assertListEqual(self.core.parse_input("!e asdfh"), ["e", "asdfh"])
        self.assertListEqual(self.core.parse_input("!s"), ["s", "surrender"])
    
    #checking section
    def test_check_space(self):
        with self.assertRaises(EndOfBoardError):
            result = self.core.check_space(["n", "rower", (15,15), "horizontal"])

    # def test_check_if_possible(self):
    #     with self.assertRaises(ValueError):
    #         result = self.core.check_if_possible(["n", "rower", (0,5), "horizontal"])

    def test_show_board(self):
        #self.core.print_board()
        pass





if __name__ == '__main__':
    unittest.main()