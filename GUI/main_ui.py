from flask import *
from data.database import *
from NLP.parser import process

app = Flask(__name__)

class MainGUI:
    def __init__(self, parser):
        self.parser = parser

        app.add_url_rule('/', 'index', self.index)
        app.add_url_rule('/query', 'taking_question', self.taking_question, methods=['GET', 'POST'])
        
    def run_ui(self):
        app.run(port=5000)


    def index(self):
        return render_template('index.html')


    def taking_question(self):
        if request.method == "GET":
            return redirect(url_for('index'))

        user_input = request.form.get('user_input')
        sql_results = ""
        query = ""

        if user_input:
            print("gg")
            print(self.parser)
            query = process(user_input, self.parser)
            
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