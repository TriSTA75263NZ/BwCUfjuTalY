# 代码生成时间: 2025-09-22 15:25:36
import os
import shutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# FolderOrganizer class to handle the file and folder operations
class FolderOrganizer:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif'],
            'documents': ['.pdf', '.doc', '.docx', '.txt'],
            'videos': ['.mp4', '.avi', '.mov'],
            'audios': ['.mp3', '.wav'],
        }

    def organize(self):
        # Create destination folders if they don't exist
        for folder_name in self.extensions.keys():
            folder_path = os.path.join(self.destination_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)

        # Move files to their respective folders
        for file_name in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, file_name)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(file_name)[1].lower()
                for folder_name, extensions in self.extensions.items():
                    if file_extension in extensions:
                        target_path = os.path.join(
                            self.destination_folder, folder_name, file_name)
                        shutil.move(file_path, target_path)
                        break

# Pyramid view to trigger the FolderOrganizer
@view_config(route_name='organize', renderer='json')
def organize_view(request):
    try:
        source_folder = request.params.get('source')
        destination_folder = request.params.get('destination')

        if not source_folder or not destination_folder:
            return Response(
                json_body={'error': 'Source and destination folders must be provided.'},
                status=400
            )

        organizer = FolderOrganizer(source_folder, destination_folder)
        organizer.organize()
        return Response(
            json_body={'message': 'Files organized successfully.'},
            status=200
        )
    except Exception as e:
        return Response(
            json_body={'error': str(e)},
            status=500
        )

# Pyramid app configuration
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('organize', '/organize')
    config.scan()
    return config.make_wsgi_app()
