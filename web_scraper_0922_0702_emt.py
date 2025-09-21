# 代码生成时间: 2025-09-22 07:02:49
# web_scraper.py
"""
A Pyramid web application that serves as a web content scraper tool.
This application uses the requests library to fetch web content and Beautiful Soup to parse HTML.
"""

import os
import requests
from bs4 import BeautifulSoup
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# Define the root directory for the application
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the route for the 'scrap' view
def scrap(request):
    """
    Scrape the content of a web page specified by the 'url' parameter in the request.
    Returns the HTML content of the page.
    """
    url = request.params.get(u'url')
    if not url:
        return Response("Please provide a URL to scrape", status=400)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return Response(response.text, content_type='text/html')
    except requests.exceptions.RequestException as e:
        return Response(f"An error occurred: {e}", status=500)

# Pyramid configuration
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('scrap', '/scrap')
        config.add_view(scrap, route_name='scrap', renderer='json')
        config.scan()

if __name__ == '__main__':
    main({})