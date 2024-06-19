# Lines

This code provides functionality to process ROS bag files, extract robot positional data and finish conditions, plot trajectories, save individual and summary figures, and store extracted data in JSON format for analysis.

## Commands Supported:

### `lines`

Processes a directory containing ROS bag files.

- **Usage**: `python lines.py lines <directory>`
- **Functionality**:
  - Utilizes `linesMethod` from `processLines.py` to extract data and plot trajectories.
  - Generates individual trajectory plots and a summary figure for the entire experiment.
  - Saves extracted data as JSON files in a specified directory.

### `straight`

Processes a JSON file to calculate straightness ratings for trajectory data.

- **Usage**: `python lines.py straight <json_file>`
- **Functionality**:
  - Uses `calculate_straightness_rating` function to evaluate trajectory straightness.
  - Outputs ratings for each trajectory file processed.

### `oscillate`

Processes a JSON file to calculate oscillation ratings for trajectory data.

- **Usage**: `python lines.py oscillate <json_file>`
- **Functionality**:
  - Uses `calculate_oscillation_rating` function to assess trajectory oscillation.
