import os

current_directory = os.getcwd()
os.chdir(current_directory)

from coastal_model.server import server

server.launch(open_browser=True)