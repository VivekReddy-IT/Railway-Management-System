import logging
import sys

def setup_logger(name):
    """Set up and return a logger instance"""
    logger = logging.getLogger(name)
    
    # Set the logging level
    logger.setLevel(logging.DEBUG)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger 