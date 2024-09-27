import pytest

from core.logger import logger
from testcases.test_webghost.conftest import webgl_host_data


class TestWebGLHost:

    @pytest.mark.parametrize("devicesid, packagename, type, gamename, gamelink",webgl_host_data['test_webgl_host'])
    def test_webgl_host(self, devicesid, packagename, type, gamename, gamelink):
        logger.info("***********  开始用例  *****************")
        logger.info(f"devicesid : {devicesid}, packagename : {packagename}, type : {type}, gamename : {gamename}, gamelink{gamelink}")
        assert 1 == 1

