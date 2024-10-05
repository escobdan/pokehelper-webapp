from flask import Flask, render_template, request, jsonify
import pokebase as pb
from flask_socketio import SocketIO, emit


async_mode = None
app = Flask(__name__)
# Configure application
# Web Socket setup
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")

counters = {
    'normal': {'strong_against': [], 'weak_against': ['rock', 'ghost', 'steel'], 'resistant_to': ['ghost'], 'vulnerable_to': ['fighting']},
    'fighting': {'strong_against': ['normal', 'rock', 'steel', 'ice', 'dark'], 'weak_against': ['flying', 'poison', 'psychic', 'bug', 'ghost', 'fairy'], 'resistant_to': ['rock', 'bug', 'dark'], 'vulnerable_to': ['flying', 'psychic', 'fairy']},
    'flying': {'strong_against': ['fighting', 'bug', 'grass'], 'weak_against': ['rock', 'steel', 'electric'], 'resistant_to': ['fighting', 'ground', 'bug', 'grass'], 'vulnerable_to': ['rock', 'electric', 'ice']},
    'poison': {'strong_against': ['grass', 'fairy'], 'weak_against': ['poison', 'ground', 'rock', 'ghost', 'steel'], 'resistant_to': ['fighting', 'poison', 'grass', 'fairy'], 'vulnerable_to': ['ground', 'psychic']},
    'ground': {'strong_against': ['poison', 'rock', 'steel', 'fire', 'electric'], 'weak_against': ['flying', 'bug', 'grass'], 'resistant_to': ['poison', 'rock', 'electric'], 'vulnerable_to': ['water', 'grass', 'ice']},
    'rock': {'strong_against': ['flying', 'bug', 'fire', 'ice'], 'weak_against': ['fighting', 'ground', 'steel'], 'resistant_to': ['normal', 'flying', 'poison', 'fire'], 'vulnerable_to': ['fighting', 'ground', 'steel', 'water', 'grass']},
    'bug': {'strong_against': ['grass', 'psychic', 'dark'], 'weak_against': ['fighting', 'flying', 'poison', 'ghost', 'steel', 'fire', 'fairy'], 'resistant_to': ['fighting', 'ground', 'grass'], 'vulnerable_to': ['flying', 'rock', 'fire']},
    'ghost': {'strong_against': ['ghost', 'psychic'], 'weak_against': ['normal', 'dark'], 'resistant_to': ['normal', 'fighting', 'poison', 'bug'], 'vulnerable_to': ['ghost', 'dark']},
    'steel': {'strong_against': ['rock', 'ice', 'fairy'], 'weak_against': ['steel', 'fire', 'water', 'electric'], 'resistant_to': ['normal', 'flying', 'poison', 'rock', 'bug', 'steel', 'grass', 'psychic', 'ice', 'dragon', 'fairy'], 'vulnerable_to': ['fighting', 'ground', 'fire']},
    'fire': {'strong_against': ['bug', 'steel', 'grass', 'ice'], 'weak_against': ['rock', 'fire', 'water', 'dragon'], 'resistant_to': ['bug', 'steel', 'fire', 'grass', 'ice'], 'vulnerable_to': ['ground', 'rock', 'water']},
    'water': {'strong_against': ['ground', 'rock', 'fire'], 'weak_against': ['water', 'grass', 'dragon'], 'resistant_to': ['steel', 'fire', 'water', 'ice'], 'vulnerable_to': ['grass', 'electric']},
    'grass': {'strong_against': ['ground', 'rock', 'water'], 'weak_against': ['flying', 'poison', 'bug', 'steel', 'fire', 'grass', 'dragon'], 'resistant_to': ['ground', 'water', 'grass', 'electric'], 'vulnerable_to': ['flying', 'poison', 'bug', 'fire', 'ice']},
    'electric': {'strong_against': ['flying', 'water'], 'weak_against': ['ground', 'grass', 'electric', 'dragon'], 'resistant_to': ['flying', 'steel', 'electric'], 'vulnerable_to': ['ground']},
    'psychic': {'strong_against': ['fighting', 'poison'], 'weak_against': ['steel', 'psychic', 'dark'], 'resistant_to': ['fighting', 'psychic'], 'vulnerable_to': ['bug', 'ghost', 'dark']},
    'ice': {'strong_against': ['flying', 'ground', 'grass', 'dragon'], 'weak_against': ['steel', 'fire', 'water', 'ice'], 'resistant_to': ['ice'], 'vulnerable_to': ['fighting', 'rock', 'steel', 'fire']},
    'dragon': {'strong_against': ['dragon'], 'weak_against': ['steel', 'fairy'], 'resistant_to': ['fire', 'water', 'grass', 'electric'], 'vulnerable_to': ['ice', 'dragon', 'fairy']},
    'dark': {'strong_against': ['ghost', 'psychic'], 'weak_against': ['fighting', 'dark', 'fairy'], 'resistant_to': ['ghost', 'psychic', 'dark'], 'vulnerable_to': ['fighting', 'bug', 'fairy']},
    'fairy': {'strong_against': ['fighting', 'dragon', 'dark'], 'weak_against': ['poison', 'steel', 'fire'], 'resistant_to': ['fighting', 'bug', 'dragon', 'dark'], 'vulnerable_to': ['poison', 'steel']}
    }

colors = {
	'normal': '#aab09f',
	'fire': '#ea7a3c',
	'water': '#539ae2',
	'electric': '#e5c531',
	'grass': '#71c558',
	'ice': '#70cbd4',
	'fighting': '#cb5f48',
	'poison': '#b468b7',
	'ground': '#cc9f4f',
	'flying': '#7da6de',
	'psychic': '#e5709b',
	'bug': '#94bc4a',
	'rock': '#b2a061',
	'ghost': '#846ab6',
	'dragon': '#6a7baf',
	'dark': '#373438',
	'steel': '#89a1b0',
	'fairy': '#e397d1',
}

data = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", data=data, colors=colors, counters=counters)

@app.route("/battle-update", methods=["POST"])
def battle_update():
    
    newData = request.get_json()
    renders = processNewData(newData)

    socketio.emit("newData", renders)
    
    return jsonify({'data': "received new battle info succesfully"}), 200
    

def processNewData(newData):
    global data
    tempKeys = list(newData.keys())
    player, enemy = newData.values()
    playerSprite = pb.SpriteResource('pokemon', player["pokemon"][0]["pokedexNumber"])
    enemySprite = pb.SpriteResource('pokemon', enemy["pokemon"][0]["pokedexNumber"])
    player["url"] = playerSprite.url
    enemy["url"] = enemySprite.url
    newData["player"], newData["enemy"] = newData.pop(tempKeys[0]), newData.pop(tempKeys[1])
    
    # send new renders to existing clients
    renders = {}
    renders["username"] = tempKeys[0]
    if tempKeys[0] in data:
        renders["new"] = False
    else:
        renders["new"] = True
        renders["navlink"] = render_template("usersnavlink.html", username=renders["username"])
    renders["tabpane"] = render_template("userstabpane.html", username=renders["username"], playerInfo=newData, colors=colors, counters=counters)
    
    data[tempKeys[0]] = newData
    
    return renders
