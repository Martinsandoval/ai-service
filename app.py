from api import app
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from flask import request, jsonify

from api.mutation import create_embedding, create_embeddings_from_project
from api.query import get_suggestion_for_text, get_answer_for_question

query = ObjectType("Query")
mutation = ObjectType("Mutation")

mutation.set_field("createEmbedding", create_embedding)
mutation.set_field("createEmbeddingsFromProject", create_embeddings_from_project)

query.set_field("getSuggestionForText", get_suggestion_for_text)
query.set_field("getAnswerForQuestion", get_answer_for_question)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run()

