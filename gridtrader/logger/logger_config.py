import logging
import sys
from datetime import datetime
td = datetime.today().date()

logging.basicConfig(filename=f'mylog_{td}.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
