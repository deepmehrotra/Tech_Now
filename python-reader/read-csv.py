import pandas as pd
import requests
import json
import time

def read_excel_and_print(file_path):
    """Reads an Excel file and prints its contents.

    Args:
        file_path (str): The path to the Excel file.
    """

    df = pd.read_excel(file_path)
    print(df)


def make_http_request(url, data, headers=None):
    """
    Makes an HTTP POST request to the specified URL with the given JSON data.

    Args:
        url (str): The URL of the API endpoint.
        data (dict): The JSON data to be sent in the request body.
        headers (dict, optional): Additional headers to be included in the request. Defaults to None.

    Returns:
        dict: The JSON response from the server, or None if an error occurs.
    """

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for error HTTP statuses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
        return None
    
def get_posts(url, headers=None):
    """
    Makes an HTTP GET request to the specified URL to get the JSON data.

    Args:
        url (str): The URL of the API endpoint.
        headers (dict, optional): Additional headers to be included in the request. Defaults to None.

    Returns:
        dict: The JSON response from the server, or None if an error occurs.
    """

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for error HTTP statuses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
        return None

def modify_json_data(data, key_to_replace, new_value):
    """
    Modifies a JSON object by replacing the value of a specified key.

    Args:
        data (dict): The JSON data to be modified.
        key_to_replace (str): The key to be replaced.
        new_value (any): The new value to be assigned to the key.

    Returns:
        dict: The modified JSON object.
    """

    data[key_to_replace] = new_value
    return data


if __name__ == "__main__":
    now = int(time.time())
    print(f"Current timestamp: {now}")
    file_path = "test.xlsx"  # Replace with your file path
    read_excel_and_print(file_path)

    url = "http://localhost:3000/posts"  # Replace with your actual API endpoint

    # Read JSON data from a file
    with open("data1.json", "r") as f:
        data = json.load(f)

    # Modify a key in the JSON data
    modified_data = modify_json_data(data, "id", now)

    # Make the HTTP POST request
    response = make_http_request(url, modified_data)

    # Make the HTTP POST request
    res = get_posts(url)

    if response:
        print(response)

    if res:
        print("GET")
        print(res)