


from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from services.user_query import get_sql_query,execute_sql_query
from flask_cors import CORS
import os

# Load database connection details from .env file
load_dotenv()
POSTGRE_URL = os.getenv('POSTGRE_URL')


# Create SQLAlchemy engine and sessionmaker
engine = create_engine(POSTGRE_URL)
Session = sessionmaker(bind=engine)

# Create a new Flask application
app = Flask(__name__)

CORS(app)


@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data['query']
    sql_query = get_sql_query(user_query)
    return {'query': sql_query}

@app.route('/api/results', methods=['GET'])
def results():
    sql_query = request.args.get('query')  # get the SQL query from the query string
    results = execute_sql_query(sql_query)
    return jsonify({'results': results})



if __name__ == '__main__':
    app.run(debug=True)



