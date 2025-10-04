# 代码生成时间: 2025-10-05 03:10:31
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Authenticated
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, MetaData, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from pyramid.authentication import remember, forget
from datetime import datetime
from pyramid.exceptions import Forbidden
import json

# 设置数据库连接
DATABASE_URL = 'sqlite:///medical_records.db'
engine = create_engine(DATABASE_URL)
metadata = MetaData()
db_session = scoped_session(sessionmaker(bind=engine))

# 定义电子病历表
patient_table = Table('patients', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('birth_date', Date),
    Column('medical_record', Text)
)

metadata.create_all(engine)

# 实现电子病历系统的基本功能
class EMRSystem:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='add_patient', renderer='json')
    def add_patient(self):
        """添加新病人"""
        data = json.loads(self.request.body)
        try:
            patient = Patient(name=data['name'], birth_date=data['birth_date'])
            db_session.add(patient)
            db_session.commit()
            return {'status': 'success', 'message': 'Patient added successfully'}
        except Exception as e:
            db_session.rollback()
            return {'status': 'error', 'message': str(e)}

    @view_config(route_name='update_patient', renderer='json')
    def update_patient(self):
        """更新病人信息"""
        data = json.loads(self.request.body)
        try:
            patient = db_session.query(Patient).filter_by(id=data['id']).first()
            if patient:
                patient.name = data['name']
                patient.birth_date = data['birth_date']
                db_session.commit()
                return {'status': 'success', 'message': 'Patient updated successfully'}
            else:
                return {'status': 'error', 'message': 'Patient not found'}
        except Exception as e:
            db_session.rollback()
            return {'status': 'error', 'message': str(e)}

    @view_config(route_name='delete_patient', renderer='json')
    def delete_patient(self):
        """删除病人"""
        data = json.loads(self.request.body)
        try:
            patient = db_session.query(Patient).filter_by(id=data['id']).first()
            if patient:
                db_session.delete(patient)
                db_session.commit()
                return {'status': 'success', 'message': 'Patient deleted successfully'}
            else:
                return {'status': 'error', 'message': 'Patient not found'}
        except Exception as e:
            db_session.rollback()
            return {'status': 'error', 'message': str(e)}

    @view_config(route_name='get_patient', renderer='json')
    def get_patient(self):
        """获取病人信息"""
        data = json.loads(self.request.body)
        try:
            patient = db_session.query(Patient).filter_by(id=data['id']).first()
            if patient:
                return {'status': 'success', 'data': {'name': patient.name, 'birth_date': patient.birth_date}}
            else:
                return {'status': 'error', 'message': 'Patient not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# 实现病人模型
class Patient:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        self.medical_record = ''

# 设置 Pyramid 配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('add_patient', '/add_patient')
    config.add_route('update_patient', '/update_patient')
    config.add_route('delete_patient', '/delete_patient')
    config.add_route('get_patient', '/get_patient')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})