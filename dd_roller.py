import random
import json
from flask import jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('dd_roller', __name__)

@bp.route('/roll')
@login_required
def roll():
    return render_template('dd_roller/roll.html', roll=roll)

@bp.route('/character', methods=('GET', 'POST'))
@login_required
def character():
    if request.method == 'POST':
        name = request.form['name']
        class_character = request.form['class_character']
        race = request.form['race']
        strenght = request.form['strenght']
        dexterity = request.form['dexterity']
        constitution = request.form['constitution']
        intelligence = request.form['intelligence']
        wisdom = request.form['wisdom']
        charisma = request.form['charisma']
        
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO character (character_name, character_class, character_race, character_strenght, character_dexterity, character_constitution, character_intelligence, character_wisdom, character_charisma, character_ author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (name, class_character, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, g.user['id'])
            )
            db.commit()
            return redirect(url_for('roll'))
    
    return render_template('dd_roller/create_character.html')  
   