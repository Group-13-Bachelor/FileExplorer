from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog
import Controller
from PyQt5 import uic
import sys
import zmq
from time import sleep

# Initialize a zmq Context
context = zmq.Context.instance()
publisher = context.socket(zmq.PAIR)
publisher.bind("inproc://endpoint")
sleep(1)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("mainwindow.ui", self)

        # Start a thread to handle events from the UI
        controller_thread = Thread(target=Controller.Listener.__init__, args=(Controller.Listener, context))
        controller_thread.daemon = True
        controller_thread.start()

        sleep(4)

        # File button widgets
        self.newFileButton = self.findChild(QPushButton, "newFileButton")
        self.openFileButton = self.findChild(QPushButton, "openFileButton")
        self.copyFileButton = self.findChild(QPushButton, "copyFileButton")
        self.deleteFileButton = self.findChild(QPushButton, "deleteFileButton")

        # Folder Button widgets
        self.newFolderButton = self.findChild(QPushButton, "newFolderButton")
        self.copyFolderButton = self.findChild(QPushButton, "copyFolderButton")
        self.deleteFolderButton = self.findChild(QPushButton, "deleteFolderButton")

        #Label widget
        self.label = self.findChild(QLabel, "label")

        #Define Widgets
        self.newFileButton.clicked.connect(self.new_file)
        self.openFileButton.clicked.connect(self.open_file)
        self.copyFileButton.clicked.connect(self.copy_file)
        self.deleteFileButton.clicked.connect(self.delete_file)

        self.newFolderButton.clicked.connect(self.new_folder)
        self.copyFolderButton.clicked.connect(self.copy_folder)
        self.deleteFolderButton.clicked.connect(self.delete_folder)

        self.show()


    def select_file(self):
        # Get filename with path and filetype
        filename = QFileDialog.getOpenFileName(self, "Choose File", "c:\\", "All Files (*)")

        return filename

    def select_folder(self):
        # Get name of the folder selected
        foldername = QFileDialog.getExistingDirectory(self, 'Select Directory')

        return foldername

    def new_file(self):
        # Get filename with path and filetype
        filename = QFileDialog.getSaveFileName(self, 'Select Directory')
        # Check if a file was selected
        if filename[0]:
            event = b'create_new_file'
            filename = str(filename[0])

            # Send event to controller
            self.send(event, filename)

    def open_file(self):
        # Get filename with path and filetype
        filename = self.select_file()
        # Check if a file was selected
        if filename[0]:
            event = b'open_file'
            filename = str(filename[0])

            self.send(event, filename)

    def copy_file(self):
        # Get filename with path and filetype
        filename = self.select_file()
        # Check if a file was selected
        if filename[0]:
            event = b'copy_file'
            filename = str(filename[0])

            self.send(event, filename)

    def delete_file(self):
        # Get filename with path and filetype
        filename = self.select_file()
        # Check if a file was selected
        if filename[0]:
            event = b'delete_file'
            filename = str(filename[0])

            self.send(event, filename)

    def new_folder(self):
        # Get foldername with path
        foldername = self.select_folder()
        # Check if a folder was selected
        if foldername:
            event = b'new_folder'
            self.send(event, foldername)

    def copy_folder(self):
        # Get foldername with path
        foldername = self.select_folder()
        # Check if a folder was selected
        if foldername:
            event = b'copy_folder'
            self.send(event, foldername)

    def delete_folder(self):
        # Get foldername with path
        foldername = self.select_folder()
        # Check if a folder was selected
        if foldername:
            event = b'delete_folder'
            self.send(event, foldername)

    # Send event
    def send(self, event, data):
        # Store the event and data as a list
        msg = [event, str(data).encode('ascii')]
        # Send the list to controller
        publisher.send_multipart(msg)
        print("Message sent")


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()