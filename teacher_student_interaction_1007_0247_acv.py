# 代码生成时间: 2025-10-07 02:47:26
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pyramid.session import签字和密封

# 定义数据库模型
Base = declarative_base()

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

# 配置数据库和会话
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    config.include('pyramid_chameleon.zpt')
    config.add_route('index', '/')
    config.add_route('create_interaction', '/create_interaction')
    config.add_route('view_interactions', '/view_interactions')
    config.scan()
    return config.make_wsgi_app()

# 创建数据库连接
engine = create_engine('sqlite:///interactions.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 定义视图
@view_config(route_name='index', renderer='templates/index.pt')
def index_view(request):
    """
    Return a view for the index page.
    """
    return {}

@view_config(route_name='create_interaction', renderer='json')
def create_interaction_view(request):
    """
    Create a new interaction and return a response.
    """
    try:
        teacher_id = request.json['teacher_id']
        student_id = request.json['student_id']
        message = request.json['message']
        interaction = Interaction(teacher_id=teacher_id, student_id=student_id, message=message, timestamp=datetime.datetime.now())
        session.add(interaction)
        session.commit()
        return {'status': 'success', 'message': 'Interaction created successfully.'}
    except SQLAlchemyError as e:
        session.rollback()
        return {'status': 'error', 'message': 'Failed to create interaction.', 'error': str(e)}

@view_config(route_name='view_interactions', renderer='json')
def view_interactions_view(request):
    """
    Retrieve and return all interactions.
    """
    try:
        interactions = session.query(Interaction).all()
        return [{'id': interaction.id, 'teacher_id': interaction.teacher_id, 'student_id': interaction.student_id, 'message': interaction.message, 'timestamp': interaction.timestamp.isoformat()} for interaction in interactions]
    except SQLAlchemyError as e:
        return {'status': 'error', 'message': 'Failed to retrieve interactions.', 'error': str(e)}
