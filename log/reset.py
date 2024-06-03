# Function to clear the content of a file
def clear_file_content(file_path):
    try:
        # Open the file in write mode, which will clear its content
        with open(file_path, 'w') as file:
            pass  # Do nothing, just open and close the file to clear it
        print(f"Successfully cleared the content of the file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the path to the file you want to clear
file_path_DBmypot = '/home/os/TestHoneypot/log/DBmypot.txt'
file_path_DBcowrie = '/home/cowrie/cowrie/var/log/cowrie/cowrie.log'
file_path_DBdionaea = '/opt/dionaea/var/log/dionaea/dionaea.log'

# Call the function to clear the file content
clear_file_content(file_path_DBmypot)
clear_file_content(file_path_DBcowrie)
clear_file_content(file_path_DBdionaea)