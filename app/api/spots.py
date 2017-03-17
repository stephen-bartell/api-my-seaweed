import json
from copy import deepcopy
from uuid import uuid4
from flask import Blueprint, request
from marshmallow_jsonapi import Schema, fields
from app.api.utils import (
    not_found, cant_process, conflict,
    ok, created, no_content)


# Models
class SpotModel:
    def __init__(self, id, spot_id, description):
        self.id = id
        self.spot_id = spot_id
        self.description = description


# Schemas
class SpotSchema(Schema):
    id = fields.Str()
    spot_id = fields.Str(required=True)
    description = fields.Str()

    class Meta:
        type_ = 'spots'


# in mem database, seeded.
class Database:
    data = [
        SpotModel(id=str(uuid4()), spot_id='4981', description='Pitas Point'),
        SpotModel(id=str(uuid4()), spot_id='49737', description='Mondos'),
        SpotModel(id=str(uuid4()), spot_id='4980', description='Emma Wood')
    ]

    def _get_data(self):
        """ Returns a copy of the data so if the user of this object
        modifies the data, we don't end up with mutations.  #referencepains
        """
        return deepcopy(self.data)

    def _get_by(self, attr, value):
        """ Returns a list filtered on an attr and it's value"""
        return [item for item in self._get_data() if getattr(item, attr) == value]

    def get_by_id(self, id):
        """ Returns a single entity from the db based on id.
        None if not found.
        """
        return next(iter(self._get_by('id', id)), None)

    def get_by_spot_id(self, spot_id):
        """ Returns a single entity from the db based on spot_id.
        None if not found.
        """
        return next(iter(self._get_by('spot_id', spot_id)), None)

    def all(self):
        return self._get_data()

    def add(self, item):
        self.data.append(item)

    def remove(self, id):
        self.data = [item for item in self.data if item.id != id]


# Routes
blueprint = Blueprint('spots', __name__)
db = Database()


@blueprint.route('/spots')
def spots_index():
    data, errs = SpotSchema(many=True).dump(db.all())
    return ok(data)


@blueprint.route('/spots/<id>')
def get_spot(id):
    models = db.get_by_id(id)
    if not models:
        return not_found(id)

    data, errs = SpotSchema().dump(models)
    return ok(data)


@blueprint.route('/spots', methods=['POST'])
def create_spot():
    schema = SpotSchema()
    payload = request.get_json()
    data, errs = schema.load(payload)
    if errs:
        return cant_process(errs)

    if 'id' not in data:
        data['id'] = str(uuid4())

    if db.get_by_id(data['id']):
        return conflict('id=({}) already exists'.format(data['id']))

    if db.get_by_spot_id(data['spot_id']):
        return conflict('spot_id=({}) already exists'.format(data['spot_id']))

    model = SpotModel(**data)
    db.add(model)
    return created(schema.dump(model).data)


@blueprint.route('/spots/<id>', methods=['DELETE'])
def remove_spot(id):
    if not db.get_by_id(id):
        return not_found(id)

    db.remove(id)
    return no_content()



