
import unittest
from flask import Flask
from ariadne.constants import PLAYGROUND_HTML
from ariadne import graphql_sync
from api import schema

class QueryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.client = self.app.test_client()
        self.app.add_url_rule(
            "/graphql", view_func=self.graphql_view
        )

    def tearDown(self):
        pass

    def graphql_view(self):
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=self.app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    def test_get_suggestion_for_text(self):
        query = '''
        query getSuggestion($text: String!) {
            getSuggestionForText(text: $text) {
                suggestion
            }
        }
        '''
        params = {
            'text': 'example text'
        }
        with self.app.test_request_context():
            response = self.client.post('/graphql', json={'query': query, 'variables': params})
            json_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', json_data)
        self.assertIn('getSuggestionForText', json_data['data'])
        self.assertIn('suggestion', json_data['data']['getSuggestionForText'])

    def test_get_answer_for_question(self):
        query = '''
        query getAnswer($question: String!) {
            getAnswerForQuestion(question: $question) {
                answer
            }
        }
        '''
        params = {
            'question': 'What is the capital of France?'
        }
        with self.app.test_request_context():
            response = self.client.post('/graphql', json={'query': query, 'variables': params})
            json_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', json_data)
        self.assertIn('getAnswerForQuestion', json_data['data'])
        self.assertIn('answer', json_data['data']['getAnswerForQuestion'])

if __name__ == '__main__':
    unittest.main()
