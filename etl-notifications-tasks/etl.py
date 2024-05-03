import logging

logger = logging.getLogger('etl-tasks-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.info('Ia yest cron')
