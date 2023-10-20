import unittest
from api import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_suggestion_for_text(self):
        response = self.app.get('/api/suggestion?text=hello')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('suggestion' in data)

    def test_create_embedding(self):
        data = {'text': 'example text'}
        response = self.app.post('/api/embedding', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('embedding' in response.get_json())

    def test_create_embeddings_from_repo(self):
        data = {
            'repo_url': 'https://github.com/example/repo.git'
        }
        response = self.app.post('/api/embeddings/repo', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('embeddings' in response.get_json())


if __name__ == '__main__':
    unittest.main()
    '''
    This test case uses the `unittest` module to define a test case class `AppTestCase`. It sets up a Flask test client and defines three test methods:
        
    1. `test_get_suggestion_for_text`: Sends a GET request to the `/api/suggestion` endpoint with a query parameter `text` and asserts that the response status code is 200 and the response JSON contains a key `suggestion`.
    2. `test_create_embedding`: Sends a POST request to the `/api/embedding` endpoint with a JSON payload and asserts that the response status code is 200 and the response JSON contains a key `embedding`.
    3. `test_create_embeddings_from_repo`: Sends a POST request to the `/api/embeddings/repo` endpoint with a JSON payload and asserts that the response status code is 200 and the response JSON contains a key `embeddings`.
        
    To run the tests, you can execute the script or use a test runner like `python -m unittest <test_module_name>`. Make sure you have the necessary dependencies installed and the Flask server is running.
    '''
