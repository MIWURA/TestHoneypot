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
file_path = '/home/os/TestHoneypot/log/DBmypot.txt'

# Call the function to clear the file content
clear_file_content(file_path)
