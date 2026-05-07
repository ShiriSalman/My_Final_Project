# import libraries

from pathlib import Path
import json

# --------------- read ESG data from esg_data.json --------------------

FILE_NAME = "esg_data.json"

path = Path.cwd() / FILE_NAME

try:
    with path.open(mode="r", ) as file:
        data = json.load(file)  # Convert JSON data to a Python object
        print("*** Data loaded successfully ***")
        print("Number of companies:", len(data))
except FileNotFoundError:
    print(f"{path} does not exist.")
except Exception as e:
    print(f"Unexpected error: {e}")

print(data)    

# ------------------------------------------------------------------------------------------------