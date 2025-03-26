from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import requests

app = Flask(__name__)

@app.route('/')
def serve_index():
    return render_template('index.html') 

# Route for checking email breaches
@app.route('/check-breach', methods=['GET'])
def check_breach():
    email = request.args.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    url = f"https://leakcheck.io/api/public?check={email}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch data from LeakCheck API"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
