import datetime
import os
import sys
from threading import Thread
import time
import dropbox
import picamera
from dropbox.exceptions import ApiError, AuthError


ACCESS_TOKEN = ''  # Fill Dropbox access token
CAMERA_RESOLUTION = (2592, 1944)


def generate_file_name():
    return (datetime.datetime.now()).strftime('%Y-%m-%d_%H-%M-%S.jpeg')


def take_photo():
    photo_file_name = generate_file_name()
    with picamera.PiCamera() as camera:
        camera.resolution = CAMERA_RESOLUTION
        camera.capture(photo_file_name)
    return photo_file_name


def upload_to_dropbox(file_name):
    print('Creating a Dropbox object')
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    try:
        dbx.users_get_current_account()
    except AuthError as arr:
        sys.exit('ERROR: Invalid access token; try re-generating an access token from the app console at dropbox.com')

    folder = file_name[:10]
    upload_path = '/{}/{}'.format(folder, file_name)

    with open(file_name, 'rb') as f:
        print('Uploading ' + file_name + ' to Dropbox')
        try:
            dbx.files_upload(f.read(), upload_path)
        except ApiError as err:
            print('Fuck')
            print(err)


def delete_local_file(file_name):
    os.system('rm ' + file_name)
    print('File {} deleted'.format(file_name))


def take_and_upload_photo():
    photo_file = take_photo()
    upload_to_dropbox(photo_file)
    delete_local_file(photo_file)


def is_sunny():
    return 5 <= (datetime.datetime.now()).hour <= 18


def run():
    while True:
        if is_sunny():
            take_and_upload_photo()
        time.sleep(180)  # 3 minutes


if __name__ == "__main__":
    run()
