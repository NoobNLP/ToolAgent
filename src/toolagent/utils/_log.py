import logging

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("otl")
    logger.setLevel(logging.DEBUG)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter("[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s")

    console = logging.StreamHandler(stream=None)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    
    logger.addHandler(console)
    return logger