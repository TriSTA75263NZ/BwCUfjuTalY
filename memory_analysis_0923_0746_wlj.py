# 代码生成时间: 2025-09-23 07:46:24
from pyramid.config import Configurator
from pyramid.view import view_config
import psutil
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryAnalysisService:
    """
    内存使用情况分析服务类
    """
    def __init__(self):
        pass

    def get_memory_usage(self):
        """
        获取内存使用情况
        """
        try:
            # 获取系统内存信息
            mem = psutil.virtual_memory()
            # 计算内存使用率
            memory_usage = mem.percent
            logger.info(f"Memory Usage: {memory_usage}%")
            return memory_usage
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            raise


@view_config(route_name='memory_analysis', renderer='json')
def memory_analysis_view(request):
    """
    视图函数，返回内存使用情况
    """
    service = MemoryAnalysisService()
    try:
        memory_usage = service.get_memory_usage()
        return {"memory_usage": memory_usage}
    except Exception as e:
        return {"error": str(e)}


def main(global_config, **settings):
    """
    程序入口函数
    """
    config = Configurator(settings=settings)
    config.include("pyramid_jinja2")
    config.add_route('memory_analysis', '/memory_analysis')
    config.scan()
    return config.make_wsgi_app()
