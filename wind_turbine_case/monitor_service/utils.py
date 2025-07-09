def log_assert(logger, condition, message):
    if not condition:
        logger.error(message)
        raise AssertionError(message)