from flask import Flask, request
from services.user_query import get_sql_query
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data['query']
    sql_query = get_sql_query(user_query)
    return {'query': sql_query}

if __name__ == '__main__':
    app.run(debug=True)
