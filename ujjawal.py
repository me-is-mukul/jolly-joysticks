from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

# Path to the local file
path = "H:/jolly-joystics/jolly-joysticks/temp_diagram.png" # Replace with the actual path to your file

def save(local_file_path):
# Read the local file
    try:
        with open(local_file_path, "rb") as file:
            file_data = file.read()
    
    # Open a dialog box for file saving
        Tk().withdraw()  # Hides the root window
        save_path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Image As"
        )
    
        if save_path:
            with open(save_path, "wb") as file:
                file.write(file_data)
            print(f"Image successfully saved to {save_path}.")
        else:
            print("Save operation canceled by the user.")
    except FileNotFoundError:
        print("The specified file was not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

save(path)