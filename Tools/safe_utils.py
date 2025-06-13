import functools
import logging
import time
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)

class RetryableError(Exception):
    """Exception to signal that an operation should be retried."""
    pass

def safe_for(*exc_types, default=None, handler=None, max_retries=0, retry_delay=0):
    """
    Decorator factory: catch only exc_types, return `default` (or call
    `handler`) instead of blowing up. Supports retrying on RetryableError.

    - exc_types: one or more Exception subclasses to catch.
    - default:    value to return when caught.
    - handler:    optional fn(exc, fn_name, args, kwargs) for side-effects.
    - max_retries: number of times to retry if handler raises RetryableError.
    - retry_delay: seconds to wait between retries.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except exc_types as e:
                    logging.warning(f"Caught {e!r} in {fn.__name__!r}, returning default={default!r}")
                    if handler:
                        try:
                            handler(e, fn.__name__, args, kwargs)
                        except RetryableError:
                            if attempts < max_retries:
                                attempts += 1
                                logging.info(f"Retrying {fn.__name__} (attempt {attempts}) after RetryableError...")
                                if retry_delay:
                                    time.sleep(retry_delay)
                                continue
                            else:
                                logging.error(f"Max retries reached for {fn.__name__}")
                        except Exception as h:
                            logging.error(f"Error in handler: {h!r}")
                    return default
        return wrapped
    return decorator

@contextmanager
def tolerate(*exc_types, default=None, handler=None, max_retries=0, retry_delay=0):
    """
    Context-manager: wrap a block, catch exc_types, recover to `default`
    or call `handler`. Supports retrying on RetryableError.
    """
    attempts = 0
    while True:
        try:
            yield
            break
        except exc_types as e:
            logging.warning(f"Caught {e!r} in tolerate(), recovering with default={default!r}")
            if handler:
                try:
                    handler(e)
                except RetryableError:
                    if attempts < max_retries:
                        attempts += 1
                        logging.info(f"Retrying tolerate block (attempt {attempts}) after RetryableError...")
                        if retry_delay:
                            time.sleep(retry_delay)
                        continue
                    else:
                        logging.error("Max retries reached in tolerate block")
                except Exception as h:
                    logging.error(f"Error in handler: {h!r}")
            break 