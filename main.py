from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        locations_file = request.files.get('locations')
        metadata_file = request.files.get('metadata')

        if not locations_file or not metadata_file:
            return jsonify({"error": "Both JSON files are required"}), 400

        locations = json.load(locations_file)
        metadata = json.load(metadata_file)

        data_map = {entry["id"]: entry for entry in locations}
        for entry in metadata:
            if entry["id"] in data_map:
                data_map[entry["id"]].update(entry)
            else:
                data_map[entry["id"]] = entry

        merged_data = list(data_map.values())

        type_counts = {}
        rating_sums = {}
        rating_counts = {}
        max_reviews = -1
        most_reviewed_location = None
        incomplete_data = []

        for entry in merged_data:
            has_complete_data = all(key in entry for key in ["id", "type", "rating", "reviews", "latitude", "longitude"])
            if not has_complete_data:
                incomplete_data.append(entry["id"])
                continue

            type_counts[entry["type"]] = type_counts.get(entry["type"], 0) + 1
            rating_sums[entry["type"]] = rating_sums.get(entry["type"], 0) + entry["rating"]
            rating_counts[entry["type"]] = rating_counts.get(entry["type"], 0) + 1

            if entry["reviews"] > max_reviews:
                max_reviews = entry["reviews"]
                most_reviewed_location = entry

        avg_ratings = {t: rating_sums[t] / rating_counts[t] for t in rating_sums}

        response = {
            "valid_points_per_type": type_counts,
            "average_rating_per_type": avg_ratings,
            "most_reviewed_location": most_reviewed_location,
            "incomplete_data": incomplete_data
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
