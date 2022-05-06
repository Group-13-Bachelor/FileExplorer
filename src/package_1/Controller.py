import sys
import zmq
from time import sleep
import os
import shutil


class Listener():
    def __init__(self, context):
        #Connect to the UI through inproc
        ctx = zmq.Context.instance()
        sleep(2)
        subscriber = ctx.socket(zmq.PAIR)
        subscriber.connect("inproc://endpoint")

        while True:
            # Wait for events from the UI
            event, data = subscriber.recv_multipart()
            print(f'Received event: {event}')

            if event == b'create_new_file':
                new_file(data)
            elif event == b'open_file':
                open_file(data)
            elif event == b'copy_file':
                copy_file(data)
            elif event == b'delete_file':
                delete_file(data)
            elif event == b'new_folder':
                new_folder(data)
            elif event == b'copy_folder':
                copy_folder(data)
            elif event == b'delete_folder':
                delete_folder(data)


# Create new file
def new_file(path):
    try:
        open(path, 'a').close()
    except OSError:
        print('Failed creating a new file')
    else:
        print('Created new file')


# Open file using default program
def open_file(path):
    if os.path.isfile(path):
        os.startfile(path)
        print('Opened file')
    else:
        print('Failed to open file, file not found')


# Copy a file
def copy_file(path):
    if os.path.isfile(path):
        stripped, extension = os.path.splitext(path)
        newpath = stripped + b'_copy' + extension
        shutil.copy(path, newpath)
        print(f'Copied file, new filename: {newpath}')
    else:
        print('Failed to copy file, file not found')


# Delete a file
def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
        print('Deleted file')
    else:
        print('Failed to delete file, file not found')


# Create new folder
def new_folder(path):
    path = path + b'/newfolder/'
    if not os.path.exists(path):
        os.makedirs(path)
        print('Created new folder')
    else:
        print('Failed to create folder, folder already exists')


# Copy existing folder
def copy_folder(path):
    print(path)
    destination = path + b'_copy'

    if os.path.exists(path):
        shutil.copytree(path, destination)
        print('Copied folder')
    else:
        print('Failed to copy some files')


# Delete folder
def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print('Deleted folder')
    else:
        print('Failed to delete folder, folder not found')
