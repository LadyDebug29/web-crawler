import os
import click
from web_crawler import WebCrawler


def try_make_directory(directory_name):
    try:
        os.mkdir(f'{directory_name}')
    except FileExistsError:
        pass

@click.command()
@click.option("--url", default='https://example.com')
@click.option("--depth", default=1)
def main(url, depth):
    try_make_directory('links')
    os.chdir('links')
    wc = WebCrawler(url, depth)
    wc.start_crawl()


if __name__ == "__main__":
    main()
