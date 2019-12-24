# Project 2

Web Programming with Python and JavaScript

## Application Logic

When the user is visiting the landing page (127.0.0.1:5000) for the very first time, he/she is asked to provide a screen name, which is saved in the domain's local storage, and then the user is redirected to the messaging page.

When the user is visiting the landing page again, a JavaScript dialog is showing his/her name, and there is possible to continue to the messaging page by pressing "Ok", or to sign in as a different user.

The messaging page contains a section for the channel list, a section for the messages of the currently selected channel, and respectively buttons for managing the user interface.

As a "personal touch" I've added a section with a list of private messages sent to the current user (more like a mailbox) - it can be opened by hitting the "padlock" icon.

All user names are clickable, hitting them opens a dialog for sending a private message to the respective user.

## Implementation

The project is a POC, not intended to be used "as is" in real-world scenarios.

The mock database includes two GLOBAL memory variables: 
- a user dictionary - with user names as keys and roles as values (updated directy in the Python source code)
- a channel dictionary - with channel names as keys and deques as values (each deque is storing a list of maximum 100 message objects, as required)

The channel dictionary is stored in the server application's memory: saved ad-hoc in a text file, and then restored at application start-up.

On the landing page there is no authentication and authorization, those features are supposed to be resolved by a different module. The landing page itself is a mock.

The channel list and the message lists are pulled from the server via http requests.

When the user is creating a new channel, the new channel name is sent to the server via http request, and then broadcasted to all connected users via socketio.

When the user is submitting a message, the message is sent to the server and then broadcasted to the connected channel users (room) via socketio. The private messages are not broadcasted.

A user is joined only to the channel (room) with messages currently listed on the page. The private message list is not associated to any particular room.

#### My Configuration 

- Windows 10 Pro
- Python 3.8 with current flask and flask-socketio
- socket.io 1.3.6

#### As of December 2019:
Due to changes in python, flask and flask-socketio, when testing the application, please use the following command line command:
python application.py


## Project Files and Folders 

- application.py - source code
- mess.json - text file, a backup of my test data (channels and messages), it's loaded into the server application's memory (when being started)
- README.md - this file
- requirements.txt - as received, no additional items
- socketerrors.log - text file intended to log socketio errors, also used for verifying the program logic

#### static folder 

- add.png, cancel.png, chat.png, list.png, lock.png, logo.png, roll.png, save.png, send.png - images used on the two web pages
- app.css - style sheet
- chat.js - source file, event handlers and helper functions used on the messaging page
- home.js - source file, event handlers used on the landing page

#### templates folder 

- chat.html - template for the messaging page
- home.html - template for the landing page
