from flask import Flask, flash, redirect, render_template, request, jsonify
import json
import pokebase as pb


# Configure application
app = Flask(__name__)

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

players = ["escobdan"]

test4 = '{"player":{"is_player":true,"pokemon":[{"pokemonName":"Palkia","pokedexNumber":484,"primaryType":"water","secondaryType":"dragon","hp":13,"currentHealth":13,"lvl":1,"attack":7,"defence":7,"specialAttack":8,"specialDefence":7,"speed":6,"moves":[{"moveName":"waterpulse","moveDesc":"The user attacks the target with a pulsing blast of water. This may also confuse the target.","moveType":"water","movePower":60.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":20},{"moveName":"scaryface","moveDesc":"The user frightens the target with a scary face to harshly lower its Speed stat.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":10},{"moveName":"dragonbreath","moveDesc":"The user exhales a mighty gust that inflicts damage. This may also leave the target with paralysis.","moveType":"dragon","movePower":60.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":20}]}]},"enemy":{"is_player":false,"pokemon":[{"pokemonName":"Groudon","pokedexNumber":383,"primaryType":"ground","hp":13,"currentHealth":13,"lvl":1,"attack":8,"defence":7,"specialAttack":7,"specialDefence":6,"speed":7,"moves":[{"moveName":"scaryface","moveDesc":"The user frightens the target with a scary face to harshly lower its Speed stat.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":10},{"moveName":"precipiceblades","moveDesc":"The user attacks opposing Pokémon by manifesting the power of the land in fearsome blades of stone.","moveType":"ground","movePower":120.0,"moveCategory":"physical","moveAccuracy":85.0,"movePp":10},{"moveName":"mudshot","moveDesc":"The user attacks by hurling a blob of mud at the target. This also lowers the target’s Speed stat.","moveType":"ground","movePower":55.0,"moveCategory":"special","moveAccuracy":95.0,"movePp":15},{"moveName":"lavaplume","moveDesc":"The user torches everything around it in an inferno of scarlet flames. This may also leave those it hits with a burn.","moveType":"fire","movePower":80.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":15}]}]}}'
test2 = '{"player":{"is_player":true,"pokemon":[{"pokemonName":"Charmander","pokedexNumber":4,"primaryType":"fire","hp":28,"currentHealth":28,"lvl":10,"attack":18,"defence":15,"specialAttack":19,"specialDefence":13,"speed":20,"moves":[{"moveName":"smokescreen","moveDesc":"The user releases an obscuring cloud of smoke or ink. This lowers the target’s accuracy.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":20},{"moveName":"ember","moveDesc":"The target is attacked with small flames. This may also leave the target with a burn.","moveType":"fire","movePower":40.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":25},{"moveName":"scratch","moveDesc":"Hard, pointed, sharp claws rake the target to inflict damage.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":35},{"moveName":"growl","moveDesc":"The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":40}]}]},"enemy":{"is_player":false,"pokemon":[{"pokemonName":"Groudon","pokedexNumber":383,"primaryType":"ground","hp":13,"currentHealth":13,"lvl":1,"attack":8,"defence":7,"specialAttack":7,"specialDefence":6,"speed":7,"moves":[{"moveName":"scaryface","moveDesc":"The user frightens the target with a scary face to harshly lower its Speed stat.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":10},{"moveName":"precipiceblades","moveDesc":"The user attacks opposing Pokémon by manifesting the power of the land in fearsome blades of stone.","moveType":"ground","movePower":120.0,"moveCategory":"physical","moveAccuracy":85.0,"movePp":10},{"moveName":"mudshot","moveDesc":"The user attacks by hurling a blob of mud at the target. This also lowers the target’s Speed stat.","moveType":"ground","movePower":55.0,"moveCategory":"special","moveAccuracy":95.0,"movePp":15},{"moveName":"lavaplume","moveDesc":"The user torches everything around it in an inferno of scarlet flames. This may also leave those it hits with a burn.","moveType":"fire","movePower":80.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":15}]}]}}'
test3 = '{"player":{"is_player":true,"pokemon":[{"pokemonName":"Pikachu","pokedexNumber":25,"primaryType":"electric","hp":11,"currentHealth":11,"lvl":1,"attack":6,"defence":5,"specialAttack":6,"specialDefence":6,"speed":5,"moves":[{"moveName":"thundershock","moveDesc":"A jolt of electricity crashes down on the target to inflict damage. This may also leave the target with paralysis.","moveType":"electric","movePower":40.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":30},{"moveName":"tailwhip","moveDesc":"The user wags its tail cutely, making opposing Pokémon less wary and lowering their Defense stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":30},{"moveName":"sweetkiss","moveDesc":"The user kisses the target with a sweet, angelic cuteness that causes confusion.","moveType":"fairy","movePower":0.0,"moveCategory":"status","moveAccuracy":75.0,"movePp":10},{"moveName":"quickattack","moveDesc":"The user lunges at the target at a speed that makes it almost invisible. This move always goes first.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":30}]},{"pokemonName":"Charmander","pokedexNumber":4,"primaryType":"fire","hp":28,"currentHealth":28,"lvl":10,"attack":18,"defence":15,"specialAttack":19,"specialDefence":13,"speed":20,"moves":[{"moveName":"smokescreen","moveDesc":"The user releases an obscuring cloud of smoke or ink. This lowers the target’s accuracy.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":20},{"moveName":"ember","moveDesc":"The target is attacked with small flames. This may also leave the target with a burn.","moveType":"fire","movePower":40.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":25},{"moveName":"scratch","moveDesc":"Hard, pointed, sharp claws rake the target to inflict damage.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":35},{"moveName":"growl","moveDesc":"The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":40}]}]},"enemy":{"is_player":false,"pokemon":[{"pokemonName":"Doduo","pokedexNumber":84,"primaryType":"normal","secondaryType":"flying","hp":24,"currentHealth":24,"lvl":8,"attack":20,"defence":15,"specialAttack":9,"specialDefence":10,"speed":18,"moves":[{"moveName":"rage","moveDesc":"As long as this move is in use, the power of rage raises the Attack stat each time the user is hit in battle.","moveType":"normal","movePower":20.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":20},{"moveName":"quickattack","moveDesc":"The user lunges at the target at a speed that makes it almost invisible. This move always goes first.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":30},{"moveName":"peck","moveDesc":"The target is jabbed with a sharply pointed beak or horn.","moveType":"flying","movePower":35.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":35},{"moveName":"growl","moveDesc":"The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":40}]}]}}'
test1 = '{"player":{"is_player":true,"pokemon":[{"pokemonName":"Cradily","pokedexNumber":346,"primaryType":"rock","secondaryType":"grass","hp":54,"currentHealth":54,"lvl":15,"attack":27,"defence":36,"specialAttack":32,"specialDefence":42,"speed":20,"moves":[{"moveName":"ingrain","moveDesc":"The user lays roots that restore its HP on every turn. Because it’s rooted, it can’t switch out.","moveType":"grass","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":20},{"moveName":"wringout","moveDesc":"The user powerfully wrings the target. The more HP the target has, the greater the move’s power.","moveType":"normal","movePower":0.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":5},{"moveName":"wrap","moveDesc":"A long body, vines, or the like are used to wrap and squeeze the target for four to five turns.","moveType":"normal","movePower":15.0,"moveCategory":"physical","moveAccuracy":90.0,"movePp":20},{"moveName":"leechseed","moveDesc":"A seed is planted on the target. It steals some HP from the target every turn.","moveType":"grass","movePower":0.0,"moveCategory":"status","moveAccuracy":90.0,"movePp":10}]},{"pokemonName":"Charmander","pokedexNumber":4,"primaryType":"fire","hp":29,"currentHealth":29,"lvl":10,"attack":17,"defence":14,"specialAttack":22,"specialDefence":16,"speed":20,"moves":[{"moveName":"smokescreen","moveDesc":"The user releases an obscuring cloud of smoke or ink. This lowers the target’s accuracy.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":20},{"moveName":"ember","moveDesc":"The target is attacked with small flames. This may also leave the target with a burn.","moveType":"fire","movePower":40.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":25},{"moveName":"scratch","moveDesc":"Hard, pointed, sharp claws rake the target to inflict damage.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":35},{"moveName":"growl","moveDesc":"The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":40}]},{"pokemonName":"Revavroom","pokedexNumber":966,"primaryType":"steel","secondaryType":"poison","hp":286,"currentHealth":286,"lvl":99,"attack":264,"defence":203,"specialAttack":124,"specialDefence":162,"speed":212,"moves":[{"moveName":"gunkshot","moveDesc":"The user shoots filthy garbage at the target to attack. This may also poison the target.","moveType":"poison","movePower":120.0,"moveCategory":"physical","moveAccuracy":80.0,"movePp":5},{"moveName":"spinout","moveDesc":"Lowers the user\'s Speed by 2 stages.","moveType":"steel","movePower":100.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":5},{"moveName":"uproar","moveDesc":"The user attacks in an uproar for three turns. During that time, no Pokémon can fall asleep.","moveType":"normal","movePower":90.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":10},{"moveName":"poisonjab","moveDesc":"The target is stabbed with a tentacle, arm, or the like steeped in poison. This may also poison the target.","moveType":"poison","movePower":80.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":20}]}]},"enemy":{"is_player":false,"pokemon":[{"pokemonName":"Revavroom","pokedexNumber":966,"primaryType":"steel","secondaryType":"poison","hp":12,"currentHealth":12,"lvl":1,"attack":7,"defence":6,"specialAttack":6,"specialDefence":6,"speed":6,"moves":[{"moveName":"shiftgear","moveDesc":"The user rotates its gears, raising its Attack stat and sharply raising its Speed stat.","moveType":"steel","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":10},{"moveName":"poisongas","moveDesc":"A cloud of poison gas is sprayed in the face of opposing Pokémon, poisoning those it hits.","moveType":"poison","movePower":0.0,"moveCategory":"status","moveAccuracy":90.0,"movePp":40},{"moveName":"magnetrise","moveDesc":"The user levitates using electrically generated magnetism for five turns.","moveType":"electric","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":10},{"moveName":"lick","moveDesc":"The target is licked with a long tongue, causing damage. This may also leave the target with paralysis.","moveType":"ghost","movePower":30.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":30}]}]}}'
test5 = '{"player":{"is_player":true,"pokemon":[{"pokemonName":"Revavroom","pokedexNumber":966,"primaryType":"steel","secondaryType":"poison","hp":286,"currentHealth":286,"lvl":99,"attack":264,"defence":203,"specialAttack":124,"specialDefence":162,"speed":212,"moves":[{"moveName":"gunkshot","moveDesc":"The user shoots filthy garbage at the target to attack. This may also poison the target.","moveType":"poison","movePower":120.0,"moveCategory":"physical","moveAccuracy":80.0,"movePp":5},{"moveName":"spinout","moveDesc":"Lowers the user\'s Speed by 2 stages.","moveType":"steel","movePower":100.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":5},{"moveName":"uproar","moveDesc":"The user attacks in an uproar for three turns. During that time, no Pokémon can fall asleep.","moveType":"normal","movePower":90.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":10},{"moveName":"poisonjab","moveDesc":"The target is stabbed with a tentacle, arm, or the like steeped in poison. This may also poison the target.","moveType":"poison","movePower":80.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":20}]},{"pokemonName":"Charmander","pokedexNumber":4,"primaryType":"fire","hp":29,"currentHealth":29,"lvl":10,"attack":17,"defence":14,"specialAttack":22,"specialDefence":16,"speed":20,"moves":[{"moveName":"smokescreen","moveDesc":"The user releases an obscuring cloud of smoke or ink. This lowers the target’s accuracy.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":20},{"moveName":"ember","moveDesc":"The target is attacked with small flames. This may also leave the target with a burn.","moveType":"fire","movePower":40.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":25},{"moveName":"scratch","moveDesc":"Hard, pointed, sharp claws rake the target to inflict damage.","moveType":"normal","movePower":40.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":35},{"moveName":"growl","moveDesc":"The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.","moveType":"normal","movePower":0.0,"moveCategory":"status","moveAccuracy":100.0,"movePp":40}]},{"pokemonName":"Cradily","pokedexNumber":346,"primaryType":"rock","secondaryType":"grass","hp":54,"currentHealth":54,"lvl":15,"attack":27,"defence":36,"specialAttack":32,"specialDefence":42,"speed":20,"moves":[{"moveName":"ingrain","moveDesc":"The user lays roots that restore its HP on every turn. Because it’s rooted, it can’t switch out.","moveType":"grass","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":20},{"moveName":"wringout","moveDesc":"The user powerfully wrings the target. The more HP the target has, the greater the move’s power.","moveType":"normal","movePower":0.0,"moveCategory":"special","moveAccuracy":100.0,"movePp":5},{"moveName":"wrap","moveDesc":"A long body, vines, or the like are used to wrap and squeeze the target for four to five turns.","moveType":"normal","movePower":15.0,"moveCategory":"physical","moveAccuracy":90.0,"movePp":20},{"moveName":"leechseed","moveDesc":"A seed is planted on the target. It steals some HP from the target every turn.","moveType":"grass","movePower":0.0,"moveCategory":"status","moveAccuracy":90.0,"movePp":10}]}]},"enemy":{"is_player":false,"pokemon":[{"pokemonName":"Revavroom","pokedexNumber":966,"primaryType":"steel","secondaryType":"poison","hp":12,"currentHealth":12,"lvl":1,"attack":7,"defence":6,"specialAttack":6,"specialDefence":6,"speed":6,"moves":[{"moveName":"shiftgear","moveDesc":"The user rotates its gears, raising its Attack stat and sharply raising its Speed stat.","moveType":"steel","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":10},{"moveName":"poisongas","moveDesc":"A cloud of poison gas is sprayed in the face of opposing Pokémon, poisoning those it hits.","moveType":"poison","movePower":0.0,"moveCategory":"status","moveAccuracy":90.0,"movePp":40},{"moveName":"magnetrise","moveDesc":"The user levitates using electrically generated magnetism for five turns.","moveType":"electric","movePower":0.0,"moveCategory":"status","moveAccuracy":-1.0,"movePp":10},{"moveName":"lick","moveDesc":"The target is licked with a long tongue, causing damage. This may also leave the target with paralysis.","moveType":"ghost","movePower":30.0,"moveCategory":"physical","moveAccuracy":100.0,"movePp":30}]}]}}'

data = json.loads(test1)

player, enemy = data.values()

updated = True

playerSprite = pb.SpriteResource('pokemon', data["player"]["pokemon"][0]["pokedexNumber"])
enemySprite = pb.SpriteResource('pokemon', data["enemy"]["pokemon"][0]["pokedexNumber"])
player["url"] = playerSprite.url
enemy["url"] = enemySprite.url

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", player=player, enemy=enemy, colors=colors, counters=counters)


@app.route("/_update-data/", methods=["POST"])
def update_data():
    global updated
    if not updated:
        updated = True
        return jsonify({'data': render_template('index.html', player=player, enemy=enemy, colors=colors, counters=counters)}), 200
    else: 
        return jsonify({'data': True}), 200

@app.route("/battle-update", methods=["POST"])
def battle_update():
    global player
    global enemy
    global updated
    # if request.isjson:
    data = request.get_json()
    player, enemy = data.values()
    playerSprite = pb.SpriteResource('pokemon', player["pokemon"][0]["pokedexNumber"])
    enemySprite = pb.SpriteResource('pokemon', enemy["pokemon"][0]["pokedexNumber"])
    player["url"] = playerSprite.url
    enemy["url"] = enemySprite.url
    
    updated = False

    return jsonify({'data': render_template('battle.html', player=player, enemy=enemy, colors=colors, counters=counters)}), 200
    # return jsonify("successfuly received data"), 200
    # else:
    #     return jsonify({"error":"Content Type must be json"}, 400)