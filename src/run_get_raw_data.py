import os
from mne.utils import _fetch_file
import zipfile 
url = "https://uc494b528f2d51052f61e34e3a55.dl.dropboxusercontent.com/cd/0/get/AIhnLZVOaaBOp3Qa8ulOR_9kgl5WOLsxaNOlF70VPyLtieaC8T5nxgnmifnUY0Wq_1WXuQu2ivAW_787bSnW0jydmbi5uZWCvjiByYQQ7RMOXyPKNQ5WcbF6U61pwMmtpZWn-LGz2rZDvi3DU3WKsQhnw7msBMh10b4ZuOUB0aUcJbEGNyvIfVDYbvpnnrS2VrI/file?_download_id=3170314809379957726895780297864946905675172882621103847177491497&_notify_domain=www.dropbox.com&dl=1"
file = '../data/RAW/EEG/Nathalie-78_20171118_123017.mff.zip'
_fetch_file(url, file, print_destination=True)
eeg_zip = zipfile.ZipFile(file)
eeg_zip.extract('Nathalie-78_20171118_123017.mff', path='../data/RAW/EEG/')
eeg_zip.close()