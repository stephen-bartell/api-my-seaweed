from app.api.spots import db as spots_db
from app import surfline
from flask import Blueprint, request
from marshmallow_jsonapi import Schema, fields
from marshmallow import pre_load
from app.api.utils import ok, cant_process


FIELDS_FULL = ['id', 'spotName', 'regionName', 'windDirection', 'height',
               'windSpeed', 'tide', 'waterTempMin', 'waterTempMax']
FIELDS_BASIC = ['id', 'spotName', 'height']
FIELDS_GROUPED = ['basic']


# Schemas

class ReportSchema(Schema):
    id = fields.Int()
    height = fields.Int()
    spotName = fields.Str()
    regionName = fields.Str()
    windDirection = fields.List(fields.Int())
    windSpeed = fields.List(fields.Float())
    tide = fields.Float()
    waterTempMin = fields.Float()
    waterTempMax = fields.Float()

    class Meta:
        type_ = 'reports'

    @pre_load()
    def before_load(self, data):
        # TODO: remove the land mines. eg accessing a list
        # when it might be an object.
        result = {}
        result['height'] = data.get('Sort', {}).get('height_max')
        result['id'] = data.get('Quickspot', {}).get('spotid')
        result['spotName'] = data.get('Quickspot', {}).get('spotname')
        result['regionName'] = data.get('Quickspot', {}).get('regionname')
        result['windDirection'] = data.get('Wind', {}).get('wind_direction')[0]
        result['windSpeed'] = data.get('Wind', {}).get('wind_speed')[0]
        result['tide'] = data.get('Tide', {}).get('dataPoints')[0]['height']
        result['waterTempMin'] = data.get('WaterTemp', {}).get('watertemp_min')
        result['waterTempMax'] = data.get('WaterTemp', {}).get('watertemp_max')
        return result


def prepare_params(paramss):
    params = [p for p in paramss.split(',') if len(p)]
    errs = [p for p in params if p not in FIELDS_FULL + FIELDS_GROUPED]
    if len(errs):
        return params, errs

    # schema requires an id at all times.
    if 'id' not in params:
        params.append('id')

    return params, None



# Routes
blueprint = Blueprint('reports', __name__)


@blueprint.route('/reports', methods=['GET'])
def get_reports():

    #TODO: extract params processing to clean things up.
    fields = None
    errs = None
    if 'fields[reports]' in request.args:
        fields, errs = prepare_params(request.args['fields[reports]'])
    if errs:
        return cant_process([f'field=({field}) is invalid' for field in errs])

    # override the groupings with actual lists of fields if necessary
    if fields is None:
        fields = FIELDS_FULL
    elif 'basic' in fields:
        fields = FIELDS_BASIC

    spot_ids = [spot.spot_id for spot in spots_db.all()]
    results = surfline.fetch_spots(spot_ids)
    parsed = [{'type': 'reports', 'attributes': r.json()} for r in results]

    schema = ReportSchema(many=True, only=fields)
    data, _ = schema.load({'data': parsed})

    return ok(schema.dump(data).data)
