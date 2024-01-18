#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if not animal:
        response_body = '<h1>404 animal not found</h1>'
        response = make_response(response_body,404)
        return response
    response_body = f'''
        <ul>
        <h2>ID:{animal.id}</h2>
        <h2>NAME:{animal.name}</h2>
        <h2>Species:{animal.species}</h2>
        <h2>Zookeeper:{animal.zookeeper.name}</h2>
        <h2>Enclosure:{animal.enclosure.environment}</h2>
        </ul>
    '''
    response = make_response(response_body, 200)
    
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if not zookeeper:
        response_body = '<h1>404 animal not found</h1>'
        response = make_response(response_body,404)
        return response
    response_body = f'''
        <ul>
        <h2>ID:{zookeeper.id}</h2>
        <h2>NAME:{zookeeper.name}</h2>
        <h2>Birthday:{zookeeper.birthday}</h2>
        </ul>
    '''
    animals = [animal for animal in zookeeper.animals]
    if not animals:
        response_body += f'<h2>Has no animals under their care at the moment</h2>'
    else:
        for animal in animals:
            response_body += f'<ul><h2>Animal:{animal.name}</h2></ul>'

    response = make_response(response_body,200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    if not enclosure:
        response_body = '<h1>404 enclosure not found</h1>'
        response = make_response(response_body,404)
        return response
    response_body = f'''
        <ul>
        <h2>ID:{enclosure.id}</h2>
        <h2>Environment:{enclosure.environment}</h2>
        <h2>Open to Visitors:{enclosure.open_to_visitors}</h2>
        </ul>
    '''
    animals = [animal for animal in enclosure.animals]
    if not animals:
        response_body += f'<h2>Has no animals at the moment</h2>'
    else:
        for animal in animals:
            response_body += f'<ul><h2>Animal:{animal.name}</h2></ul>'

    response = make_response(response_body,200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
