from elasticsearch import Elasticsearch
from config.config_handling import get_config_value
from ssl import create_default_context

def connect_elasticsearch(**kwargs):
    # context = create_default_context(cafile='./http_ca.crt')
    # _es_obj = Elasticsearch(['https://localhost:9200'],http_auth=('elastic','3ZAi5GaC4hdKLouW5OTM'), ssl_context=context)
    _es_obj = Elasticsearch(['http://localhost:9200'])
    print(_es_obj)
    if _es_obj.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es_obj

es = connect_elasticsearch()