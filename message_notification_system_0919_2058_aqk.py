# 代码生成时间: 2025-09-19 20:58:30
{
    """
    A simple message notification system using PYRAMID framework.
    """

    import json
    from pyramid.config import Configurator
    from pyramid.response import Response
    from pyramid.view import view_config
    from pyramid.httpexceptions import HTTPInternalServerError
    
    # Define a simple in-memory storage for messages
    messages_storage = []
    
    def add_message(message):
        """
        Add a new message to the storage.
        :param message: The message to be added.
        :return: None
        """
        try:
            messages_storage.append(message)
        except Exception as e:
            raise HTTPInternalServerError('Error adding message: {}'.format(e))
    
    def get_messages():
        """
        Retrieve all messages from the storage.
        :return: A list of messages.
        """
        try:
            return messages_storage
        except Exception as e:
            raise HTTPInternalServerError('Error retrieving messages: {}'.format(e))
    
    @view_config(route_name='add_message', request_method='POST')
    def add_message_view(request):
        """
        View function to handle adding a new message.
        :return: A JSON response with the result of the operation.
        """
        try:
            message_data = request.json_body
            add_message(message_data['message'])
            return Response(json.dumps({'status': 'success', 'message': 'Message added successfully'}),
                            content_type='application/json')
        except KeyError:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid message data'}),
                            content_type='application/json', status=400)
        except Exception as e:
            raise HTTPInternalServerError('Error in adding message view: {}'.format(e))
    
    @view_config(route_name='get_messages', request_method='GET')
    def get_messages_view(request):
        """
        View function to handle retrieving all messages.
        :return: A JSON response with the messages.
        """
        try:
            messages = get_messages()
            return Response(json.dumps({'status': 'success', 'messages': messages}),
                            content_type='application/json')
        except Exception as e:
            raise HTTPInternalServerError('Error in getting messages view: {}'.format(e))
    
    def main(global_config, **settings):
        """
        Main function to configure the Pyramid application.
        :param global_config: The global configuration data.
        :param settings: Additional settings for the application.
        :return: A Pyramid application object.
        """
        with Configurator(settings=settings) as config:
            config.add_route('add_message', '/add_message')
            config.add_route('get_messages', '/get_messages')
            config.scan()
        
        return config.make_wsgi_app()
    
    if __name__ == '__main__':
        from wsgiref.simple_server import make_server
        app = main({})
        server = make_server('0.0.0.0', 6543, app)
        print('Serving on http://0.0.0.0:6543')
        server.serve_forever()
}
