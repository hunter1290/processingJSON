import json

def process_map_data():
    # 1. Load and parse the JSON files
    try:
        # For demo purposes, I'm hardcoding the JSON data as provided in the assignment
        # In a real scenario, you would load from files
        locations_data = [
            {"id": "loc_01", "latitude": 37.7749, "longitude": -122.4194},
            {"id": "loc_04", "latitude": 27.8749, "longitude": 122.4194},
            {"id": "loc_05", "latitude": 57.2749, "longitude": -112.4344},
            {"id": "loc_06", "latitude": 14.0522, "longitude": -119.2531},
            {"id": "loc_07", "latitude": 64.0522, "longitude": -108.2330},
            {"id": "loc_02", "latitude": 34.0522, "longitude": -118.2437},
            {"id": "loc_08", "latitude": 24.0522, "longitude": -168.2197},
            {"id": "loc_03", "latitude": 40.7128, "longitude": -74.0060}
        ]
        
        metadata = [
            {"id": "loc_01", "type": "restaurant", "rating": 4.5, "reviews": 120},
            {"id": "loc_04", "type": "restaurant", "rating": 4.1, "reviews": 500},
            {"id": "loc_05", "type": "restaurant", "rating": 3.7, "reviews": 110},
            {"id": "loc_02", "type": "hotel", "rating": 4.2, "reviews": 200},
            {"id": "loc_06", "type": "hotel", "rating": 4.0, "reviews": 700},
            {"id": "loc_07", "type": "hotel", "rating": 2.0, "reviews": 900},
            {"id": "loc_03", "type": "cafe", "rating": 4.7, "reviews": 150},
            {"id": "loc_08", "type": "cafe", "rating": 4.5, "reviews": 750}
        ]
        
        # Alternative file loading approach (commented out)
        # with open('locations.json', 'r') as locations_file:
        #     locations_data = json.load(locations_file)
        # with open('metadata.json', 'r') as metadata_file:
        #     metadata = json.load(metadata_file)
            
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return
    
    # 2. Merge the data based on matching id
    merged_data = []
    locations_dict = {location['id']: location for location in locations_data}
    metadata_dict = {meta['id']: meta for meta in metadata}
    
    # Find all unique IDs from both datasets
    all_ids = set(locations_dict.keys()) | set(metadata_dict.keys())
    
    # Merge data and identify locations with incomplete data
    incomplete_data = []
    for id in all_ids:
        location_info = locations_dict.get(id, {})
        meta_info = metadata_dict.get(id, {})
        
        # Check if data is complete
        if id not in locations_dict or id not in metadata_dict:
            incomplete_data.append(id)
            
        # Create merged entry with all available data
        merged_entry = {"id": id}
        merged_entry.update(location_info)
        merged_entry.update(meta_info)
        merged_data.append(merged_entry)
    
    # 3. Count valid points per type
    # Valid points are those with complete location and metadata information
    valid_data = [entry for entry in merged_data if 
                 'latitude' in entry and 'longitude' in entry and 
                 'type' in entry and 'rating' in entry and 'reviews' in entry]
    
    type_counts = {}
    for entry in valid_data:
        location_type = entry['type']
        type_counts[location_type] = type_counts.get(location_type, 0) + 1
    
    # 4. Calculate average rating per type
    type_ratings = {}
    for entry in valid_data:
        location_type = entry['type']
        if location_type not in type_ratings:
            type_ratings[location_type] = {'sum': 0, 'count': 0}
        type_ratings[location_type]['sum'] += entry['rating']
        type_ratings[location_type]['count'] += 1
    
    avg_ratings = {
        location_type: round(data['sum'] / data['count'], 2) 
        for location_type, data in type_ratings.items()
    }
    
    # 5. Identify location with highest number of reviews
    max_reviews = 0
    max_reviews_location = None
    
    for entry in valid_data:
        if 'reviews' in entry and entry['reviews'] > max_reviews:
            max_reviews = entry['reviews']
            max_reviews_location = entry['id']
    
    # Prepare and print the results
    results = {
        "valid_points_per_type": type_counts,
        "average_rating_per_type": avg_ratings,
        "highest_reviews_location": {
            "id": max_reviews_location,
            "reviews": max_reviews
        },
        "incomplete_data_locations": incomplete_data
    }
    
    return results

# Execute the function and print results
if __name__ == "__main__":
    results = process_map_data()
    
    print("\n===== MAP DATA ANALYSIS RESULTS =====")
    print("\nValid Points Per Type:")
    for type_name, count in results["valid_points_per_type"].items():
        print(f"  {type_name}: {count}")
    
    print("\nAverage Rating Per Type:")
    for type_name, avg in results["average_rating_per_type"].items():
        print(f"  {type_name}: {avg}")
    
    print("\nLocation With Highest Reviews:")
    highest = results["highest_reviews_location"]
    print(f"  ID: {highest['id']}, Reviews: {highest['reviews']}")
    
    print("\nLocations With Incomplete Data:")
    if results["incomplete_data_locations"]:
        for loc_id in results["incomplete_data_locations"]:
            print(f"  {loc_id}")
    else:
        print("  None")