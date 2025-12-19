from flask import *
from data.database import *
from data.db_utils import *
from NLP.parser import process

app = Flask(__name__)

class MainGUI:
    def __init__(self, parser):
        self.parser = parser
        self.dbs = None
        self.tables = None
        self.current_db = None

        app.add_url_rule('/', 'index', self.index)
        app.add_url_rule('/query', 'taking_question', self.taking_question, methods=['GET', 'POST'])
        
    def run_ui(self):
        app.run(port=5000)


    def index(self):
        """
        Display the homepage
        """
        self.dbs = get_available_dbs()

        self.current_db = session.get('db', self.dbs[0])

        schema = get_schema_info(self.current_db)
        self.tables = list(schema.keys())

        return render_template('index.html',
                               available_dbs = self.dbs,
                               available_tables = self.tables,
                               selected_db = self.current_db,
                               selected_table = session.get('table', 'auto'))


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
            available_dbs = self.dbs,
            available_tables = self.tables,
            selected_db = self.current_db,
            selected_table = session.get('table', 'auto')
        )
    
    @app.route("/get_tables/<db>")
    def get_tables(db):
        try:
            schema = get_schema_info(db)
            tables = list(schema.keys())

            return jsonify({'tables': tables})

        except Exception as e:
            print(e)
            return