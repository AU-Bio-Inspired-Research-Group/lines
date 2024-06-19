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
            'rating': straightness_rating
        })

    return straightness_ratings


def calculate_oscillation_rating(json_file):
    json_file = "./rosbags/figures/" + json_file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    oscillation_ratings = []

    for entry in data:
        x = np.array(entry['x'])
        y = np.array(entry['y'])

        # Calculate total angular change
        total_angular_change = 0.0
        for i in range(len(x) - 2):
            v1 = np.array([x[i+1] - x[i], y[i+1] - y[i]])
            v2 = np.array([x[i+2] - x[i+1], y[i+2] - y[i+1]])

            # Calculate angle between vectors v1 and v2
            dot_product = np.dot(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)
            if norms == 0:
                angle = 0  # Handle zero division case
            else:
                angle = np.arccos(np.clip(dot_product / norms, -1.0, 1.0))

            total_angular_change += angle

        # Calculate oscillation rating
        oscillation_rating = total_angular_change / (2 * np.pi)  # Normalize by 2*pi for a range of [0, 1]

        oscillation_ratings.append({
            'file_name': entry['file_name'],
            'rating': oscillation_rating
        })

    return oscillation_ratings