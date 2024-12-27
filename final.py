import requests
import google.generativeai as genai
from textblob import TextBlob
from dotenv import load_dotenv
import os
import together
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

load_dotenv()   

API_URL_HUGGING_FACE = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Summarization model
API_KEY_HUGGING_FACE = os.getenv("API_KEY_HUGGING_FACE")  # Get token from the .env file
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
API_KEY_TOGETHER = os.getenv("API_KEY_TOGETHER")


# Function to simplify and enhance the input
def simplify_prompt(user_input):
    headers = {"Authorization": f"Bearer {API_KEY_HUGGING_FACE}"}
    payload = {
        "inputs": user_input,
        "parameters": {
            "max_length": 100,  # Set max length for the simplified output
            "min_length": 20,   # Minimum length to ensure useful output
            "do_sample": False  # Deterministic output
        }
    }

    response = requests.post(API_URL_HUGGING_FACE, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["summary_text"]  # Simplified or enhanced text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to correct spelling errors
def correct_spelling(text):
    corrected_text = TextBlob(text).correct()
    return str(corrected_text)

def response_from_gemini(text):

    genai.configure(api_key = API_KEY_GEMINI)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(text).text

    return response

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


def response_from_together(text):
    client = together.Together(api_key=API_KEY_TOGETHER)
    completion = client.chat.completions.create(model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", messages=[{"role": "user", "content": text}])
    return completion.choices[0].message.content

    
    
if __name__ == "__main__":
    user_text = "Give me a code of star pattern in cpp"
    user_text = user_text.strip()

    try:
        corrected_text = correct_spelling(user_text)
        simplified_text = simplify_prompt(corrected_text)
        response = response_from_gemini(simplified_text)

    
    
    except Exception as e:
        print(f"An error occurred: {e}")
