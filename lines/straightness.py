import json
import numpy as np

def calculate_straightness_rating(json_file):
    json_file = "./rosbags/figures/" + json_file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    straightness_ratings = []

    for entry in data:
        x = np.array(entry['x'])
        y = np.array(entry['y'])

        # Calculate Euclidean distance between start and end points
        start_point = np.array([x[0], y[0]])
        end_point = np.array([x[-1], y[-1]])
        distance = np.linalg.norm(end_point - start_point)

        # Calculate actual trajectory length
        total_distance = 0.0
        for i in range(len(x) - 1):
            total_distance += np.linalg.norm([x[i+1] - x[i], y[i+1] - y[i]])

        # Calculate straightness rating
        straightness_rating = distance / total_distance

        straightness_ratings.append({
            'file_name': entry['file_name'],
            'straightness_rating': straightness_rating
        })

    return straightness_ratings
