# Jitsi Face Recognition application

This project implements a server/client application. The application is used to perform real time face recognition with
the DNI and the person face. It also implements the identification of the person along a DB. Finally, it implements
a series of test that check whether the person is alive.

## Applications

When running the client, a Jitsi conference is established.Then, there are 3 main applications:

* **Face recognition**: Detects two faces (for example; DNI and person face) and returns the level of similitude/
accuracy in %.
* **Check life**: A series of tests which consists of:
    * Move the head to the left.
    * Move the head to the right.
    * Move the head to the top.
    * Move the head to the bottom.
* **Face recognition along DB**: Captures a face and search it in a DB. Finally, it returns the identified person and 
the level of similitud/accuracy in %. (The DB must contain the field of the name and the pertinent encoded face)

## How to install?

There are several dependencies that you must install before use it. Follow the instructions below:

* *(Optional) Use Pycharm and creates a new Project. Put all the files in the root Project folder.*
* Use a venv with **python3.8.3** *(Only tested with this version)*.
* Install the requirements.txt (*pip install -r requirements.txt*)
* Now, it will be mandatory to perform the following: 
    * *pip install cmake (I may carry some error if a c compiler is not installed)*
    * *pip install dlib*
    * *pip install face-recognition*

Right now, the application may be ready to run. Just run the main.py and the flask framework will runs the server. Then, open
a browser and put the URL where the server is actually running. *By default, flask runs in http://127.0.0.1:5000/.*

