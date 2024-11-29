from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from app import app, db
from checks import auth

@app.get('/')
def main():
    if 'user' in session and session['user'] != '':
        return redirect('/welcome')
    return render_template('main.html')

@app.post('/in')
def login():
    q = db.session.execute(text('select id, secret from users where nick=:a'), {
      'a': request.form['user']
    }).fetchone()

    if q and check_password_hash(q[1], request.form['secret']):
        session['user'] = q[0]

        return redirect('/welcome')

    return redirect('/')

@app.get('/out')
def logout():
    session['user'] = ''

    return redirect('/')

@app.post('/register')
def register():
    if request.form['secret'] == '':
        return redirect('/')
    
    h = generate_password_hash(request.form['secret'])

    try:
        nid = db.session.execute(text('insert into users (nick, secret) values (:a, :b) returning id'), {
          'a': request.form['user'],
          'b': h
        }).fetchone()[0]
    except IntegrityError:
        return redirect('/')

    session['user'] = nid

    db.session.commit()

    return redirect('/welcome')

@app.get('/welcome')
@auth
def welcome():
    q = db.session.execute(text('select * from messages where receiver=:a'), {
      'a': session['user']
    }).fetchall()

    return render_template('welcome.html', msgs=q)

@app.post('/message')
@auth
def message():
    q = db.session.execute(text('select id from users where nick=:a'), {
      'a': request.form['name']
    }).fetchone()

    if q:
        try:
            db.session.execute(text('insert into messages (msg, sender, receiver) values (:a, :b, :c)'), {
              'a': request.form['msg'],
              'b': session['user'],
              'c': q[0]
            })
        except IntegrityError:
            pass

    db.session.commit()

    return redirect('/welcome')

@app.post('/nick')
@auth
def nick():
    q = db.session.execute(text(f'select nick from users where id=:a'), {
      'a': request.form['id']
    }).fetchone()

    if q:
        return q[0]

    return 'ei löytynyt'

@app.post('/change')
@auth
def change():
    try:
        db.session.execute(text('update users set nick=:a where id=:b'), {
          'a': request.form['name'],
          'b': session['user']
        })
    except IntegrityError:
        pass

    db.session.commit()

    return redirect('/welcome')
