import functools
import sys


def clamp(minimum, v, maximum):
    """Clamp a value within the range"""
    return max(minimum, min(v, maximum))


if sys.version_info.major < 3:
    raise RuntimeError

# Python<3.9 doesn't have `cache`. Shim with `lru_cache`
cache = functools.cache if sys.version_info.minor >= 9 else functools.lru_cache
