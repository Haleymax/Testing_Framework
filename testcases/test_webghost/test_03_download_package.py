from core.all_path import appPath
from core.file_download import Getlab_request, clear_file, is_exist, unzip_file


class TestWebGLhost:
    def test_install_app(self, get_job_id, get_property):
        request = Getlab_request(get_property["gitlab_token"])
        # request.set_url_by_jobid(get_job_id)
        # request.download_by_pipeline_id(7817)
        is_exist(appPath)

        clear_file(appPath)

        request.download_by_pipeline_id(7817)

        unzip_file(appPath)