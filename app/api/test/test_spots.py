import json
from app.api.test.utils import ApiTestCase
from app.api.spots import db


class GetSpotsTestCase(ApiTestCase):

    def test_get_all(self):
        rv = self.client.get('/spots')
        self.assertEqual(rv.status_code, 200)

    def test_get_one_ok(self):
        test_id = db.all()[0].id
        rv = self.client.get('/spots/{}'.format(test_id))
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(data['data']['id'], test_id)

    def test_get_one_not_found(self):
        rv = self.client.get('/spots/{}'.format('foo'))
        self.assertEqual(rv.status_code, 404)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertIn('errors', data)


class CreateSpotsTestCase(ApiTestCase):
    def test_create_ok(self):
        payload = {
            'data': {
                'type': 'spots',
                'attributes': {
                    'description': 'Rincon',
                    'spot_id': '278'
                }
            }
        }
        headers = {'Content-Type': 'application/vnd.api+json'}
        rv = self.client.post('/spots', data=json.dumps(payload), headers=headers)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(data['data']['id'], db.all()[-1].id)

    def test_create_with_missing_required_attribute(self):
        payload = {
            'data': {
                'type': 'spots',
                'attributes': {
                    'description': 'Rincon',
                    # 'spot_id': '278'
                }
            }
        }
        headers = {'Content-Type': 'application/vnd.api+json'}
        rv = self.client.post('/spots', data=json.dumps(payload), headers=headers)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(rv.status_code, 422)

    def test_create_with_validation_error(self):
        payload = {
            'data': {
                'type': 'spots',
                'attributes': {
                    'description': 'Rincon',
                    'spot_id': 300 # int triggers validation error
                }
            }
        }
        headers = {'Content-Type': 'application/vnd.api+json'}
        rv = self.client.post('/spots', data=json.dumps(payload), headers=headers)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(rv.status_code, 422)

    def test_create_with_spot_id_conflict(self):
        payload = {
            'data': {
                'type': 'spots',
                'attributes': {
                    'description': 'Rincon',
                    'spot_id': '275' # spot_id will conflict
                }
            }
        }
        headers = {'Content-Type': 'application/vnd.api+json'}
        rv = self.client.post('/spots', data=json.dumps(payload), headers=headers)
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(rv.status_code, 409)

    def test_create_with_id_conflict(self):
        payload = {
            'data': {
                'id': db.all()[0].id, # this id will conflict
                'type': 'spots',
                'attributes': {
                    'description': 'Rincon',
                    'spot_id': '300' # spot_id won't conflict
                }
            }
        }
        headers = {'Content-Type': 'application/vnd.api+json'}
        rv = self.client.post('/spots', data=json.dumps(payload), headers=headers)

        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(rv.status_code, 409)


class RemoveSpotsApiTestCase(ApiTestCase):

    def test_remove_ok(self):
        test_id = db.all()[0].id
        # verify we get it
        rv = self.client.get(f'/spots/{test_id}')
        self.assertEqual(rv.status_code, 200)

        # remove it
        rv = self.client.delete(f'/spots/{test_id}')
        self.assertEqual(rv.status_code, 204)

        # verify the 404
        rv = self.client.get(f'/spots/{test_id}')
        self.assertEqual(rv.status_code, 404)

    def test_remove_not_found(self):
        rv = self.client.delete(f'/spots/foo')
        self.assertEqual(rv.status_code, 404)
