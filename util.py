import functools
import os
import shutil
import requests
import sys
import re
try:
    from google.colab import drive
except:
    pass

def download_file(url, file_name):
    # adapted from https://stackoverflow.com/a/39217788/5013267
    with requests.get(url, stream=True) as r:
        with open(file_name, 'wb') as f:
            r.raw.read = functools.partial(r.raw.read, decode_content=True)
            shutil.copyfileobj(r.raw, f)

def download_from_drive_id(drive_id, file_name):
    pre_url = "https://drive.google.com/u/0"
    html = requests.get(pre_url + "/uc?id={}&export=download".format(drive_id)).text
    confirm_code = re.search(r'href="\/uc\?export=download&amp;confirm=(.+?)&amp;', html).group(1)
    download_file(pre_url + "/uc?export=download&confirm={}&id={}".format(confirm_code, drive_id), file_name)


# the following code is from https://github.com/minimaxir/gpt-2-simple/blob/master/gpt_2_simple/gpt_2.py

def mount_gdrive():
    """Mounts the user's Google Drive in Colaboratory."""
    assert 'google.colab' in sys.modules, "You must be in Colaboratory to mount your Google Drive"

    drive.mount('/content/drive')

def is_mounted():
    """Checks if the Google Drive is mounted."""
    assert os.path.isdir('/content/drive'), "You must mount first using mount_gdrive()"

def copy_file_to_gdrive(file_path):
    """Copies a file to a mounted Google Drive."""
    is_mounted()

    shutil.copyfile(file_path, "/content/drive/My Drive/" + file_path)

def copy_file_from_gdrive(file_path):
    """Copies a file from a mounted Google Drive."""
    is_mounted()

    shutil.copyfile("/content/drive/My Drive/" + file_path, file_path)
