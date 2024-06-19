import json
import os
import tarfile as tf
import matplotlib.pyplot as plt
import pandas as pd
import bagpy as bp

# Drop columns
drop = ["Time", "header.stamp.secs", "header.stamp.nsecs", "pose.orientation.x", 
        "pose.orientation.y", "pose.orientation.w", "pose.orientation.z", "header.frame_id"]

# Define the directories
rosbags_directory = "./rosbags/straight/"
figures_directory = "./rosbags/figures/"

finish_colormap = {3: "red", 1: "gray", 2: "red", 0: "green"}

def is_zip_file(x: str): 
    return x.endswith(".bag.tar.gz")

# Define a list to store extracted data
extracted_data = []

# Iterate through valid entries in the directory
valid_entries = (entry for entry in os.scandir(rosbags_directory) if is_zip_file(entry.path))
for entry in valid_entries:
    tarfile = tf.open(entry.path, mode="r:gz")
    decompressed_path = None
    for tarinfo in tarfile:
        decompressed_path = os.path.join(rosbags_directory, tarinfo.path)
    tarfile.extractall(path=rosbags_directory)
    tarfile.close()

    bagfile = bp.bagreader(decompressed_path)
    if decompressed_path.endswith(".bag"):
        position = bagfile.message_by_topic("/turtlebot3/filtered/position")
        finish = bagfile.message_by_topic("/check_finished")

        finish_df = pd.read_csv(finish)
        position_df = pd.read_csv(position)
        position_df = position_df.drop(drop, axis=1)

        x = position_df["pose.position.x"].values.tolist()
        y = position_df["pose.position.y"].values.tolist()
        finish_condition = int(finish_df.iloc[-1, 1])

        data_entry = {
            "file_name": entry.name,
            "x": x,
            "y": y,
            "finish_condition": finish_condition
        }

        extracted_data.append(data_entry)

        if finish_condition == 0:
            plt.plot(x, y, c="green")
        else:
            plt.plot(x, y, alpha=0.5)

        plt.scatter(x[0], y[0], marker="o", c=finish_colormap[finish_condition])
        plt.scatter(x[-1], y[-1], marker="x", c=finish_colormap[finish_condition])

        plt.scatter(6, 6, c="black", s=50)
        plt.plot([7, 7], [5, 3], c="black", lw=2)
        plt.plot([7, 7], [-3, -5], c="black", lw=2)

# Save extracted_data to a JSON file
experiment_name = os.path.basename(os.path.normpath(rosbags_directory))
json_file_name = os.path.join(figures_directory, experiment_name + "_data.json")
with open(json_file_name, 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

# Save the figure
file_name = os.path.join(figures_directory, experiment_name + ".png")
plt.title(experiment_name)
plt.savefig(file_name, dpi=600)
plt.show()
