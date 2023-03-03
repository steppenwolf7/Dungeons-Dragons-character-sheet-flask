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
        name = request.form.get('name')
        class_character = request.form.get('class_character')
        race = request.form.get('race')
        strenght = request.form.get('get_data1')
        dexterity = request.form.get('get_data2')
        constitution = request.form.get('get_data3')
        intelligence = request.form.get('get_data4')
        wisdom = request.form.get('get_data5')
        charisma = request.form.get('get_data6')
        
        db = get_db()
        db.execute(
                'INSERT INTO character (character_name, character_class, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, author_id)' #columnes in data base 
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (name,class_character, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, g.user['id']) 
            )
        db.commit()
        return redirect(url_for('roll'))
    
    return render_template('dd_roller/create_character.html')  
   