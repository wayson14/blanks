from flask import render_template, Blueprint


import core.blanks_core as blanks_core

core = blanks_core.Core()
game = Blueprint("game", __name__, static_folder="static", template_folder="templates")



@game.route("/test")
def test():
    return render_template("test.html.jinja", board = core.board, vars_dict = core.show_all_vars())

