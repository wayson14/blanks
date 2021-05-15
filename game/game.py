from flask import render_template, Blueprint, request, redirect, url_for


import core.blanks_core as blanks_core
import game.mesa_core as mesa_core



### 1. "mesa" is a particular game between players.
### 2. "core" is an object (distinct for every mesa) which contains atributes and methods specific for particular game - also "player" objects are stored within it
### 3. "engine" is an object used to 'play' the game - i.e. it modifies properities in "core" and binds everything. Main method of "engine" is "turn" - makesa single turn further

### for purpose of development there will be only 3 instances of Core() 
### mesa number is also an ID                                             
### core[0] (thus ID = 0) is reserved for testing purposes              


### initialization ###
               
board_count = 5
for i in range(board_count):
    core = [blanks_core.Core() for i in range(board_count)]
engine = mesa_core.Engine()
game = Blueprint("game", __name__, static_folder="static", template_folder="templates")


### URL routing ###

@game.route("/test")
def test():
    return render_template("mesa.html.jinja", board = core[0].board, bonuses = core[0].bonuses, vars_dict = core[0].show_all_vars(), id = 0)


@game.route("/<id>", methods=["POST", "GET"])
def mesa(id):
    id = int(id)
    if request.method == "POST":
        material = request.form["move"]
        core[id] = mesa_core.make_turn(core[id], material)
        core[id] = engine.turn(core[id], material)
        return redirect(url_for("game.mesa", id = id))
    else:
        return render_template("mesa.html.jinja", core = core[id], board = core[id].board, bonuses = core[id].bonuses, vars_dict = core[id].show_all_vars(), id = id)



### backbone mesa processing ###

