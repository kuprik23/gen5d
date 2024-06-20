from flask import Flask, render_template_string, request, jsonify
from flaskwebgui import FlaskUI
import secrets

# Initialize a set to store previously generated numbers
generated_numbers = set()

def generate_unique_random_number():
    global generated_numbers
    
    while True:
        hex_string = secrets.token_hex(12)
        decimal_number = int(hex_string, 16)
        
        if decimal_number not in generated_numbers:
            generated_numbers.add(decimal_number)
            return decimal_number

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    number = generate_unique_random_number()
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Unique Random Number Generator</title>
    </head>
    <body>
        <h1>Your Unique Number: <span id="number">{number}</span></h1>
        <button id="generateBtn">GENERATE</button>
        <button id="copyBtn">COPY</button>

        <script>
            document.getElementById('generateBtn').addEventListener('click', function() {
                fetch('/generate', {method: 'POST'}).then(response => response.json()).then(data => {
                    document.getElementById('number').textContent = data.number;
                });
            });

            document.getElementById('copyBtn').addEventListener('click', function() {
                const number = document.getElementById('number').textContent;
                navigator.clipboard.writeText(number).then(() => {
                    alert('Number copied to clipboard');
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        </script>
    </body>
    </html>
    """, number=str(number))  # Correctly named placeholder

@app.route('/generate', methods=['POST'])
def generate():
    number = generate_unique_random_number()
    return jsonify({'number': str(number)})

if __name__ == '__main__':
    # Uncomment the following line to run as a desktop application
    # FlaskUI(app, width=500, height=300).run()
    
    # Comment the above line and uncomment the following line to run as a web application
    app.run(host='0.0.0.0', port=5000, debug=True)
