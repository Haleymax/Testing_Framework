import sys
import getopt
from core.logger import logger, Logger


class Parameter:

    def get_serial(self):
        serial = ''
        try:
            opts, args = getopt.getopt(sys.argv, '', ['jobId=', 'serial=', 'download=', 'casenum='])
        except getopt.GetoptError:
            logger.warning('Error parsing command line arguments.')
            return None
        for arg in args :
            if '--serial' in arg:
                serial = arg.split('=')[1]
                break
        return str(serial)

    def get_casenum(self):
        casenum = ''
        try:
            opts, args = getopt.getopt(sys.argv, '', ['jobId=', 'serial=', 'download=', 'casenum='])
            logger.info(args)
        except getopt.GetoptError:
            logger.warning('Error parsing command line arguments.')
            return None
        for arg in args:
            if '--casenum' in arg:
                casenum = arg.split('=')[1]
                break
        return casenum if casenum else 'all'

parameter = Parameter()