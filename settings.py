DEBUG = True

try:
    # 便于设置本地开发环境
    from local_settings import *
except ImportError:
    pass
