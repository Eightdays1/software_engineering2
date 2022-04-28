from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from datetime import datetime
from datetime import timedelta
from .models import Note, Item, Group, User, Event, Task
from . import db
import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


def get_current_group():
    group = Group.query.filter_by(id=current_user.group_id).first()
    return group


def create_new_group(new_group_name):
    new_uuid = str(uuid.uuid4())
    new_group = Group(name=new_group_name, uuid=new_uuid)
    db.session.add(new_group)
    db.session.commit()
    new_group = Group.query.filter_by(uuid=new_uuid).first()
    current_user.group_id = new_group.id
    db.session.commit()


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


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('views.dashboard'))


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


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        title = request.form.get('title_input')
        user_id = request.form.get('user_input')
        date = request.form.get('date_input')
        data = request.form.get('data_input')
        if date:
            date = datetime.strptime(date, "%Y-%m-%d")
        if task_id:
            task = Task.query.get(task_id)
            if title != '':
                task.title = title
                if user_id != "0":
                    task.user_id = user_id
                else:
                    task.user_id = None
                if date:
                    task.date = date
                task.data = data
            else:
                flash('Title can´t be empty.', category='error')
        else:
            if title == '':
                flash('Please enter a title.', category='error')
            else:
                group_id = get_current_group().id
                new_task = Task(title=title, group_id=group_id, date=date, data=data)
                if user_id != "0":
                    new_task.user_id = user_id
                db.session.add(new_task)
                db.session.commit()

    users_list = User.query.filter_by(group_id=get_current_group().id).all()
    task_list = Task.query.filter_by(group_id=get_current_group().id).all()

    tasks_structured = []
    for task in task_list:
        element = {
            'id': task.id,
            'title': task.title,
            'data': task.data,
            'state': task.state
        }
        if task.user_id:
            user = User.query.filter_by(id=task.user_id).first()
            element['user_name'] = user.first_name
            element['user_id'] = user.id
        if task.date:
            date = task.date.date()
            element['date'] = date
        tasks_structured.append(element)

    return render_template("tasks.html", tasks=tasks_structured, users_in_group=users_list, current_user=current_user, group=get_current_group())


@views.route('/household', methods=['GET', 'POST'])
@login_required
def household():
    if request.method == 'POST':
        group_name = request.form.get('group-name')
        new_group_name = request.form.get('new-group-name')
        add_user_email = request.form.get('add-user-email')
        if group_name is not None:
            if get_current_group().change_group_name(group_name) is True:
                flash('Changed name of the group successfully.', category='success')
        elif new_group_name is not None:
            create_new_group(new_group_name)
        elif add_user_email is not None:
            add_user_to_group(add_user_email)
        db.session.commit()
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
            result = current_user.change_email(email)
            if result is True:
                flash('Email changed successfully.', category='success')
            else:
                flash('Email exists already.', category='error')
        elif name is not None:
            current_user.change_name(name)
            flash('Name changed.', category='success')
        elif (old_password1 or old_password2 or new_password) is not None:
            if old_password1 is None:
                flash('Please enter your current password.', category='error')
            elif old_password2 is None:
                flash('Please confirm your current password.', category='error')
            elif old_password1 != old_password2:
                flash('Passwords do not match.', category='error')
            elif current_user.check_password(old_password1) is False:
                flash('Wrong password.', category='error')
            else:
                current_user.change_pasword(new_password)
                db.session.commit()
                flash('Password changed.', category='success')
        db.session.commit()
    return render_template("profile.html", current_user=current_user, group=get_current_group())


@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    if request.method == 'POST':
        title = request.form.get('title_input')
        user_id = request.form.get('user_input')
        start_date = request.form.get('start_input')
        end_date = request.form.get('end_input')
        repeat = request.form.get('repeat_input')
        repeat_till = request.form.get('repeat-till_input')
        color = request.form.get('color_input')

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date > end_date:
            flash('End date needs to be after start date!', category='error')
        elif title == '':
            flash('Please enter a title.', category='error')
        else:
            new_uuid = str(uuid.uuid4())
            group_id = get_current_group().id
            new_event = Event(title=title, group_id=group_id,
                              uuid=new_uuid, repeat=repeat,
                              start=start_date, end=end_date, color=color)
            db.session.add(new_event)
            db.session.commit()
            if user_id != "0":
                new_event.user_id = user_id
            if repeat_till:
                repeat_till = datetime.strptime(repeat_till, "%Y-%m-%d")
            new_event.repeat_till = repeat_till
            db.session.commit()

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
    task_list = Task.query.filter_by(group_id=get_current_group().id).all()
    for task in task_list:
        if task.date:
            if task.user_id:
                user_name = User.query.get(task.user_id).first_name
            else:
                user_name = ''
            element = {
                'id': event_list[-1].id + 1,
                'title': task.title + ' (' + user_name + ')',
                'start': task.date,
                'end': task.date,
                'color': 'grey'
            }
            events.append(element)


    return render_template("calendar.html", current_user=current_user, group=get_current_group(), events=events)
