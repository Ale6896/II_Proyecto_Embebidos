import PySimpleGUI as sg
import paramiko
import os
import ast

# Function to connect to Raspberry Pi
def connect_to_raspberry(ip_address, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the Raspberry Pi
        client.connect(ip_address, username=username, password=password)
        print(f"Connected to {ip_address}")

        return client
    
    except paramiko.AuthenticationException:
        print(f"Failed to connect to {ip_address} (Authentication failed)")
    except paramiko.SSHException as e:
        print(f"Failed to connect to {ip_address} ({str(e)})")
    print("Connecting to Raspberry Pi...")

# Function to check if the application in computer B is running
def is_application_running(client, application_name):

    # Check if the application is running
    command = f"pgrep -f {application_name}"
    stdin, stdout, stderr = client.exec_command(command)
    process_list = stdout.read().decode().splitlines()

    if process_list:
        print(f"The application '{application_name}' is running on Raspberry.")
        return True 
    else:
        print(f"The application '{application_name}' is not running on Raspberry.")
        return False

# Function to disconnect from Raspberry Pi
def disconnect_from_raspberry(client):
    _, stdout, _ = client.exec_command('hostname')
    hostname = stdout.read()
    # Close the SSH connection
    print("Disconnecting from Raspberry Pi...")
    client.close()
    print(f"Connection closed to {hostname}")

# Function to run the application in computer B
def run_application(client, application_name):
    print("Running app on Raspberry")
    stdin, stdout, stderr = client.exec_command(f"python3 {application_name}")
    """
    # Read the output and error messages
    #output = stdout.read().decode()
    errors = stderr.read().decode()
    # Check if there were any errors
    if errors:
        print("Error executing the program on computer B")
        print("Error message:")
        print(errors)
    else:
        print("Program executed successfully on computer B")
        print("Output:")
        #print(output)"""
    
# Function to stop the application in computer B
def stop_application(client, application_name):
    print("Stopping app on Raspberry")

    # Execute command to stop the application
    command = f"pkill -f {application_name}"
    client.exec_command(command)

    print(f"The application '{application_name}' has been stopped on computer B.")

# Function to update settings
def update_settings(client, host_folder, settings_file, client_folder):
    # Add your code here for updating settings
     # Open the settings file
    settings_file = host_folder + settings_file  # Replace with the path to your settings file
    with open(settings_file, "r") as file:
        current_settings = file.read()

    # Create the update settings layout
    update_settings_layout = [
        [sg.Multiline(default_text=current_settings, key="-SETTINGS_INPUT-", size=(50, 10))],
        [sg.Button("Save", key="-SAVE_SETTINGS-", size=(10, 1))]
    ]

    # Create the update settings window
    update_settings_window = sg.Window("Update Settings", update_settings_layout)

    # Event loop for the update settings window
    while True:
        event, values = update_settings_window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-SAVE_SETTINGS-":
            # Save the updated settings to the file
            updated_settings = values["-SETTINGS_INPUT-"]
            with open(settings_file, "w") as file:
                file.write(updated_settings)
            break

    # Close the update settings window
    update_settings_window.close()

    # Sends the settings file to Raspberry
    send_file(client, settings_file, client_folder)

    print("Updating settings...")

# Function to send a file through SSH
def send_file(client, settings_file, client_folder):
    try:
        # Create an SCP client
        scp_client = client.open_sftp()

        # PATH to settings file on Raspberry
        destination_path = settings_file

        # Copy the file from computer A to computer B
        scp_client.put(settings_file, destination_path)

        # Close the SCP client and SSH connection
        scp_client.close()
    except Exception as e:
        print("An error occurred:", str(e))


# Function to import folder
def import_data(client, client_images_folder, host_images_folder, labels_file):
    print("Importing data...")
    try:
        # Create an SCP client
        scp_client = client.open_sftp()

        # Import labels file from computer B to computer A
        #destination_path = os.path.join(host_folder, labels_file)
        #scp_client.get(source_folder, destination_path)

        # Get a list of files in the source folder on computer B
        file_list = scp_client.listdir(client_images_folder)

        # Copy each file from the source folder to the destination folder on computer A
        for file_name in file_list:
            source_path = os.path.join(client_images_folder, file_name)
            destination_path = os.path.join(host_images_folder, file_name)
            scp_client.get(source_path, destination_path)

        # Close the SCP client and SSH connection
        scp_client.close()

        print("Files copied successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to compare data
def compare_data(host_folder, images_folder, labels_file):
    # Add your code here for comparing data
    print("Comparing data...")
    image_folder = images_folder  # Replace with the path to your image folder

    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Create the image shower window layout
    image_shower_layout = [
        [
            sg.Listbox(values=image_files, size=(60, 20), key="-IMAGE_LIST-", enable_events=True),
            sg.Image(key="-IMAGE_PREVIEW-", size=(640, 480)),
        ],
        [sg.Text("Label:", font=("Helvetica", 18)), sg.Text("", key="-LABEL-", font=("Helvetica", 18))]
    ]

    # Create the image shower window
    image_shower_window = sg.Window("Image Shower", image_shower_layout)

    # Load the labels dictionary from the text file
    labels_dict = {}
    with open(host_folder + labels_file, "r") as file:
        content = file.read()
        if content:
            labels_dict = ast.literal_eval(content)

    # Event loop for the image shower window
    while True:
        image_event, image_values = image_shower_window.read()

        if image_event == sg.WINDOW_CLOSED:
            break
        elif image_event == "-IMAGE_LIST-":
            selected_image = image_values["-IMAGE_LIST-"][0]
            image_path = os.path.join(image_folder, selected_image)
            image_shower_window["-IMAGE_PREVIEW-"].update(filename=image_path)

            if selected_image in labels_dict:
                label = labels_dict[selected_image]
                image_shower_window["-LABEL-"].update(label)
            else:
                image_shower_window["-LABEL-"].update("No label")

    # Close the image shower window
    image_shower_window.close()

# Function to verify connection
def verify_connection(client):
    if client is None:
        return False
    return True  # Replace with your verification logic

# Create the GUI layout
layout = [
    [sg.Text("Connection Status: ", font=("Helvetica", 12)), sg.Text("Disconnected", key="-STATUS-", font=("Helvetica", 12), background_color="red")],
    [sg.Text("Application Running", font=("Helvetica", 12)), sg.Text("Application Not Running", key="-APP_STATUS-", font=("Helvetica", 12), background_color="red")],
    [sg.Button("Connect", size=(10, 2), key="-CONNECT-"), sg.Button("Update Settings", size=(15, 2), key="-UPDATE_SETTINGS-")],
    [sg.Button("Request Data", size=(10, 2), key="-REQUEST_DATA-"), sg.Button("Compare Data", size=(10, 2), key="-COMPARE_DATA-")],
    [sg.Button("Run App", key="-RUN_APP-", size=(15, 1), pad=((5, 5), (10, 0)))],
    [sg.Image(key="-IMAGE-")]
]

# Create the window
window = sg.Window("Face Emotion Detector", layout)

connected = False  # Initially set the connected status as False

# Usage
username = "ale6896"  # Replace with your username on computer B
password = "1"  # Replace with your password on computer B
ip_address = "192.168.1.106"  # Replace with the IP address of computer B
client_folder = "/home/ale6896/to/"  # Replace with the path to the source folder on computer B
host_folder = "/home/ale6896/to/"  # Replace with the path to the destination folder on computer A
application_name = "app.py" # Application name to check if running
client_images_folder = "/home/ale6896/to/Images/" # Folder where pictures are saved
host_images_folder = "/home/ale6896/to/Images/" # Folder where pictures are saved
settings_file = "settings.txt" # File to define application settings. Path has to be from host_file
labels_file = "labels.txt" # File to check predictions. Path has to be from host_file

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-CONNECT-":
        if connected:
            client = disconnect_from_raspberry(client)
            connected = verify_connection(client)
            window["-STATUS-"].update("Disconnected", background_color="red")
            window["-CONNECT-"].update("Connect")
        else:
            client = connect_to_raspberry(ip_address, username, password)
            connected = verify_connection(client)
            if connected:
                window["-STATUS-"].update("Connected", background_color="green")
                window["-CONNECT-"].update("Disconnect")
    elif event == "-UPDATE_SETTINGS-":
        update_settings(client, host_folder, settings_file, client_folder)
    elif event == "-REQUEST_DATA-":
        import_data(client, client_images_folder, host_images_folder, labels_file)
    elif event == "-COMPARE_DATA-":
        compare_data(host_folder, host_images_folder, labels_file)
        window["-STATUS-"].update("Connected", background_color="green")
        window["-CONNECT-"].update("Disconnect")

    elif event == "-RUN_APP-":
        if connected:
            if window[event].get_text() == "Run App":
                # Call the run_application function
                run_application(client, application_name)
                window[event].update("Stop App")
            else:
                # Call the stop_application function
                stop_application(client, application_name)
                window[event].update("Run App")
        else:
            print("Not connected to Raspberry")

    # Verify connection and update the status display
    connection_status = verify_connection(client)
    if connection_status:
        window["-STATUS-"].update("Connected", background_color="green")
        connected = True
        window["-CONNECT-"].update("Disconnect")
    else:
        window["-STATUS-"].update("Disconnected", background_color="red")
        connected = False
        window["-CONNECT-"].update("Connect")

    # Update the application status
    if connection_status:
        if is_application_running(client, application_name):
            window["-APP_STATUS-"].update("Application Running", background_color="green")
        else:
            window["-APP_STATUS-"].update("Application Not Running", background_color="red")


# Close the window
window.close()

