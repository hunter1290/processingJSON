from flask import Flask, request, jsonify
from task import process_json_task
import json

app = Flask(__name__)

@app.route('/process-json', methods=['POST'])
def process_json():
    try:
        # Read uploaded files
        locations_file = request.files['locations']
        metadata_file = request.files['metadata']

        # Convert to JSON strings
        locations_json = json.dumps(json.load(locations_file))
        metadata_json = json.dumps(json.load(metadata_file))

        # Send task to Celery queue
        task = process_json_task.apply_async(args=[locations_json, metadata_json])

        return jsonify({"task_id": task.id, "status": "Processing..."}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/task-status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task_result = process_json_task.AsyncResult(task_id)
    
    if task_result.state == "PENDING":
        return jsonify({"task_id": task_id, "status": "Pending"}), 200
    elif task_result.state == "SUCCESS":
        return jsonify({"task_id": task_id, "status": "Completed", "result": task_result.result}), 200
    else:
        return jsonify({"task_id": task_id, "status": task_result.state}), 200

if __name__ == '__main__':
    app.run(debug=True)
