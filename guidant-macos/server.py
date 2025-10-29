from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/screenshot', methods=['POST'])
def screenshot():
    # Define the path to save the screenshot
    screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')

    # Execute the Swift script to take a screenshot
    result = subprocess.run(['xcrun', 'swift', 'main.swift', 'screenshot', screenshot_path], capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify({'message': 'Screenshot taken successfully', 'path': screenshot_path})
    else:
        return jsonify({'error': 'Failed to take screenshot', 'details': result.stderr}), 500

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    x = data.get('x')
    y = data.get('y')

    if x is None or y is None:
        return jsonify({'error': 'x and y coordinates are required'}), 400

    # Execute the Swift script to simulate a click
    result = subprocess.run(['xcrun', 'swift', 'main.swift', 'click', str(x), str(y)], capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify({'message': f'Clicked at ({x}, {y})'})
    else:
        return jsonify({'error': 'Failed to perform click', 'details': result.stderr}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
