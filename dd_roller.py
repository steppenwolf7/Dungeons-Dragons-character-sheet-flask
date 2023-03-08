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
    db = get_db()
    characters = db.execute(
        'SELECT c.id, character_name, character_class, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, created, author_id, username'
        ' FROM character c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('dd_roller/roll.html', characters=characters)


@bp.route('/character', methods=('GET', 'POST'))
@login_required
def character():
    if request.method == 'POST':
        name = request.form.get('name')
        class_character = request.form.get('class_character')
        race = request.form.get('race')
        strenght = request.form.get('strenght')
        dexterity = request.form.get('dexterity')
        constitution = request.form.get('constitution')
        intelligence = request.form.get('intelligence')
        wisdom = request.form.get('wisdom')
        charisma = request.form.get('charisma')
        error = None

        if not name:
            error = 'Name is required.'
        if not strenght:
            error = 'Attributes are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # columnes in data base
                'INSERT INTO character (character_name, character_class, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (name, class_character, race, strenght, dexterity,
                 constitution, intelligence, wisdom, charisma, g.user['id'])
            )
            db.commit()
        return redirect(url_for('roll'))

    return render_template('dd_roller/create_character.html')


def get_character(id, check_author=True):  # checking if author of post is logged in
    character = get_db().execute(
        'SELECT c.id, character_name, character_class, race, strenght, dexterity, constitution, intelligence, wisdom, charisma, author_id'
        ' FROM character c JOIN user u ON c.author_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if character is None:
        abort(404, f"charcter id {id} doesn't exist.")

    if check_author and character['author_id'] != g.user['id']:
        abort(403)

    return character


@bp.route('/delete', methods=('POST',))
@login_required
def delete():
    id = request.form['id']
    character = get_character(id, check_author=False)
    
    if character['author_id'] != g.user['id']:
        flash('This is not your character')
    else:    
        db = get_db()
        db.execute('DELETE FROM character WHERE id = ?', (id,))
        db.commit()
        flash('Character deleted')
    return redirect(url_for('roll'))
