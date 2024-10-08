import pytest

from core.games_info import create_gamelist_by_casenum
from core.parameter import  parameter
from core.read_data import read_data
from core.all_path import config_file_path





webgl_host_data = create_gamelist_by_casenum(parameter.get_serial(), parameter.get_casenum())