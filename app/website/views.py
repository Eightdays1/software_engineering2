from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from .models import Note, Item, Group, User
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


def get_current_group():
    group = Group.query.filter_by(id=current_user.group_id).first()
    return group


@views.route('/reset_db', methods=['GET'])
def reset_db():
    print('Test')
    db.drop_all()
    db.create_all()
    print('DB reset')
    return redirect(url_for('auth.login'))


@views.route('/create_demo_data', methods=['GET'])
def create_demo_data():
    db.drop_all()
    db.create_all()

    new_group = Group(name='Badstraße')
    db.session.add(new_group)
    db.session.commit()
    group = Group.query.filter_by(name='Badstraße').first()
    new_user = User(email='test@test.com',
                    group_id=group.id,
                    first_name='test',
                    password=generate_password_hash('test', method='sha256'))
    db.session.add(new_user)
    new_user2 = User(email='test2@test.com',
                     group_id=group.id,
                     first_name='test2',
                     password=generate_password_hash('test2', method='sha256'))
    db.session.add(new_user2)
    db.session.commit()

    new_item1 = Item(title='müsli', group_id=group.id, state=False)
    new_item2 = Item(title='käse', group_id=group.id, state=False)
    new_item3 = Item(title='apfel', group_id=group.id, state=False)
    new_item4 = Item(title='honig', group_id=group.id, state=False)
    db.session.add_all([new_item1, new_item2, new_item3, new_item4])
    db.session.commit()
    print('Added demo data')
    return redirect(url_for('auth.login'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print(current_user.first_name)
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
        if item.group_id == get_current_group().id:
            print("test")
            db.session.delete(item)
            db.session.commit()

    return jsonify({})


@views.route('/toggle-item', methods=['POST'])
def toggle_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item.group_id == get_current_group().id:
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
        if len(item) < 1:
            flash('Item ist too short!', category='error')
        else:
            group = get_current_group()
            new_item = Item(title=item, group_id=group.id, state=False)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added!', category='success')

    return render_template("list.html", user=current_user, group=get_current_group())


@views.route('/household', methods=['GET', 'POST'])
@login_required
def household():
    if request.method == 'POST':
        group_name = request.form.get('group-name')
        print(group_name)
        group = get_current_group()
        group.name = group_name
        db.session.commit()

    return render_template("household.html", user=current_user, group=get_current_group())


