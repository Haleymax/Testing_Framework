import pytest

from core.logger import logger
from testcases.test_webghost.conftest import webgl_host_data


class TestWebGLHosttest:

    @pytest.mark.parametrize("device_serial,packname,desc, case_type, case, instant_game, game_name", webgl_host_data)
    def test_webgl_host_huawei(self, device_serial, packname, desc, case_type, case, instant_game, game_name):
        logger.info(device_serial + ", " + packname + ", " + desc + ", " + case_type + ", " + case + ", " + instant_game + ", " + game_name)

if __name__ == '__main__':
    pytest.main(["-s", __file__])




# 终端启动命令： pytest .\testcases\test_webghost\test_02_print_case.py --serial=abcdefghijk --jobId=sdfas --casenum=20 --download=Flase