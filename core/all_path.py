import os.path

base_path = os.path.dirname(os.path.dirname(__file__))

appPath = os.path.join(base_path , "app")
dataPath = os.path.join(base_path , "data" , "webgl_host")
reportPath = os.path.join(base_path , "report")
config_file_path = os.path.join(base_path , "config" , "webgl_host.ini")