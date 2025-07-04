from flask import Flask, request, render_template, redirect, url_for
from flask_migrate import Migrate
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing
from models import db, Run
import json
import os

app = Flask(__name__)
uri = os.getenv("DATABASE_URL", "sqlite:///runs.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.init_app(app)

if os.environ.get("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        run_output = list(enumerate(generate_all_encounters(39), 1))
        blessing = generate_divine_blessing()

        return render_template(
            'index.html',
            encounters=run_output,
            divine_blessing=blessing
        )
    
    # For GET request, just render empty
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    title_run = request.form.get('title')
    blessing = request.form.get('blessing')
    encounters = request.form.get('encounters')

    if title_run and blessing and encounters:
        run = Run(
            title_run=title_run,
            data=json.dumps({
                "blessing": json.loads(blessing),
                "encounters": json.loads(encounters)
            })
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
    parsed = json.loads(run.data)
    return render_template(
        'index.html',
        divine_blessing=parsed['blessing'],
        encounters=parsed['encounters']
    )

@app.route('/runs/<int:run_id>/delete', methods=['POST'])
def delete_run(run_id):
    run = Run.query.get_or_404(run_id)
    db.session.delete(run)
    db.session.commit()
    return redirect(url_for('list_runs'))

if __name__ == '__main__':
    app.run(debug=True)