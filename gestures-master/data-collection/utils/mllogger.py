"""
  Generic logger for common library
  Created on August 30, 2016
"""
__author__ = "Richard Gass"
__copyright__ = """
Copyright (c) 201x Magic Leap, Inc. (COMPANY) All Rights Reserved.
Magic Leap, Inc. Confidential and Proprietary

NOTICE:  All information contained herein is, and remains the property
of COMPANY. The intellectual and technical concepts contained herein
are proprietary to COMPANY and may be covered by U.S. and Foreign
Patents, patents in process, and are protected by trade secret or
copyright law.  Dissemination of this information or reproduction of
this material is strictly forbidden unless prior written permission is
obtained from COMPANY.  Access to the source code contained herein is
hereby forbidden to anyone except current COMPANY employees, managers
or contractors who have executed Confidentiality and Non-disclosure
agreements explicitly covering such access.

The copyright notice above does not evidence any actual or intended
publication or disclosure of this source code, which includes
information that is confidential and/or proprietary, and is a trade
secret, of COMPANY.  ANY REPRODUCTION, MODIFICATION, DISTRIBUTION,
PUBLIC PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS
SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF COMPANY IS
STRICTLY PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND
INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF THIS SOURCE
CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS
TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
"""

import datetime
import logging
import sys
import traceback


class MLLogger(object):
    """Generic logger that uses the python logging system """
    def __init__(self, logfile, name="ml-logger", level="WARNING"):
        """Initialization

        :param logfile:  String path of logfile to use
        :param name:  Name of the logger (optional)
        :param level:  Debugging level desired (optional)
        """
        self.log = logging.getLogger(name)
        self.log.setLevel(getattr(logging, level))
        self.log.propagate = False

        formatter = logging.Formatter(
            '%(created)i %(asctime)s [%(filename)s:%(lineno)d] '
            '%(levelname)s: %(message)s', "%Y%m%d %H:%M:%S")

        #  Check to make sure we don't add extra handlers
        if not self.log.handlers:
            fh = logging.FileHandler(logfile)
            fh.setFormatter(formatter)
            self.log.addHandler(fh)

        if len(self.log.handlers) < 2 and level == "DEBUG":
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            self.log.addHandler(ch)

    def get_logger(self):
        """Return the logger"""
        return self.log

    def now(self):
        """return the current time"""
        return datetime.datetime.now()

    def starttime(self):
        """Set a start time"""
        self._starttime = datetime.datetime.now()

    def endtime(self):
        """Set an end time"""
        self._endtime = datetime.datetime.now()

    def get_execution_time(self, time_format="seconds"):
        """Get total execution time from starttime and endtime

        :param time_format:  Format to return timestamp.  Currently only seconds
        :return:  Execution time in format
        """
        exec_time = self._endtime - self._starttime

        if time_format == "seconds":
            return exec_time.total_seconds()

        return exec_time
