from app import app
from api.elastic_test import connect_elasticsearch
from flask import jsonify, request, make_response

es = connect_elasticsearch()

index_name = 'employee'

def insert_or_update(request):
    nik = request.form['nik']
    employee_dict = {
        'nik': nik, 'name': request.form['name'], 'address': request.form['address'], 'position': request.form['position'],
        'division': request.form['division'], 'company': request.form['company']
    }
    result = es.index(index=index_name, id=nik, body=employee_dict)
    print(result)
    is_success = result['_shards']['successful']
    message = 'Success' if is_success else 'Failed'
    return make_response(jsonify({'status_code': is_success, 'message': message}), 201)

@app.route('/employees', methods=['POST', 'GET', 'PUT', 'DELETE'])
def employees():
    if request.method == 'POST':
        return insert_or_update(request)
    elif request.method == 'GET':
        nik = request.args.get('nik')
        results = es.get(index=index_name, id=nik)
        print(results)
        return make_response(jsonify(results['_source']), 200)
    elif request.method == 'PUT':
        return insert_or_update(request)
    elif request.method == 'DELETE':
        nik = request.args.get('nik')
        result = es.delete(index=index_name, id=nik)
        print(result)
        return make_response(jsonify({'status_code': 1}), 200)


@app.route('/employees/searching', methods=['POST'])
def employees_searching():
    keyword = request.form['keyword']
    query_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "nik": keyword
                        }
                    },
                    {
                        "match": {
                            "name": keyword
                        }
                    },
                    {
                        "match": {
                            "division": keyword
                        }
                    },
                ]
            }
        }
    }

    result = es.search(index=index_name, body=query_body)
    print(result)
    
    return make_response(jsonify(result['hits']['hits']), 200)