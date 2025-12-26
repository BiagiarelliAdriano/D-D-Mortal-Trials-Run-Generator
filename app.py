from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing
from models import db, Run, Character
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/characters-hub')
def characters_hub():
    characters = Character.query.all()
    return render_template('characters.html', characters=characters)

@app.route('/characters/create', methods=['POST'])
def create_character():
    data = request.form
    character_data = {
        "class_name": data.get("class_name"),
        "subclass": data.get("subclass"),
        "level": int(data.get("level"))
    }

    character = Character(name=data.get("name"))
    character.set_data(character_data)

    db.session.add(character)
    db.session.commit()

    return jsonify({
        "id": character.id,
        "name": character.name,
        "class_name": character_data["class_name"],
        "subclass": character_data["subclass"],
        "level": character_data["level"]
    })

@app.route('/characters/<int:char_id>')
def view_character(char_id):
    character = Character.query.get_or_404(char_id)
    character_data = json.loads(character.data)
    return render_template(
        'character_sheet.html',
        character=character,
        character_data=character_data,
        editable=False
    )

@app.route('/characters/<int:char_id>/edit', methods=['GET', 'POST'])
def edit_character(char_id):
    character = Character.query.get_or_404(char_id)
    if request.method == 'POST':
        character.name = request.form.get('name')
        updated_data = {
            "class_name": request.form.get('class_name'),
            "subclass": request.form.get('subclass'),
            "level": int(request.form.get('level'))
        }
        character.set_data(updated_data)
        db.session.commit()
        return redirect(url_for('characters_hub'))
    return render_template('character_sheet.html', character=character, editable=True)

@app.route('/characters/<int:char_id>/delete', methods=['POST'])
def delete_character(char_id):
    character = Character.query.get_or_404(char_id)
    db.session.delete(character)
    db.session.commit()
    return redirect(url_for('characters_hub'))

@app.route('/run-generator', methods=['GET', 'POST'])
def run_generator():
    if request.method == 'POST':
        run_output = list(enumerate(generate_all_encounters(39), 1))
        blessing = generate_divine_blessing()

        return render_template(
            'run_generator.html',
            encounters=run_output,
            divine_blessing=blessing
        )
    
    return render_template('run_generator.html')

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
        'run_generator.html',
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
