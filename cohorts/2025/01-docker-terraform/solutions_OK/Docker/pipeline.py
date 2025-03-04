import logging
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger(__name__)

logger.info("job started")

arg0 = sys.argv[0]
logger.info(f"running: {arg0}")

if len(sys.argv)>1:
    arg1 = sys.argv[1]
    logger.info(f"first argument: {arg1}")

logger.info("job finished successfully")