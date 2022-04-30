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
    print("DB reset")
    return redirect(url_for('auth.login'))


@api.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)
    if note:
        if note.group_id == current_user.group_id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


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
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


@api.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item:
        if item.group_id == current_user.group_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


@api.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    event_id = event['event_id']
    event = Event.query.get(event_id)
    if event:
        if event.group_id == current_user.group_id:
            db.session.delete(event)
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


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
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


@api.route('/delete-task', methods=['POST'])
def delete_task():
    data = json.loads(request.data)
    task_id = data['task_id']
    task = Task.query.get(task_id)
    if task:
        if task.group_id == current_user.group_id:
            db.session.delete(task)
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 404


@api.route('/toggle-item', methods=['POST'])
def toggle_item():
    data = json.loads(request.data)
    item_id = data['item_id']
    item = Item.query.get(item_id)
    if item:
        if item.group_id == current_user.group_id:
            if item.state is False:
                item.state = True
            else:
                item.state = False
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 401


@api.route('/toggle-task', methods=['POST'])
def toggle_task():
    data = json.loads(request.data)
    task_id = data['task_id']
    task = Task.query.get(task_id)
    if task:
        if task.group_id == current_user.group_id:
            if task.state is False:
                task.state = True
            else:
                task.state = False
            db.session.commit()
            return jsonify({}), 200
        return jsonify({}), 401
    return jsonify({}), 401
