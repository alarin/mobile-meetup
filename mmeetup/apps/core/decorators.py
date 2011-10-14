def exception_to_log(logger):
    def inner(func):
        def actual_dec(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:

                logger.error('Exception.', exc_info=True)
        return actual_dec
    return inner