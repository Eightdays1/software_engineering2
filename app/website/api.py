from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user

from datetime import datetime
from .models import Note, Item, Group, User, Event, Task
from .views import get_current_group
from . import db
import json
import uuid
from werkzeug.security import generate_password_hash

api = Blueprint('api', __name__, url_prefix='/api/')


@api.route('/reset_db', methods=['GET'])
def reset_db():
    db.drop_all()
    db.create_all()
    print('DB reset')
    return redirect(url_for('auth.login'))


@api.route('/print_db', methods=['GET'])
def print_db():
    for i in range(20):
        event = Event.query.filter_by(id=i).first()
        if event:
            print('Event:' + str(event.title) + ',' + str(event.start) + ',' + str(event.end))
    return redirect(url_for('views.dashboard'))


@api.route('/create_demo_data', methods=['GET'])
def create_demo_data():
    db.drop_all()
    db.create_all()

    new_uuid = str(uuid.uuid4())
    new_group = Group(name='Badstraße', uuid=new_uuid)
    db.session.add(new_group)
    db.session.commit()
    group = Group.query.filter_by(uuid=new_uuid).first()
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
    new_user3 = User(email='test3@test.com',
                     first_name='test3',
                     password=generate_password_hash('test3', method='sha256'))
    db.session.add(new_user3)
    db.session.commit()

    new_item1 = Item(title='müsli', group_id=group.id, state=False)
    new_item2 = Item(title='käse', group_id=group.id, state=False)
    new_item3 = Item(title='apfel', group_id=group.id, state=False)
    new_item4 = Item(title='honig', group_id=group.id, state=False)
    db.session.add_all([new_item1, new_item2, new_item3, new_item4])
    db.session.commit()

    user = User.query.filter_by(first_name='test').first()
    new_event = Event(title='Restmüll', group_id=group.id, user_id=user.id, repeat=2,
                      repeat_till=datetime(2022, 5, 26, 0, 0), color='#401902')
    new_event1 = Event(title='Wertstoff', group_id=group.id, repeat=1, repeat_till=datetime(2022, 5, 26, 0, 0),
                       color='green')
    db.session.add_all([new_event, new_event1])
    db.session.commit()

    new_task1 = Task(title='Schranktür reparieren', group_id=group.id,
                     data='Kleiderschranktür links öffnet nicht mehr richtig')
    new_task2 = Task(title='Müll rausbringen', group_id=group.id,
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
        if note.user_id == current_user.id:
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
        if item.group_id == get_current_group().id:
            db.session.delete(item)
            db.session.commit()
    return jsonify({})


@api.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    event_id = event['event_id']
    event = Event.query.get(event_id)
    if event:
        if event.group_id == get_current_group().id:
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
        if task.group_id == get_current_group().id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


@api.route('/toggle-item', methods=['POST'])
def toggle_item():
    data = json.loads(request.data)
    item_id = data['item_id']
    item = Item.query.get(item_id)
    if item.group_id == get_current_group().id:
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
    if task.group_id == get_current_group().id:
        if task.state is False:
            task.state = True
        else:
            task.state = False
        db.session.commit()
    return jsonify({})
