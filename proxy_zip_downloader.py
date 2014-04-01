"""
Logs into the specified gmail account and downloads the latest 2 HideMyAss Zip 
proxy files to abs_path_zips. Any other zip file in that folder is removed.

   python proxy_zip_downloader.py gmail_username gmail_pass abs_path_to_fldr

"""

import datetime
from gmail import Gmail
import os, sys

class ProxyZipDownloader:

    def __init__(self, username, password, abs_path_zips):
        self.username = username
        self.password = password
        self.abs_path_zips = abs_path_zips
        self.g = Gmail()
        self.g.login(username, password)
    
    def __remove_all_zips__(self):
        for file_name in os.listdir(self.abs_path_zips):
            if file_name.endswith(".zip"):
                file_to_remove = self.abs_path_zips + file_name
                print "Removing %s" % file_to_remove
                os.remove(file_to_remove)


    def __is_zip_file_old__(self, file_name):
        # proxylist-10-26-13.zip
        date_zip_file = datetime.datetime.strptime(file_name, \
                                                           'proxylist-%m-%d-%y.zip')
        date_today = datetime.datetime.now()
        return (date_today - date_zip_file).days >= 2

    def fetch_files(self):
        self.__remove_all_zips__()
        for email in self.g.inbox().mail(sender="noreply@pl.hidemyass.com"):
            message = email.fetch()

            m1 = message.get_payload()[0]
            m2 = message.get_payload()[1]

            zip_file_name = m2.get_filename()
            if self.__is_zip_file_old__(zip_file_name):
                continue

            zip_file_contents = m2.get_payload(decode=True)
                    
            print "Saving %s" % zip_file_name
            f = open(self.abs_path_zips + zip_file_name, 'w')
            f.write(zip_file_contents)
            f.close()


if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    abs_path_zips = sys.argv[3]
    pzd = ProxyZipDownloader(username, password, abs_path_zips)
    pzd.fetch_files()
