import ollama
import requests
import sys

def process_image_with_prompt(image_url: str, prompt: str):
    """
    Downloads an image from a URL, sends it to the Ollama VLM with a prompt,
    and prints the response.
    """
    model_name = "qwen2.5vl:3b"

    try:
        # Download the image from the URL
        print(f"Downloading image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        image_bytes = response.content
        print("Image downloaded successfully.")

        # Call the Ollama API with the image and prompt using generate
        print(f"Sending prompt to {model_name}...")
        generate_response = ollama.generate(
            model=model_name,
            prompt=prompt,
            images=[image_bytes],
        )

        # Print the response from the model
        print("\n--- Model Response ---")
        if 'response' in generate_response:
            print(generate_response['response'])
        else:
            print("No content in response.")
            print("Full response:", generate_response)
        print("--------------------")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # python vlm_test.py <image_url> <prompt>
    # If no arguments are provided, use default values.

    # A default image URL and prompt for demonstration
    default_image_url = "https://images.pexels.com/photos/32963802/pexels-photo-32963802.jpeg"
    default_prompt = "What is this a picture of?"

    if len(sys.argv) == 3:
        image_url = sys.argv[1]
        prompt = sys.argv[2]
    elif len(sys.argv) == 1:
        print("Using default image URL and prompt.")
        image_url = default_image_url
        prompt = default_prompt
    else:
        print("Usage: python vlm_test.py <image_url> \"<prompt>\"")
        sys.exit(1)

    process_image_with_prompt(image_url, prompt)