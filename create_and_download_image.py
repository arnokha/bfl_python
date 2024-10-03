## API REF: https://docs.bfl.ml/
import os
import requests
import time
import argparse
import sys
import json

API_VERSION = "v1"
ALLOWED_MODELS = ["flux-pro-1.1", "flux-pro", "flux-dev"]

# ==========================
# Configuration Defaults
# ==========================
# You can modify these default values as needed.
DEFAULT_PROMPT = "A cat on its back legs running like a human is holding a big silver fish with its arms. The cat is running away from the shop owner and has a panicked look on his face. The scene is situated in a crowded market."
DEFAULT_IMG_WIDTH = 1024
DEFAULT_IMG_HEIGHT = 768
DEFAULT_OUTPUT_FILENAME = "sample_out.jpg"
DEFAULT_MODEL = "flux-pro-1.1"

# Optionally, you can set the API key here.
# WARNING: Embedding API keys directly in scripts is not recommended for shared or public code.
# It's safer to set them as environment variables.
DEFAULT_BFL_API_KEY = ""  # e.g., "3xjdsiuvere-ddsf-..."

# ==========================
# Helper Functions
# ==========================
def round_to_nearest_32(n):
    return round(n / 32) * 32

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an image using Black Forest Labs API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--prompt',
        type=str,
        default=DEFAULT_PROMPT,
        help='Prompt for image generation.'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=DEFAULT_IMG_WIDTH,
        help='Width of the image in pixels. Must be between 256 and 1440 and divisible by 32.'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=DEFAULT_IMG_HEIGHT,
        help='Height of the image in pixels. Must be between 256 and 1440 and divisible by 32.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=DEFAULT_OUTPUT_FILENAME,
        help='Filename to save the resulting image.'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=DEFAULT_BFL_API_KEY,
        help='Black Forest Labs API key. If not provided, the script will look for the BFL_API_KEY environment variable.'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=DEFAULT_MODEL,
        choices=ALLOWED_MODELS,
        help='Model to use for image generation.'
    )
    
    # Optional Arguments
    parser.add_argument(
        '--prompt-upsampling',
        action='store_true',
        default=False,
        help='Whether to perform upsampling on the prompt. If active, automatically modifies the prompt for more creative generation.'
    ) # note: gave a 500 error when i tried this
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Optional seed for reproducibility.'
    )
    parser.add_argument(
        '--safety-tolerance',
        type=int,
        choices=range(0, 7),
        default=None,
        metavar='[0-6]',
        help='Tolerance level for input and output moderation. Between 0 and 6, 0 being most strict, 6 being least strict.'
    )
    
    args = parser.parse_args()
    
    # Validate and adjust width and height
    original_width, original_height = args.width, args.height
    args.width = max(256, min(1440, args.width))
    args.height = max(256, min(1440, args.height))
    
    # Round width and height to nearest multiple of 32
    args.width = round_to_nearest_32(args.width)
    args.height = round_to_nearest_32(args.height)
    
    # Print warning if dimensions were adjusted or rounded
    if args.width != original_width or args.height != original_height:
        print(f"Warning: Dimensions have been adjusted to fit within bounds and rounded to the nearest multiple of 32.")
        print(f"Original dimensions: {original_width}x{original_height}")
        print(f"Adjusted dimensions: {args.width}x{args.height}")
    
    return args


def get_api_key(provided_key):
    """
    Retrieves the API key from the provided argument or environment variable.
    """
    api_key = provided_key or os.environ.get("BFL_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please provide it via the '--api-key' argument or set the BFL_API_KEY environment variable."
        )
    return api_key


def make_request(api_key, prompt, width, height, model, 
                 prompt_upsampling=False, seed=None, safety_tolerance=None):
    url = f'https://api.bfl.ml/{API_VERSION}/{model}'
    headers = {
        'accept': 'application/json',
        'x-key': api_key,
        'Content-Type': 'application/json',
    }
    payload = {
        'prompt': prompt,
        'width': width,
        'height': height,
        'prompt_upsampling': prompt_upsampling,
        'seed': seed,
        'safety_tolerance': safety_tolerance
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error during API request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Response Content:", e.response.text)
        sys.exit(1)


def print_relevant_request_info(request):
    """
    Extracts and prints relevant information from the API response.
    """
    relevant_keys = ['id', 'status']
    filtered = {key: request.get(key) for key in relevant_keys if key in request}
    print("Request Details:")
    print(json.dumps(filtered, indent=4))


def poll_result(api_key, request_id):
    """
    Polls the API until the image generation is complete.
    Returns the image URL when ready.
    """
    url = 'https://api.bfl.ml/v1/get_result'
    headers = {
        'accept': 'application/json',
        'x-key': api_key,
    }
    params = {'id': request_id}

    print("Polling for result...")
    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as e:
            print(f"Error fetching result: {e}")
            sys.exit(1)

        status = result.get("status")
        if status == "Ready":
            sample = result.get('result', {}).get('sample')
            if sample:
                return sample
            else:
                print("Result is ready but no sample found.")
                sys.exit(1)
        else:
            print(f"Status: {status}")
            time.sleep(0.5)  # Wait before the next poll


def save_image(image_url, output_filename):
    """
    Downloads the image from the provided URL and saves it to a file.
    """
    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully saved to '{output_filename}'.")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error saving image to file: {e}")
        sys.exit(1)


# ==========================
# Main Execution Flow
# ==========================
def main():
    args = parse_args()
    
    try:
        api_key = get_api_key(args.api_key)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)

    print(f"Using model: {args.model}")
    print("Initiating image generation request...")
    request = make_request(
        api_key,
        args.prompt,
        args.width,
        args.height,
        args.model,
        prompt_upsampling=args.prompt_upsampling,
        seed=args.seed,
        safety_tolerance=args.safety_tolerance
    )
    print_relevant_request_info(request)

    request_id = request.get("id")
    if not request_id:
        print("Error: No request ID found in the response.")
        sys.exit(1)

    image_url = poll_result(api_key, request_id)
    print(f"Image is ready. Downloading from: {image_url}")

    save_image(image_url, args.output)


if __name__ == "__main__":
    main()