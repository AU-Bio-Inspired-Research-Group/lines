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

        # Calculate slope and intercept of the line connecting start and end points
        start_point = np.array([x[0], y[0]])
        end_point = np.array([x[-1], y[-1]])
        
        if start_point[0] == end_point[0]:
            slope = np.inf  # Vertical line
        else:
            slope = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
        
        intercept = start_point[1] - slope * start_point[0]

        # Calculate perpendicular distances from each point to the line
        distances = []
        for i in range(1, len(x) - 1):
            point = np.array([x[i], y[i]])
            if np.isinf(slope):
                # Vertical line case
                distance = np.abs(point[0] - start_point[0])
            else:
                # Perpendicular distance formula
                distance = np.abs(slope * point[0] - point[1] + intercept) / np.sqrt(slope ** 2 + 1)
            distances.append(distance)

        # Calculate straightness rating
        mean_distance = np.mean(distances) if distances else 0.0
        straightness_rating = 1.0 - mean_distance / np.linalg.norm(end_point - start_point)

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
        total_length = 0.0

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

            # Calculate the length of the segment
            segment_length = np.linalg.norm(v1)

            total_angular_change += angle
            total_length += segment_length

        # Calculate oscillation rating
        if total_length == 0:
            oscillation_rating = 0  # To avoid division by zero
        else:
            oscillation_rating = total_angular_change / (2 * np.pi * total_length)  # Normalize by 2*pi*total_length for a range of [0, 1]

        oscillation_ratings.append({
            'file_name': entry['file_name'],
            'rating': oscillation_rating
        })

    return oscillation_ratings