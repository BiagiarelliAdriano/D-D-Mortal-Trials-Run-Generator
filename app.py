from flask import Flask, request, render_template
from encounter_generator import generate_encounter, generate_divine_blessing

app = Flask(__name__)
last_result = None
last_blessing = None

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

if __name__ == '__main__':
    app.run(debug=True)