from flask import Flask, request, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    directory = request.form.get('directory', '').strip()
    results = []
    directory_path = os.path.join('dictionaries', directory)
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for word, definition in data.items():
                        if word.lower() == query:
                            results.append((word, definition, filename))
                            break  # Stop after finding the first match in the current file
    return jsonify(results)

@app.route('/save', methods=['POST'])
def save():
    query = request.form.get('query', '').strip().lower()
    directory = request.form.get('directory', '').strip()
    content = request.form.get('content', '').strip()
    directory_path = os.path.join('dictionaries', directory, 'vocabularies')
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{query}.html")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return jsonify({"message": "File saved successfully"})



if __name__ == '__main__':
    app.run(debug=True)
