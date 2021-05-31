# EXPERIMENTAL BRANCH


# remote imports

import core.blanks_core as blanks_core
import sys
from flask import Flask, redirect, url_for, render_template, request, Blueprint
from game.game import game




core = blanks_core.Core()
app = Flask(__name__)
app.register_blueprint(game, url_prefix="/game")
app.secret_key = b'_5#y3L"F4Q8z\n\xec]/'


def main():

    @app.route("/")
    def home():
        return render_template("index.html",
                               content="content",
                               board=core.board)

    
    app.run(debug=True)

    

if __name__ == '__main__':

    main()
