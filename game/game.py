from flask import render_template, Blueprint, request, redirect, url_for


import core.blanks_core as blanks_core

### for purpose of development there will be only 3 instances of Core() (further called "mesas") 
### mesa number is also a game ID visible in the URL                                             
### core[0] (thus ID = 0) is reserved for testing purposes              


### initialization ###
               
board_count = 5
for i in range(board_count):
    core = [blanks_core.Core() for i in range(board_count)]
game = Blueprint("game", __name__, static_folder="static", template_folder="templates")


### URL routing ###

@game.route("/test")
def test():
    return render_template("mesa.html.jinja", board = core[0].board, bonuses = core[0].bonuses, vars_dict = core[0].show_all_vars(), id = 0)


@game.route("/<id>", methods=["POST", "GET"])
def mesa(id):
    id = int(id)
    if request.method == "POST":
        move = request.form["move"]
        core[id].move = move
        return redirect(url_for("game.mesa", id = id))
    else:
        return render_template("mesa.html.jinja", board = core[id].board, bonuses = core[id].bonuses, vars_dict = core[id].show_all_vars(), id = id)



### backbone mesa processing ###

