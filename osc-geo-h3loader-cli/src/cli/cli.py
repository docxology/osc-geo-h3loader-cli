import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_cli():
    try:
        logger.info('CLI operation successful')
    except Exception as e:
        logger.error(f'CLI Error: {str(e)}')
        raise

if __name__ == '__main__':
    run_cli() 