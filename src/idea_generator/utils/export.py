import json

from pydantic import BaseModel


def export_to_json(data: BaseModel, filename: str) -> None:
    """Export the data to a JSON file.
    
    Args:
        data (BaseModel): The data to be exported.
        filename (str): The name of the file to export the data to.

    """
    with open(filename, 'w') as f:
        json.dump(data.model_dump_json(), f, indent=4)
