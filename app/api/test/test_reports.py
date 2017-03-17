import json
from app.api.test.utils import ApiTestCase


class GetReportsTestCase(ApiTestCase):

    def test_get_reports_full(self):
        expected_fields = ['spotName', 'regionName',
            'windDirection', 'height', 'windSpeed', 'tide',
            'waterTempMin', 'waterTempMax'
        ]
        res = self.client.get('/reports')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        for result in data['data']:
            for field in expected_fields:
                self.assertIn(field, result['attributes'])

    def test_get_reports_basic(self):
        expected_fields = ['spotName', 'height']
        res = self.client.get('/reports')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        for result in data['data']:
            for field in expected_fields:
                self.assertIn(field, result['attributes'])