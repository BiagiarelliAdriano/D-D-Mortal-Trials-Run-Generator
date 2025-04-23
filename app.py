from flask import Flask, request, jsonify
from encounter_generator import generate_encounter

app = Flask(__name__)

@app.route('/encounter', methods=['GET'])
def get_encounter():
    try:
        encounter_number = int(request.args.get('number'))
        result = generate_encounter(encounter_number)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)