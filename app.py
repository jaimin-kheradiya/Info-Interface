

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Wikipedia API base URL
WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    topic = request.form.get('topic', '').strip()
    if not topic:
        return jsonify({"status": "error", "information": "Please enter a valid topic."})

    try:
        # Fetch information from Wikipedia API
        response = requests.get(WIKIPEDIA_API_URL + topic)
        if response.status_code == 200:
            data = response.json()
            # Check if the page exists
            if "extract" in data:
                return jsonify({"status": "success", "information": data["extract"]})
            else:
                return jsonify({"status": "error", "information": "No information found for this topic."})
        else:
            return jsonify({"status": "error", "information": "Could not fetch data. Please try again later."})
    except Exception as e:
        return jsonify({"status": "error", "information": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

