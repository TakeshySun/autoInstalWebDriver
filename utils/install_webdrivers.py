import sys
import glob
import gzip
import os
import requests
import urllib
import zipfile

from setuptools import Command


class InstallWebDrivers(Command):
    description = 'Installs web drivers'

    user_options = []

    # This method must be implemented
    def initialize_options(self):
        pass

    # This method must be implemented
    def finalize_options(self):
        pass

    def run(self):
        print('Installing Web Drivers for platform {}'.format(sys.platform))
        download_dir = os.path.join(os.path.abspath(os.curdir), 'web_drivers')

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        files = glob.glob(os.path.join(download_dir, '*'))
        files_to_download = []
        here = os.path.abspath(os.path.curdir)

        win_platform = 'win'
        linux_platform = 'linux'

        print("Web Drivers files to delete: {}".format(files))
        for f in files:
            os.remove(f)

        if linux_platform in sys.platform:
            files_to_download = [
                'https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz',
                'https://chromedriver.storage.googleapis.com/2.39/chromedriver_linux64.zip'
            ]

        elif win_platform in sys.platform:
            files_to_download = [
                'http://selenium-release.storage.googleapis.com/3.12/IEDriverServer_x64_3.12.0.zip',
                'https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-win64.zip',
                'https://chromedriver.storage.googleapis.com/2.39/chromedriver_win32.zip'
            ]

        for url in files_to_download:
            drivers_dir = os.path.join(here, "web_drivers")
            driver_archive_name = os.path.join(drivers_dir, url.split(r'/')[-1])
            print("Downloading and installing web driver {}".format(driver_archive_name))
            ext = driver_archive_name.split(r'.')[-1]
            driver_archive_path = os.path.join(drivers_dir, url.split("/")[-1])

            urllib.request.urlretrieve(url, driver_archive_path)

            if ext == 'zip':
                unarchived_file_path = driver_archive_path[:-4]
                if 'chromedriver' in unarchived_file_path:
                    unarchived_file_path = unarchived_file_path[:-8]
                zip_ref = zipfile.ZipFile(driver_archive_path, 'r')
                zip_ref.extractall(drivers_dir)
                zip_ref.close()

                if linux_platform in sys.platform:
                    import subprocess
                    subprocess.run("chmod +x {}".format(unarchived_file_path), shell=True, check=True)

            elif ext == 'gz':
                unarchived_file_path = driver_archive_path[:-7]
                with open(unarchived_file_path, 'wb') as in_file:
                    with gzip.open(driver_archive_path, 'wb') as out_file:
                        content = b''
                        out_file.write(content)

                if linux_platform in sys.platform:
                    import subprocess
                    subprocess.run("chmod +x {}".format(unarchived_file_path), shell=True, check=True)

            os.remove(driver_archive_path)
