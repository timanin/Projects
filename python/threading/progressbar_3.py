#!/usr/bin/env python3

"""Create a progress bar for applications that can keep track of a
download in progress. The progress bar will be on a separate thread
and will communicate with the main thread using delegates."""

import requests


def get_size(url):
    """Checks the remote file size."""
    req = requests.head(url)
    return int(req.headers['Content-Length'])


def download(url, filename):
    """Downloads the specified URL into filename."""
    downloaded = 0
    file_size = get_size(url)
    req = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in req.iter_content(chunk_size=1024):
            file.write(chunk)
            downloaded += 1024
            percent_downloaded = int(100 * downloaded / file_size)
            yield percent_downloaded


def print_progress(percent):
    """Prints progress to stdout."""
    hashes = '#' * int(percent / 2)
    print('Progress: {:s} ({:d}%)'.format(hashes, percent),
          end='\r', flush=True)
    if percent == 100:
        print('')


def make_url(domain_name, query_path, filename):
    """Return a full URL."""
    return 'https://{d}/{q}/{f}'.format(
        d=domain_name,
        q=query_path,
        f=filename
    )


def main():
    """main function"""

    filename = 'Skype_7.56.776.dmg'
    url = make_url(
        'download.skype.com',
        'macosx/26d34dde05a09c44a8a29fa28eb15940',
        filename
    )

    for i in download(url, filename):
        print_progress(i)

if __name__ == '__main__':
    main()
