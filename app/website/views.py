from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Item
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note ist too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item:
        if item.user_id == current_user.id:
            print("test")
            db.session.delete(item)
            db.session.commit()

    return jsonify({})


@views.route('/toggle-item', methods=['POST'])
def toggle_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item.user_id == current_user.id:
        if item.state is False:
            item.state = True
        else:
            item.state = False
        db.session.commit()

    return jsonify({})


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@views.route('/list', methods=['GET', 'POST'])
@login_required
def shoppinglist():
    if request.method == 'POST':
        item = request.form.get('item_textfield')
        print(item)
        if len(item) < 1:
            flash('Item ist too short!', category='error')
        else:
            new_item = Item(title=item, user_id=current_user.id, state=False)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added!', category='success')

    return render_template("list.html", user=current_user)

