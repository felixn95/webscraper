import colorlog
import logging

def setup_logging():
    """Configures the logger for use throughout the project with colored output."""
    logger = colorlog.getLogger()
    if not logger.handlers:  # Check if any handlers are already configured
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }))

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Optionally, stop propagation if not required

    return logger
