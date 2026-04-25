import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_all(self):
        r = self.app.get('/inventory')
        self.assertEqual(r.status_code, 200)
    
    def test_create(self):
        r = self.app.post('/inventory', 
                         data=json.dumps({"name": "Tea", "price": 2.99, "quantity": 20}),
                         content_type='application/json')
        self.assertEqual(r.status_code, 201)
    
    def test_get_one(self):
        r = self.app.get('/inventory/1')
        self.assertEqual(r.status_code, 200)
    
    def test_update(self):
        r = self.app.put('/inventory/1',
                        data=json.dumps({"price": 5.99}),
                        content_type='application/json')
        self.assertEqual(r.status_code, 200)
    
    def test_delete(self):
        r = self.app.delete('/inventory/2')
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()