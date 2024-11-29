from functools import wraps
from flask import redirect, session

def auth(f):
    @wraps(f)
    def is_signed_in(*a, **b):
        if not 'user' in session or session['user'] == '':
            return redirect('/')
        return f(*a, **b)
    return is_signed_in
