from datetime import datetime

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

from website.models import Note, Item, Group, User, Event, Task
from website import db

import json

api = Blueprint('api', __name__, url_prefix='/api/')


@api.route('/reset_db', methods=['GET'])
def reset_db():
    db.drop_all()
    db.create_all()
    print('DB reset')
    return redirect(url_for('auth.login'))


@api.route('/create_demo_data', methods=['GET'])
def create_demo_data():
    db.drop_all()
    db.create_all()

    new_group = Group(name='Familie Müller')
    db.session.add(new_group)
    db.session.commit()
    new_user = User(email='Thomas@domain.com',
                    group_id=new_group.id,
                    first_name='Thomas',
                    password=generate_password_hash('Thomas123', method='sha256'))
    new_user2 = User(email='Sophia@domain.com',
                     group_id=new_group.id,
                     first_name='Sophia',
                     password=generate_password_hash('Sophia123', method='sha256'))
    new_user3 = User(email='Peter@domain.com',
                     group_id=new_group.id,
                     first_name='Peter',
                     password=generate_password_hash('Peter123', method='sha256'))
    db.session.add_all([new_user, new_user2, new_user3])
    db.session.commit()

    new_item1 = Item(title='Müsli', group_id=new_group.id, state=False)
    new_item2 = Item(title='Käse', group_id=new_group.id, state=False)
    new_item3 = Item(title='Apfel', group_id=new_group.id, state=False)
    new_item4 = Item(title='Honig', group_id=new_group.id, state=False)
    new_item5 = Item(title='Zucker', group_id=new_group.id, state=True)
    new_item6 = Item(title='Kaffe', group_id=new_group.id, state=True)
    db.session.add_all([new_item1, new_item2, new_item3, new_item4, new_item5, new_item6])
    db.session.commit()

    user = User.query.filter_by(first_name='Thomas').first()
    new_event = Event(title='Restmüll', group_id=new_group.id, user_id=user.id, repeat=2,
                      repeat_till=datetime(2022, 5, 26, 0, 0), color='#401902')
    new_event1 = Event(title='Wertstoff', group_id=new_group.id, repeat=1, repeat_till=datetime(2022, 5, 26, 0, 0),
                       color='green')
    db.session.add_all([new_event, new_event1])
    db.session.commit()

    new_task1 = Task(title='Schranktür reparieren', group_id=new_group.id,
                     data='Kleiderschranktür links öffnet nicht mehr richtig')
    new_task2 = Task(title='Müll rausbringen', group_id=new_group.id,
                     data='Der Müll stinkt.', user_id=user.id, date=datetime.now())
    db.session.add_all([new_task1, new_task2])
    db.session.commit()

    print('Added demo data')
    return redirect(url_for('auth.login'))


@api.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)
    if note:
        if note.group_id == current_user.get_current_group.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@api.route('/leave-group', methods=['POST'])
def leave_group():
    group = json.loads(request.data)
    group_id = group['group_id']
    group = Group.query.get(group_id)
    if group:
        if current_user in group.users:
            current_user.group_id = None
            db.session.commit()
        group = Group.query.get(group_id)
        if group.users is None:
            db.session.delete(group)
            db.session.commit()
    return jsonify({})


@api.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item:
        if item.group_id == current_user.get_current_group.id:
            db.session.delete(item)
            db.session.commit()
    return jsonify({})


@api.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    event_id = event['event_id']
    event = Event.query.get(event_id)
    if event:
        if event.group_id == current_user.get_current_group.id:
            db.session.delete(event)
            db.session.commit()
    return jsonify({})


@api.route('/delete-user', methods=['POST'])
def delete_user():
    data = json.loads(request.data)
    user_id = data['user_id']
    user = User.query.get(user_id)
    group_id = user.group_id
    if user:
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()

    group = Group.query.get(group_id)
    if group.users is None:
        db.session.delete(group)
        db.session.commit()
    return jsonify({})


@api.route('/delete-task', methods=['POST'])
def delete_task():
    data = json.loads(request.data)
    task_id = data['task_id']
    task = Task.query.get(task_id)
    if task:
        if task.group_id == current_user.get_current_group.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


@api.route('/toggle-item', methods=['POST'])
def toggle_item():
    data = json.loads(request.data)
    item_id = data['item_id']
    item = Item.query.get(item_id)
    if item.group_id == current_user.get_current_group.id:
        if item.state is False:
            item.state = True
        else:
            item.state = False
        db.session.commit()
    return jsonify({})


@api.route('/toggle-task', methods=['POST'])
def toggle_task():
    data = json.loads(request.data)
    task_id = data['task_id']
    task = Task.query.get(task_id)
    if task.group_id == current_user.get_current_group.id:
        if task.state is False:
            task.state = True
        else:
            task.state = False
        db.session.commit()
    return jsonify({})
