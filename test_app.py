import unittest
import json
from app import app

class TestInventoryAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        # Reset inventory for testing
        from app import inventory, next_id
        inventory.clear()
        inventory.append({
            "id": 1,
            "name": "Test Item",
            "barcode": "123456",
            "price": 9.99,
            "quantity": 10,
            "brand": "Test Brand"
        })
        import app as app_module
        app_module.next_id = 2
    
    # Test GET all items
    def test_get_all_items(self):
        response = self.app.get('/api/inventory')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
    
    # Test GET single item
    def test_get_single_item_success(self):
        response = self.app.get('/api/inventory/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Test Item')
    
    # Test GET item not found
    def test_get_item_not_found(self):
        response = self.app.get('/api/inventory/999')
        self.assertEqual(response.status_code, 404)
    
    # Test POST create item
    def test_create_item_success(self):
        new_item = {
            "name": "New Item",
            "price": 19.99,
            "quantity": 5,
            "brand": "New Brand",
            "barcode": "789012"
        }
        response = self.app.post('/api/inventory', 
                                data=json.dumps(new_item),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'New Item')
    
    # Test PUT update item
    def test_update_item_full_success(self):
        update_data = {
            "name": "Updated Item",
            "price": 29.99,
            "quantity": 15,
            "brand": "Updated Brand"
        }
        response = self.app.put('/api/inventory/1',
                               data=json.dumps(update_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Updated Item')
    
    # Test PATCH partial update
    def test_patch_item_partial_update(self):
        patch_data = {"price": 49.99, "quantity": 20}
        response = self.app.patch('/api/inventory/1',
                                 data=json.dumps(patch_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['price'], 49.99)
        self.assertEqual(data['data']['quantity'], 20)
    
    # Test DELETE item
    def test_delete_item_success(self):
        response = self.app.delete('/api/inventory/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    # Test DELETE item not found
    def test_delete_item_not_found(self):
        response = self.app.delete('/api/inventory/999')
        self.assertEqual(response.status_code, 404)
    
    # Test external API endpoint (just check it responds)
    def test_fetch_product_endpoint(self):
        response = self.app.get('/api/fetch-product/5449000135357')
        self.assertIn(response.status_code, [200, 404, 500])
    
    # Test search endpoint
    def test_search_endpoint(self):
        response = self.app.get('/api/search-product?q=coke')
        self.assertIn(response.status_code, [200, 500])

if __name__ == '__main__':
    unittest.main()