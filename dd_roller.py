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
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
        return render_template('dd_roller/create_character.html')  
   