import argparse

from crawler import Crawler
from crawler.config_parser import JSONParser
from crawler.default_functions import (SELECT_FUNCTIONS, FILTER_FUNCTIONS,
                                       ACTION_FUNCTIONS)
from crawler.pages_downloader import FuturesDownloader
from crawler.storage_handler import JSONHandler

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config", required=True)
    parser.add_argument("-s", "--storage", dest="storage", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_arguments()
    crawler = Crawler(JSONParser.create_parser(args.config, SELECT_FUNCTIONS,
                                               FILTER_FUNCTIONS,
                                               ACTION_FUNCTIONS),
                      FuturesDownloader(),
                      JSONHandler.load_storage(args.storage))
    crawler.fetch_pages()
    crawler.process_pages()
    JSONHandler.save_storage(args.storage, crawler.new_pages_storage())

