import requests
from textblob import TextBlob

# Hugging Face API credentials
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Summarization model
API_TOKEN = "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"

# Function to simplify and enhance the input
def simplify_prompt(user_input):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "inputs": user_input,
        "parameters": {
            "max_length": 100,  # Set max length for the simplified output
            "min_length": 20,   # Minimum length to ensure useful output
            "do_sample": False  # Deterministic output
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["summary_text"]  # Simplified or enhanced text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to correct spelling errors
def correct_spelling(text):
    corrected_text = TextBlob(text).correct()
    return str(corrected_text)

# Interactive prompt for user input
if __name__ == "__main__":
    print("Enter text to simplify, enhance, and correct spelling. Type 'exit' to quit.")

    while True:
        user_text = input("\nYour Input: ").strip()  # Strip extra spaces
        if not user_text:
            print("Error: Input cannot be empty. Please enter valid text.")
            continue  # Skip empty input

        if user_text.lower() == "exit":
            print("Exiting... Goodbye!")
            break

        try:
            # Correct spelling errors
            corrected_text = correct_spelling(user_text)
            print("\nCorrected Text:")
            print(corrected_text)

            # Simplify and enhance the corrected text
            simplified_text = simplify_prompt(corrected_text)
            print("\nSimplified & Enhanced Text:")
            print(simplified_text)
        except Exception as e:
            print(f"An error occurred: {e}")
