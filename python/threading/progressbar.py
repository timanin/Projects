#!/usr/bin/env python3

"""Create a progress bar for applications that can keep track of a
download in progress. The progress bar will be on a separate thread
and will communicate with the main thread using delegates."""

import threading
from time import sleep
import requests


class Downloader(object):
    """The thing that downloads"""

    def __init__(self, url, filename):
        """Initialiser"""
        self.url = url
        self.filename = filename
        self.downloaded = 0
        self.request = None

    def download(self):
        """Starts the download"""
        self.request = requests.get(self.url, stream=True)
        with open(self.filename, 'wb') as file:
            for chunk in self.request.iter_content(chunk_size=128):
                file.write(chunk)
                self.downloaded += 128

    def get_size(self):
        """Checks the remote file size"""
        req = requests.head(self.url)
        return int(req.headers['Content-Length'])


class ProgressBar(object):
    """Progress bar as a delagate"""

    def __init__(self, url, filename):
        """Initialiser"""
        self.downloader = Downloader(url, filename)
        self.threads = []

    def download(self):
        """Starts the download"""
        self.downloader.download()

    def check_progress(self):
        """Prints the download progress"""
        size = self.downloader.get_size()

        done = 0
        while done < size:
            done = self.downloader.downloaded
            progress = int(done * 100 / size)
            # print('Progress: {:d}%'.format(progress), end='\r', flush=True)
            hashes = '#' * int(progress / 2)
            print('Progress: {:s} ({:d}%)'.format(hashes, progress),
                  end='\r', flush=True)
            sleep(1)
        print('')

    def run(self):
        """Main method"""
        thread1 = threading.Thread(target=self.download)
        self.threads.append(thread1)

        thread2 = threading.Thread(target=self.check_progress)
        self.threads.append(thread2)

        thread1.start()
        thread2.start()


def main():
    """main function"""

    domain_name = 'distfiles.gentoo.org'
    query_path = '/releases/amd64/autobuilds/20170629/'
    filename = 'install-amd64-minimal-20170629.iso'
    url = 'http://{d}/{q}/{f}'.format(
        d=domain_name,
        q=query_path,
        f=filename
    )

    downloader = ProgressBar(url, filename)

    downloader.run()


if __name__ == '__main__':
    main()
