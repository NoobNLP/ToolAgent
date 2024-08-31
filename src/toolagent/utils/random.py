import random
import string
import hashlib

def generate_random_key(length=8):
    """
    Generate a random string of specified length.

    Args:
        length (int): The length of the random string. Default is 10.

    Returns:
        str: The generated random string.
    """
    # Define all possible characters for the string
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select the specified number of characters and generate the string
    random_key = "".join(random.choice(characters) for i in range(length))
    return random_key

def calculate_tool_hash(tool_name, tool_description, tool_set, input_parameters, output_parameters):
    """
    Calculate the hash value of a tool.

    Args:
        tool_name (str): The name of the tool.
        tool_description (str): The description of the tool.
        tool_set (str): The name of the tool set.
        input_parameters (list): The list of input parameters for the tool.
        output_parameters (list): The list of output parameters for the tool.

    Returns:
        str: The hash value of the tool.
    """
    data = f"{tool_set}{tool_name}{tool_description}{str(input_parameters)}{str(output_parameters)}"
    
    hash_object = hashlib.sha256()
    hash_object.update(data.encode('utf-8'))
    
    return hash_object.hexdigest()

