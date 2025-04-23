from flask import Flask, request, render_template
from encounter_generator import generate_encounter

app = Flask(__name__)
last_result = None

@app.route('/', methods=['GET', 'POST'])
def home():
    global last_result
    if request.method == 'POST':
        # Generate new run
        run_output = []
        for i in range(1, 40):
            run_output.append((i, generate_encounter(i)))
        last_result = run_output
        return render_template('index.html', run=last_result)
    
    return render_template('index.html', run=last_result)

if __name__ == '__main__':
    app.run(debug=True)