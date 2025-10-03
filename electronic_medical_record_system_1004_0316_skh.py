# 代码生成时间: 2025-10-04 03:16:29
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Authenticated, Everyone, DenyAll
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactoryConfig
from pyramid.threadlocal import get_current_registry
from pyramid.paster import setup_logging
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from pyramid_tm import transactional
import datetime
import os
import logging
import json

# 配置日志记录
setup_logging('config:logging.ini')

# 定义数据库模型
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    dob = Column(Date)
    gender = Column(String(10))

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship('Patient', backref='records')
    date = Column(Date)
    description = Column(Text)

# 定义视图函数
@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    patients = session.query(Patient).all()
    return {'patients': patients}

@view_config(route_name='add_patient', renderer='templates/add_patient.jinja2')
def add_patient_view(request):
    if request.method == 'POST':
        name = request.params.get('name')
        dob = request.params.get('dob')
        gender = request.params.get('gender')
        patient = Patient(name=name, dob=datetime.datetime.strptime(dob, '%Y-%m-%d').date(), gender=gender)
        session.add(patient)
        session.commit()
        return HTTPFound(location=request.route_url('home'))
    return {}

@view_config(route_name='view_patient', renderer='templates/view_patient.jinja2')
def view_patient_view(request):
    patient_id = request.matchdict['id']
    patient = session.query(Patient).get(patient_id)
    if patient:
        records = patient.records
        return {'patient': patient, 'records': records}
    else:
        return HTTPFound(location=request.route_url('home'))

@view_config(route_name='add_record', renderer='templates/add_record.jinja2')
def add_record_view(request):
    if request.method == 'POST':
        patient_id = request.params.get('patient_id')
        date = request.params.get('date')
        description = request.params.get('description')
        record = MedicalRecord(patient_id=patient_id, date=datetime.datetime.strptime(date, '%Y-%m-%d').date(), description=description)
        session.add(record)
        session.commit()
        return HTTPFound(location=request.route_path('view_patient', id=patient_id))
    return {}

# 设置 Pyramid 配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 设置数据库连接
    engine = create_engine('sqlite:///emr.db')
    Base.metadata.bind = engine
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    config.registry['session'] = session
    
    # 设置视图配置
    config.add_route('home', '/')
    config.add_route('add_patient', '/add_patient')
    config.add_route('view_patient', '/patients/{id}')
    config.add_route('add_record', '/patients/{id}/add_record')
    
    # 设置视图函数
    config.scan()
    
    # 设置数据库迁移
    Base.metadata.create_all(engine)
    
    # 设置安全策略
    authn_policy = AuthTktAuthenticationPolicy('secret')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    # 设置会话工厂
    session_factory = SignedCookieSessionFactoryConfig('secret')
    config.set_session_factory(session_factory)
    
    return config.make_wsgi_app()
