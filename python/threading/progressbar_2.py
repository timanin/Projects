#!/usr/bin/env python3

"""Create a progress bar for applications that can keep track of a
download in progress. The progress bar will be on a separate thread
and will communicate with the main thread using delegates."""

import threading
from time import sleep
import requests


downloaded = 0


def download(url, filename):
    """Downloads the specified URL into filename."""
    global downloaded
    req = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in req.iter_content(chunk_size=128):
            file.write(chunk)
            downloaded += 128


def get_size(url):
    """Checks the remote file size."""
    req = requests.head(url)
    return int(req.headers['Content-Length'])


def check_progress(url):
    """Prints the download progress."""
    size = get_size(url)

    done = 0
    while done < size:
        done = downloaded
        progress = int(done * 100 / size)
        hashes = '#' * int(progress / 2)
        print('Progress: {:s} ({:d}%)'.format(hashes, progress),
              end='\r', flush=True)
        sleep(1)
    print('')


def download_with_progress(url, filename):
    """
    Runs two threads: one to download and another to observe and print
    out the progress.
    """

    threads = []
    thread1 = threading.Thread(target=download, args=(url, filename))
    threads.append(thread1)
    thread2 = threading.Thread(target=check_progress, args=(url,))
    threads.append(thread2)

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

    download_with_progress(url, filename)


if __name__ == '__main__':
    main()
