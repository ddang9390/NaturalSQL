from flask import *
from data.database import *
from NLP.parser import process

app = Flask(__name__)

parser = None
def run_ui(p):
    parser = p
    app.run(port=5000)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/query", methods=["GET", "POST"])
def taking_question():
    if request.method == "GET":
        return redirect(url_for('index'))

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