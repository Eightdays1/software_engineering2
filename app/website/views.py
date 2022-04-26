from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from datetime import datetime
from datetime import timedelta
from .models import Note, Item, Group, User, Event
from . import db
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


def get_current_group():
    group = Group.query.filter_by(id=current_user.group_id).first()
    return group


def change_group_name(group_name):
    group = get_current_group()
    group.name = group_name
    db.session.commit()


def create_new_group(new_group_name):
    new_uuid = str(uuid.uuid4())
    new_group = Group(name=new_group_name, uuid=new_uuid)
    db.session.add(new_group)
    db.session.commit()
    new_group = Group.query.filter_by(uuid=new_uuid).first()
    current_user.group_id = new_group.id
    db.session.commit()


def change_email(email):
    if User.query.filter_by(email=email).first() is not None:
        flash('Email already exists.', category='error')
    else:
        current_user.email = email
        db.session.commit()
        flash('Email changed.', category='success')


def change_name(name):
    current_user.first_name = name
    db.session.commit()
    flash('Name changed.', category='success')


def change_password(old_password1, old_password2, new_password):
    if old_password1 is None:
        flash('Please enter your current password.', category='error')
    elif old_password2 is None:
        flash('Please confirm your current password.', category='error')
    elif old_password1 != old_password2:
        flash('Passwords do not match.', category='error')
    elif current_user.check_password(old_password1) is False:
        flash('Wrong password.', category='error')
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Password changed.', category='success')


def add_user_to_group(email):
    if email is not None:
        user_to_add = User.query.filter_by(email=email).first()
        group = get_current_group()
        if current_user.group_id != group.id:
            flash('Permission denied! You are not a member of this group.', category='error')
        elif user_to_add is None:
            flash('User does not exist. (or email is wrong.)', category='error')
        elif user_to_add.group_id is not None:
            if user_to_add.group_id == group.id:
                flash('User ist already in this group.', category='error')
            else:
                flash('User ist already in a group.', category='error')
        else:
            user_to_add.group_id = group.id
            db.session.commit()


@views.route('/reset_db', methods=['GET'])
def reset_db():
    db.drop_all()
    db.create_all()
    print('DB reset')
    return redirect(url_for('auth.login'))


@views.route('/print_db', methods=['GET'])
def print_db():
    print("Current User:" + current_user.first_name)
    if current_user.group_id is None:
        print("User has no group")
    else:
        print("Current Usergroupid:" + current_user.group_id)
    users = Group.query.filter_by(name='Badstraße').first().users
    for user in users:
        print('User in group:' + user.first_name)
    return redirect(url_for('views.home'))


@views.route('/create_demo_data', methods=['GET'])
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
    new_event = Event(title='Restmüll', group_id=group.id, user_id=user.id, repeat=2, repeat_till=datetime(2022, 5, 26, 0, 0), color='#401902')
    new_event1 = Event(title='Wertstoff', group_id=group.id, repeat=1, repeat_till=datetime(2022, 5, 26, 0, 0), color='green')
    db.session.add_all([new_event, new_event1])
    db.session.commit()

    print('Added demo data')
    return redirect(url_for('auth.login'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('views.dashboard'))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/leave-group', methods=['POST'])
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


@views.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    item_id = item['item_id']
    item = Item.query.get(item_id)
    if item:
        if item.group_id == get_current_group().id:
            db.session.delete(item)
            db.session.commit()

    return jsonify({})


@views.route('/delete-user', methods=['POST'])
def delete_user():
    print("test1")
    data = json.loads(request.data)
    user_id = data['user_id']
    user = User.query.get(user_id)
    group_id = user.group_id
    if user:
        print(user.id, current_user.id)
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()

    group = Group.query.get(group_id)
    if group.users is None:
        db.session.delete(group)
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
    return render_template("dashboard.html", current_user=current_user)


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

    return render_template("list.html", current_user=current_user, group=get_current_group())


@views.route('/household', methods=['GET', 'POST'])
@login_required
def household():
    if request.method == 'POST':
        group_name = request.form.get('group-name')
        new_group_name = request.form.get('new-group-name')
        add_user_email = request.form.get('add-user-email')
        if group_name is not None:
            change_group_name(group_name)
        elif new_group_name is not None:
            create_new_group(new_group_name)
        elif add_user_email is not None:
            add_user_to_group(add_user_email)
    return render_template("household.html", current_user=current_user, group=get_current_group())


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email_address')
        name = request.form.get('first_name')
        old_password1 = request.form.get('old_password1')
        old_password2 = request.form.get('old_password2')
        new_password = request.form.get('new_password')
        if email is not None:
            change_email(email)
        elif name is not None:
            change_name(name)
        if (old_password1 or old_password2 or new_password) is not None:
            change_password(old_password1, old_password2, new_password)
    return render_template("profile.html", current_user=current_user, group=get_current_group())


@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    event_list = Event.query.filter_by(group_id=current_user.group_id).all()
    events = []
    for event in event_list:
        if event.user_id:
            user = User.query.filter_by(id=event.user_id).first()
            user_name = ' (' + user.first_name + ')'
        else:
            user_name = ''
        if event.repeat > 0:
            date = event.start
            date_end = event.end
            while event.repeat_till > date:
                element = {
                    'id': event.id,
                    'title': event.title + user_name,
                    'start': date.strftime("%Y-%m-%d"),
                    'end': date_end.strftime("%Y-%m-%d"),
                    'color': event.color
                }
                events.append(element)
                date = date + timedelta(days=(7*event.repeat))
                date_end = date_end + timedelta(days=(7*event.repeat))
        else:
            element = {
                    'id': event.id,
                    'title': event.title + user_name,
                    'start': event.start,
                    'end': event.end,
                    'color': event.color
                }
            events.append(element)

    return render_template("calendar.html", current_user=current_user, group=get_current_group(), events=events)
