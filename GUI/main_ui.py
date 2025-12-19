from flask import *
from data.database import *
from data.db_utils import *
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
        """
        Display the homepage
        """
        dbs = get_available_dbs()

        current_db = session.get('db', dbs[0])


        return render_template('index.html',
                               available_dbs = dbs,
                               selected_db = current_db)


    def taking_question(self):
        """
        Takes the user input and process it
        """
        if request.method == "GET":
            return redirect(url_for('index'))

        user_input = request.form.get('user_input')
        sql_results = ""
        query = ""

        if user_input:
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
    
    @app.route("/get_tables/<db>")
    def get_tables(db):
        try:
            schema = get_schema_info()
            tables = list(schema.keys())

            return jsonify({'tables': tables})

        except Exception as e:
            print(e)
            return