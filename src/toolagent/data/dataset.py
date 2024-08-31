from toolagent.utils.io import read_JSON
class Dataset:
    """the general dataset

    get the dataset we need

    Attributes:
        data (list):the final data

    """
    def __init__(self, data: list):
        self.data = data


    @classmethod
    def load_from_path(cls, path: str):
        """ load data from file path

        pass the path

        Args:
            path (str): your data path


        """
        data = read_JSON(path)
        dataset = Dataset(data)
        return dataset

def load_dataset(path: str)->Dataset:
    """ load data from path

    load data from path and return final dataset

    Args:
        path (str): your data path

    Returns:
        Dataset: final dataset class

    """
    return Dataset.load_from_path(path)