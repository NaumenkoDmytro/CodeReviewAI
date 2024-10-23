import logging
import sys

# Configure the logger
def configure_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set its level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)

    # Define the logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add the formatter to both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
