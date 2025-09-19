# 代码生成时间: 2025-09-19 17:03:56
# unzip_tool.py

"""
Unzip Tool application using Pyramid framework.
Handles file uploads and provides unzip functionality.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import remember, forget
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactoryConfig
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.exceptions import PredicateMismatch
from pyramid.interfaces import IBeforeRender
from pyramid.traversal import find_root
from zipfile import ZipFile
from io import BytesIO
import os

# Define a root factory function
def root_factory(request):
    return {}

# Configure the Pyramid application
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('unzip', '/unzip')
    config.add_static_view(name='static', path='unzip_tool:static')
    config.add_static_view(name='favicon', path='unzip_tool:static/favicon.ico', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()

# Create a view to handle the unzip process
@view_config(route_name='unzip', renderer='templates/unzip.pt')
def unzip_view(request):
    # Check if the request method is POST
    if request.method != 'POST':
        raise HTTPBadRequest('Only POST method is allowed.')

    # Retrieve the uploaded file from the request
    file = request.POST['file'].file
    # Create a buffer to hold the file contents
    buffer = BytesIO(file.read())
    # Open the zip file from the buffer
    with ZipFile(buffer, 'r') as zip_file:
        try:
            # Extract all files from the zip archive
            zip_file.extractall('unzipped_files')
            # Return a success message
            return {'message': 'Files successfully extracted.'}
        except Exception as e:
            # Handle any exceptions that occur during extraction
            return {'error': str(e)}

# Define a subscriber to handle before rendering events
@subscriber(IBeforeRender)
def add_unzip_script(event):
    # Add a script tag to the response to include the unzip script
    event.response.content_type = 'text/html'
    event.response.headers['X-Frame-Options'] = 'ALLOW-FROM https://example.com'
    return render_to_response('templates/unzip.pt', event)

# Define a route for serving the upload form
@view_config(route_name='upload_form')
def upload_form_view(request):
    # Render the upload form template
    return render_to_response('templates/upload_form.pt')

# Define a route for serving the static files
@view_config(route_name='static', renderer='string')
def static_view(request):
    # Get the static file path
    static_path = request.matchdict['subpath']
    # Return the static file content
    return Response(static_path, content_type='text/plain')
