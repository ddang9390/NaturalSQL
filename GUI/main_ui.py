from flask import *
from database import *
from parser import process

app = Flask(__name__)


def run_ui():
    app.run(port=5000)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/query", methods=["POST"])
def taking_question():
    user_input = request.form.get('user_input')
    sql_results = ""
    query = ""

    if user_input:
        query = process(user_input)
        
        if query:
            query, sql_results = execute_query(query)
        else:
            query = "Invalid input"

    return render_template(
        'index.html',
        user_input = user_input,
        query = query,
        sql_results = sql_results,
    )