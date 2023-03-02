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
        strenght = request.form['']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO character (character_name, character_class, character_race, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (name, class_character, race, g.user['id'])
            )
            db.commit()
            return redirect(url_for('roll'))
    
    return render_template('dd_roller/create_character.html')  
   