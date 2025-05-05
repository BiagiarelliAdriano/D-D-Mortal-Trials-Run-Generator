from flask import Flask, request, render_template, redirect, url_for
from flask_migrate import Migrate
from encounter_generator import generate_encounter, generate_divine_blessing
from models import db, Run
import json
import os

app = Flask(__name__)
uri = os.getenv("DATABASE_URL", "sqlite:///runs.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.init_app(app)
last_result = None
last_blessing = None

if os.environ.get("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def home():
    global last_result, last_blessing
    if request.method == 'POST':
        # Generate new run
        run_output = []
        for i in range(1, 40):
            run_output.append((i, generate_encounter(i)))
        last_result = run_output
        last_blessing = generate_divine_blessing()
        
        return render_template(
            'index.html',
            encounters=last_result,
            divine_blessing=last_blessing
        )
    
    return render_template('index.html', encounters=last_result)

@app.route('/save', methods=['POST'])
def save():
    global last_result, last_blessing
    title_run = request.form.get('title')
    
    if title_run and last_result and last_blessing:
        run = Run(
            title_run=title_run,
            blessing=json.dumps(last_blessing),
            encounters=json.dumps(last_result)
        )
        db.session.add(run)
        db.session.commit()
    return redirect(url_for('list_runs'))

@app.route('/runs')
def list_runs():
    runs = Run.query.all()
    return render_template('runs.html', runs=runs)

@app.route('/runs/<int:run_id>')
def view_run(run_id):
    run = Run.query.get_or_404(run_id)
    data = run.to_dict()
    return render_template(
        'index.html',
        divine_blessing=data['blessing'],
        encounters=data['encounters']
    )

if __name__ == '__main__':
    app.run(debug=True)