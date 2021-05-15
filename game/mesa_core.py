import copy, random, traceback

from core.resources import *
from core.exception_module import *


### material = raw input from a user
### move = checked input, valid move - ready to be processed further
### core = instance of a Core class 


class Engine(object):
    def __init__(self):
        self.errors = []
        pass
    
    def turn(self, core, material):
        '''This method is an "Axis Mundi" of the whole server
        side game (engine instance)
        Returns given object (modified)'''


        turn_run_flag = True

        while turn_run_flag == True:
            core.errors = []
            turn_run_flag = False

            try:
                check_material(core, material)
            except BaseException as err:
                core.errors.append((err,traceback.format_exc()))
                continue
            



        return core
        ### TO BE CONTINUED 15.05 ###
                
            

def check_material(core, material):
    try:
        core.turn += 1
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


def make_turn(core, move):
    core.moves.append(move)

    ### obscure function ###
    return core