from flask import render_template, Blueprint, request, redirect, url_for, flash, session


import core.blanks_core as blanks_core
import core.resources as resources
import game.mesa_core as mesa_core


# 1. "mesa" is a particular game between players.
# 2. "core" is an object (distinct for every mesa) which contains atributes and methods specific for particular game - also "player" objects are stored within it
# 3. "engine" is an object used to 'play' the game - i.e. it modifies properities in "core" and binds everything. Main method of "engine" is "turn" - makesa single turn further

# for purpose of development there will be only 3 instances of Core()
# mesa number is also an ID
# core[0] (thus ID = 0) is reserved for testing purposes

# UPPERCASE COMMANDS are used to modify in a high-level way behaviour of an app
#i.e. RESTART
### initialization ###

mesa_count = 10

core = [blanks_core.Core() for i in range(mesa_count)]
for i in range(mesa_count):
    core[i].id = i
engine = mesa_core.Engine()


game = Blueprint("game", __name__, static_folder="static",
                 template_folder="templates")

### URL routing ###
@game.route("/test")
def test():
    return render_template("mesa.html.jinja", board=core[0].board, bonuses=core[0].bonuses, vars_dict=core[0].show_all_vars(), id=0)


@game.route("/debug/<id>/<actual_player>", methods=["POST", "GET"])
def mesa_debug(id, actual_player):
    actual_player = int(actual_player)
    id = int(id)
    if request.method == "POST":
        material = request.form.get("move")
        exit = request.form.get("exit")

        if exit != None:
            core[id].player[actual_player].present = False
            session["in_game"] = False
            return redirect(url_for("game.lobby"))

        elif material == "RESTART":
            del(core[id])
            core[id] = blanks_core.Core()
            core[id].id = id
        
        elif "CHANGE" in material:
            material = material.split(' ')
            print(type(material[1]))
            print(hasattr(core[id], material[1]))
            try:
                if hasattr(core[id], material[1]):
                    material[2] = engine.convert_type(getattr(core[id], material[1]), material[2])
                    if material[2] == 'null':
                        flash(f'changed {material[1]} to null', 'info')
                    else:
                        setattr(core[id], material[1], material[2])
                    engine.turn(core,'refreshing_passing')

                else:
                    flash('Wrong attribute name!', 'error')
            except BaseException as err:
                flash (str(err), 'error')
            
            
        
        elif material == "KICK":
            for player in core[id].player:
                player.present = False
            return redirect(url_for("game.lobby"))

        elif core[id].player_turn == actual_player:
            core[id] = engine.turn(core[id], material)
        
        else:
            flash('Wait for your turn!', "info")
        return redirect(url_for("game.mesa", id=id, actual_player=actual_player))

    else:
        if 'in_game' not in session:
            session['in_game'] = False
        if core[id].player[actual_player].present == True and session["in_game"] == False:
            flash('Chosen seat is already occupied!', 'info')
            return redirect(url_for("game.lobby"))
        else:
            core[id].player[actual_player].present = True
            if core[id].turn == 0:
                engine.game_initialization(core[id])

            return render_template("mesa_debug.html.jinja", core=core[id], board=core[id].show_board(), bonuses=core[id].bonuses, vars_dict=core[id].show_all_vars(), id=id, engine=engine, actual_player = actual_player)

@game.route("/<id>/<actual_player>", methods=["POST", "GET"])
def mesa(id, actual_player):
    actual_player = int(actual_player)
    id = int(id)
    if request.method == "POST":
        if request.form.get("exit") != None:
            material = request.form.get("move")
            exit = request.form.get("exit")
            if exit == "exit":
                core[id].player[actual_player].present = False
                session["in_game"] = False
                return redirect(url_for("game.lobby"))
        

        material = request.form.get("move")
        if material == "RESTART":
            del(core[id])
            core[id] = blanks_core.Core()
            core[id].id = id
        
        elif "CHANGE" in material:
            material = material.split(' ')
            print(type(material[1]))
            print(hasattr(core[id], material[1]))
            try:
                if hasattr(core[id], material[1]):
                    material[2] = engine.convert_type(getattr(core[id], material[1]), material[2])
                    if material[2] == 'null':
                        flash(f'changed {material[1]} to null', 'info')
                    else:
                        setattr(core[id], material[1], material[2])
                    engine.turn(core,'refreshing_passing')

                else:
                    flash('Wrong attribute name!', 'error')
            except BaseException as err:
                flash (str(err), 'error')
            
            
        
        elif material == "KICK":
            for player in core[id].player:
                player.present = False
            return redirect(url_for("game.lobby"))

        elif core[id].player_turn == actual_player:
            core[id] = engine.turn(core[id], material)
        
        else:
            flash('Wait for your turn!', "info")
        return redirect(url_for("game.mesa", id=id, actual_player=actual_player))

    else:
        if 'in_game' not in session:
            session['in_game'] = False
        if core[id].player[actual_player].present == True and session["in_game"] == False:
            flash('Chosen seat is already occupied!', 'info')
            return redirect(url_for("game.lobby"))
        else:
            core[id].player[actual_player].present = True
            if core[id].turn == 0:
                engine.game_initialization(core[id])

            return render_template("mesa.html.jinja", core=core[id], board=core[id].show_board(), bonuses=core[id].bonuses, vars_dict=core[id].show_all_vars(), id=id, engine=engine, actual_player = actual_player)

@game.route("/lobby", methods=["POST", "GET"])
def lobby():
    session["in_game"] = False
    if request.method == "POST":
        
        if len(request.form.getlist('controlpanel')) > 1:
            actual_player = request.form.getlist('controlpanel')[0]
            id = request.form.getlist('controlpanel')[1]
        
        else:
            return render_template("lobby.html.jinja", cores=core, engine=engine)
            

        if actual_player != None:
            print(actual_player)
            session["in_game"] = True
            return redirect(url_for("game.mesa", id=id, actual_player=actual_player))

    else:
        return render_template("lobby.html.jinja", cores = core, engine=engine)


### backbone mesa processing ###
