import logging

def Logger():    
    logger = logging.getLogger('mini-spider.py')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('logs/mini_spider.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    