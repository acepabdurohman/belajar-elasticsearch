from crypt import methods
from app import app
from api.elastic_test import connect_elasticsearch
from flask import request, jsonify, make_response

es = connect_elasticsearch()

@app.route('/get_user/<user_id>', methods=['GET'])
def home(user_id):
    results = es.get(index='user', id=user_id)
    print(results)
    return make_response(jsonify(results['_source']), 200)


@app.route('/search_user', methods=['POST'])
def search_user():
    keyword = request.form['keyword']
    query_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "name": keyword
                        }
                    },
                    {
                        "match": {
                            "id": keyword
                        }
                    },
                    {
                        "match": {
                            "job": keyword
                        }
                    },
                ]
            }
        }
    }

    result = es.search(index='user', body=query_body)
    print(result)
    
    return make_response(jsonify(result['hits']['hits']), 200)