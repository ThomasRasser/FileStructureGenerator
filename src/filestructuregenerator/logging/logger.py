import logging

# ==================================================================================

def setup_logger(name: str, log_file: str, level=logging.DEBUG):
    """Function to set up a logger."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger