# Embedded System for Facial Expression Recognition and Classification

In this project, a Linux image is created using the Yocto Project and stored on a Raspberry Pi system in order to use an application capable of detecting emotions through images taken with a camera and classified using an emotion recognition model from the TensorFlow library.

### Graphical Application GUI.py

This file creates a graphical application that runs from a Host computer and, using an SSH connection, is capable of launching the emotion recognition application stored on the Raspberry Pi without the need to use the command line.

#### Application functionalities

For this application, the **_PySimpleGui_** library is used to create a simple interface that includes some buttons, so the user does not need to use command window.

The Python library **_Paramiko_** is used to establish an SSH connection. The included commands are:

- Host connection to Raspberry: A button is provided to create the connection link. Additionally, a visual aid is included to indicate when the Host is connected and disconnected.
- Execution of the application on Raspberry: A button is included to execute and stop the emotion recognition application. Additionally, a visual aid is included to indicate when the application is running.
- Settings update: A button is included to edit the application's execution settings. The file is sent to the Raspberry Pi through the same connection.
- Information request: A button is included to request the Raspberry Pi to send the data of photos and the file containing their classification.
- Information comparison: A button is included to review the received photos and observe the emotion assigned by the model.

#### How to use

In order to get a conection between Host Computer and Raspberry Pi, it is requiered for the user to add _Username_, _Password_ and _IP Address_. Moreover, user needs to specify a PATH to the Folder where the application is going to save the receiving data and a PATH to specify where is the settings file.