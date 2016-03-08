#!/usr/bin/python
import argparse
import log
import config_load
import seedfile_load
import crawl_thread


version = '1.0'
log.set_logger(filename='logs/mini_spider.log', level='DEBUG:INFO')
parser = argparse.ArgumentParser(description='a mini spider')
parser.add_argument("-c", "--conf", help="config file", required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)
args = parser.parse_args()

# an hash(called dict in python) in config file spider block
spider_config = config_load.loadconfig(args.conf, 'spider')

# Global Configs
g_url_list_file = spider_config.get('url_list_file')
g_output_directory = spider_config.get('output_directory')
g_max_depth = int(spider_config.get('max_depth'))
g_crawl_interval = int(spider_config.get('crawl_interval'))
g_crawl_timeout = int(spider_config.get('crawl_timeout'))
g_target_url = spider_config.get('target_url')
g_thread_count = int(spider_config.get('thread_count'))

log.info('init complete, start running the spider with configs: ' + str(spider_config))
seedfile_load.loadSeedFile(g_url_list_file)
crawl_thread.crawl(g_thread_count, g_output_directory, g_max_depth, g_target_url, g_crawl_interval, g_crawl_timeout)
