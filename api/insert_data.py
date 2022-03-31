from app import app
from api.elastic_test import connect_elasticsearch
from flask import request, jsonify, make_response

es = connect_elasticsearch()

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.form['id']
    first_name = request.form['fname']
    last_name = request.form['lname']
    job = request.form['job']

    user_obj = {
        'id': user_id,
        'name': '{} {}'.format(first_name, last_name),
        'job': '{}'.format(job)
    }

    result = es.index(index='user', id=user_id, body=user_obj, request_timeout=30)
    print(result)
    return make_response(jsonify({'status': result['_shards']['successful']}), 201)