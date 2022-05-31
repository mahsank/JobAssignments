#!/usr/bin/env python3
"""
This script solves the problem described below:

    Develop a Python command line utility that takes architecture (amd64, arm64, mips etc.) as an argument and downloads
    the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output
    the statistics of the top 10 packages that have most files associated with them. An example output could be:
    ./package_statistics.py amd64

    *<package name 1> <number of files>
    *<package name 2> <number of files>
    ...
    *<package name 10> <number of files>

"""

__author__ = 'Muhammad Ahsan'
__version__ = '0.1'
__copyright__ = 'Copyright (C) 2021 Muhammad Ahsan'
__license__ = 'CC BY-SA'

import os.path
import sys, argparse, logging
import requests, gzip
from requests.exceptions import HTTPError
import pandas as pd

# create or obtain a logger
logger = logging.getLogger(__name__)

# set log level
logger.setLevel(logging.DEBUG)

# create a stream and file handler and set log file format
stream_handler =  logging.StreamHandler()
stream_format = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(stream_format)
file_handler = logging.FileHandler('packagestats.log')
file_format = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_format)

# add stream and file handler to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class PackageStats(object):
    """A class to gather package statistics from architecture specific compressed files and display top n packages with
    most files"""

    def __init__(self, arch, top_n_entries):
        """Initialize the architecture and entries artibutes"""

        self.architecture = arch
        self.entries = top_n_entries

    def getContentIndices(self):
        """Get Content indices"""

        url = 'http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{}.gz'.format(self.architecture)
        self.filename = url.split('/')[-1]
        default_request_timeout = 120
        if os.path.exists(self.filename):
            logger.info(f"File is already available, using {self.filename} file")
            return
        try:
            logger.info("Fetching Contents-{} from the URL {}.".format(self.architecture, url))
            response = requests.get(url, timeout=default_request_timeout)
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            sys.exit(1)
        except Exception as err:
            logger.error(f"Exception occurred while trying to fetch {self.filename}: {err}")
            sys.exit(1)
        else:
            open(self.filename, 'wb').write(response.content)

    def collectPackageStats(self):
        """Read content indices and collect package statistics"""

        logger.info(f"Collecting package statistics for top {self.entries} packages")
        try:
            df = pd.read_table(self.filename, header=None, delim_whitespace=True, usecols=[1], names=['Utilities'])
            max_files = df['Utilities'].value_counts().nlargest(self.entries)
        except Exception as err:
            logger.error(str(err), exc_info=True)
            sys.exit(1)
        else:
            logger.info("Displaying requested package statistics")
            print()
            print("---------------------------------------------")
            print(max_files.to_string())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command line utility to parse package Content Indices and display \
            top n packages with most files")
    parser.add_argument("--arch",dest="architecture", required=True, help="Processor architecture", \
            choices=['amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips64el', 'mipsel', 'ppc64el', 'ppc64el', 's390x'], \
            type=str)
    parser.add_argument("--max-file-packages", dest="entries", required=True, help="Number of packages with most \
            files associated with them to retrieve", type=int)
    args = parser.parse_args()

    new_packagestats = PackageStats(arch=args.architecture,top_n_entries=args.entries)

    new_packagestats.getContentIndices()
    new_packagestats.collectPackageStats()
