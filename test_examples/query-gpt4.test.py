
import unittest
from ariadne import graphql_sync
from flask import Flask

# Assuming the schema and app are defined in the api package as shown in the context
from api import schema, app

class QueryTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def execute_query(self, query_string, variables=None):
        return graphql_sync(
            schema,
            {
                'query': query_string,
                'variables': variables
            },
            context_value=request,
            debug=app.debug
        )

    def test_get_suggestion_for_text(self):
        query_string = '''
        query GetSuggestion($inputText: String!) {
            getSuggestionForText(text: $inputText) {
                suggestion
            }
        }
        '''
        variables = {'inputText': 'sample text'}
        result = self.execute_query(query_string, variables)
        self.assertTrue(result[0]['data']['getSuggestionForText']['suggestion'] is not None)
        self.assertEqual(result[1], 200)

    def test_get_answer_for_question(self):
        query_string = '''
        query GetAnswer($question: String!) {
            getAnswerForQuestion(question: $question) {
                answer
            }
        }
        '''
        variables = {'question': 'What is the meaning of life?'}
        result = self.execute_query(query_string, variables)
        self.assertTrue(result[0]['data']['getAnswerForQuestion']['answer'] is not None)
        self.assertEqual(result[1], 200)

if __name__ == '__main__':
    unittest.main()
