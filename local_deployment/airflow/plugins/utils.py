import json, csv
from pathlib import Path
import os

def get_key(current_date):
    KEY = (
        current_date.strftime("%Y-%m-%d")
    )
    return KEY

def json_to_csv_write(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)['data']
    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)
        # Write the headers (keys of the first dictionary in the list)
        csv_writer.writerow(data[0].keys())
        # Write the data rows
        for row in data:
            csv_writer.writerow(row.values())

def change_file_path(target_dir, file_name):
    """
    Changes a file's path from one directory to another and changes its extension.

    :param source_dir: The source directory path.
    :param target_dir: The target directory path.
    :param file_name: The name of the file to be moved.
    :return: The new file path with changed directory and extension.
    """
    # Extract the base name of the file without extension
    base_name = Path(file_name).stem
    # Create the new file name with the new extension
    new_file_name = f"{base_name}.csv"
    # Construct the new file path
    new_file_path = os.path.join(target_dir, new_file_name)
    return new_file_path

def json_to_csv(path_json, path_csv, json_file_name):
    # set file name and save the data
    f1 = os.path.join(path_json, json_file_name)
    f2 = change_file_path(path_csv, f1)
    json_to_csv_write(f1, f2)