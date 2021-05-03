###EXPERIMENTAL BRANCH


#remote imports
import sys
from flask import Flask, redirect, url_for, render_template, request


#absolute imports (used to pass content to a webpage)
import blanks_game.blanks_core as blanks_core

core = blanks_core.Core()

#relative imports
# from .func_module import * 
# from .class_module import *


app = Flask(__name__)



#in order to restart an app use an alias "repython"
#
def main():

    @app.route("/")
    def home():
        return render_template("index.html",
         content = "content",
         board = core.board)




    app.run(debug=True)
    #print('in main')
    
if __name__ == '__main__':
    main()
