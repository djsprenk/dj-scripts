"""Utility functions used across multiple files"""

import json
import xmltodict
import zipfile


def read_json_file(file_path):
    """Load the file and return the parsed data"""
    with open(file_path) as json_file:
        data = json.load(json_file)
        json_file.close()

    return data


def write_json_file(data, output_json_path):
    """Serialize the data dict to JSON and write to the output_json_path location"""
    json_data = json.dumps(data)

    with open(output_json_path, "w") as json_file:
        json_file.write(json_data)
        json_file.close()


def read_from_xml(xml_path):
    """Read data from XML file"""
    data_dict = {}

    # open the input xml file and read data in form of python dictionary using xmltodict module
    with open(xml_path) as xml_file:

        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()

    return data_dict


def xml_to_json(xml_path, json_path):
    """
    Load XML and write to JSON
    """

    data_dict = read_from_xml(xml_path)

    # generate the object using json.dumps() corresponding to json data
    json_data = json.dumps(data_dict)

    with open(json_path, "w") as json_file:
        json_file.write(json_data)
        json_file.close()


def unzip_file(zip_path, extract_to):
    # Unzip the file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def get_latest_file_with_extension(dir_path, extension):
    """Get most recent file from directory."""
    files = list(dir_path.glob(f"*.{extension}"))

    if not files:
        raise FileNotFoundError(f"No {extension} files found in the directory.")

    # Find the most recent zip file
    most_recent_file = max(files, key=lambda p: p.stat().st_mtime)
    return most_recent_file
