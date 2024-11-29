from functools import wraps
from flask import request, redirect

def auth(f):
    @wraps(f)
    def is_signed_in(*a, **b):
        if not 'user' in request.cookies or request.cookies['user'] == '':
            return redirect('/')
        return f(*a, **b)
    return is_signed_in
