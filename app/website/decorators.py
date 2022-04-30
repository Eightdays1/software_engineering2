from functools import wraps
from .models import User
from flask_login import current_user
from flask import redirect, url_for, flash


def household_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not User.query.get(current_user.id).group_id:
            flash('Please create a household.', category="error")
            return redirect(url_for('views.household'))
        return f(*args, **kwargs)

    return wrap
