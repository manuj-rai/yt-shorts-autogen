import sys
from loguru import logger
from .config import settings

logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    backtrace=False,
    diagnose=False,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}",
)
