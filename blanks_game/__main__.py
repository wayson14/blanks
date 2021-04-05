#remote imports
import sys
from flask import Flask, redirect, url_for, render_template, request


#absolute imports (used to pass content to a webpage)
import blanks_game.func_module as func_module
import blanks_game.class_module as class_module

#relative imports
from .func_module import * 
from .class_module import *


app = Flask(__name__)

#naming convention: <lowercase class name>_obj
access_obj = Access()
game_obj = Game()
home_page_obj = HomePage()


#in order to restart an app use an alias "repython"
#
def main():

    #project zone
    
    #tutorial/testing zone
    @app.route("/")
    def home():
        return render_template("index.html",
         func_module = func_module,
         content = "Some valuable content")


    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            user = request.form["nm"]
            return redirect(url_for("user", usr = user))


    @app.route("/<usr>")
    def user(usr):
        return f"<h1>{usr}</h1>"


    @app.route("/admin")
    def admin():
        if access_obj.authorization() == True:
            return "Welcome admin."
        else:
            print("test")
            return redirect(url_for("home"))

    
    app.run(debug=True)
    #print('in main')
    
if __name__ == '__main__':
    main()
