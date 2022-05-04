import logging


def info(message: str) -> None:
    logger = logging.getLogger()
    logger.info(message)
