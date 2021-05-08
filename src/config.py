import os

# src路径
src_path = os.path.dirname(__file__)

# 根路径
root_path = os.path.dirname(src_path)

# api路径
api_path = os.path.join(src_path, 'api')

# 插件路径
plugins_path = os.path.join(root_path, 'plugins')

# 前端静态根目录
static_path = os.path.join(root_path, 'public')
