from flask import Flask, Response, request
from paycom import Paycom
import os
from cachetools import cached, LRUCache, TTLCache

code = os.environ['paycom_code']
username = os.environ['paycom_username']
password = os.environ['paycom_password']
securityquestion = os.environ['paycom_question']

app = Flask(__name__)

cache = TTLCache(maxsize=1024, ttl=1800)

def cached_usage(target):
    if not target in cache:
        cache[target] = Response(Paycom().getLastSync(username, password, code, securityquestion, target), mimetype='text/plain')
    
    return cache[target]

@app.route('/')
def landing_page():
    return '<h1>Paycom Exporter</h1><a href="/metrics">/metrics</a>'

@app.route('/metrics/')
def get_usage():
    target = request.args.get('target')
    print(target)
    if target is not None:
        return cached_usage(target)
    else:
        return Response("Invalid request, add target parameter.", mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9770)