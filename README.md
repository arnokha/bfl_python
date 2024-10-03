# Black Forest Labs Flux Image Generator

A quickstart guide to generate images using Black Forest Labs' Flux image generation models with the `create_and_download_image.py` script.

## Prerequisites

- **Python 3.6 or higher**
- **`requests` library**

  Install via pip:

  ```bash
  pip install requests
  ```

## Setup

1. **Download the Script**

   Ensure you have the `create_and_download_image.py` file in your working directory.

2. **Obtain an API Key**

   - Sign up or log in to [Black Forest Labs](https://www.bfl.ml/) to obtain your API key.
   - **Security Tip:** It's recommended to set your API key as an environment variable to avoid exposing it in scripts.

     ```bash
     export BFL_API_KEY="your_api_key_here"
     ```

## Usage

Run the script using Python with the desired options:

```bash
python create_and_download_image.py [OPTIONS]
```

**Note**: you can also just leave these options blank and edit the default values in the script if you'd prefer.

### Available Options

- `--prompt`  
  *Type:* String  
  *Default:*  
  `"A cat on its back legs running like a human is holding a big silver fish with its arms. The cat is running away from the shop owner and has a panicked look on his face. The scene is situated in a crowded market."`  
  *Description:* Prompt for image generation.

- `--width`  
  *Type:* Integer  
  *Default:* `1024`  
  *Description:* Width of the image in pixels. Must be between **256** and **1440** and divisible by **32**.

- `--height`  
  *Type:* Integer  
  *Default:* `768`  
  *Description:* Height of the image in pixels. Must be between **256** and **1440** and divisible by **32**.

- `--output`  
  *Type:* String  
  *Default:* `sample_out.jpg`  
  *Description:* Filename to save the resulting image.

- `--api-key`  
  *Type:* String  
  *Default:*  
  *(If not provided, the script will use the `BFL_API_KEY` environment variable.)*  
  *Description:* Black Forest Labs API key.

- `--model`  
  *Type:* String  
  *Choices:* `flux-pro-1.1`, `flux-pro`, `flux-dev`  
  *Default:* `flux-pro-1.1`  
  *Description:* Model to use for image generation.

### Optional Arguments

- `--prompt-upsampling`  
  *Type:* Boolean Flag  
  *Default:* `False`  
  *Description:* Enable prompt upsampling for more creative image generation.

- `--seed`  
  *Type:* Integer  
  *Default:* `None`  
  *Description:* Optional seed for reproducibility.

- `--safety-tolerance`  
  *Type:* Integer (0-6)  
  *Default:* `None`  
  *Description:* Tolerance level for input and output moderation. **0** is most strict, **6** is least strict.

## Examples

1. **Basic Image Generation with Defaults:**

   ```bash
   python create_and_download_image.py
   ```

2. **Custom Prompt and Dimensions:**

   ```bash
   python create_and_download_image.py --prompt "A serene beach at sunset" --width 512 --height 512
   ```

3. **Enable Prompt Upsampling and Set Seed:**

   ```bash
   python create_and_download_image.py --prompt-upsampling --seed 42
   ```

4. **Adjust Safety Tolerance:**

   ```bash
   python create_and_download_image.py --safety-tolerance 3
   ```

5. **Specify API Key Directly:**

   ```bash
   python create_and_download_image.py --api-key your_api_key_here
   ```

## Notes

- **Environment Variable for API Key:**

  Instead of passing the API key every time, set it as an environment variable:

  ```bash
  export BFL_API_KEY="your_api_key_here"
  ```

- **Handling Errors:**

  - If you encounter a **500 Internal Server Error** when using `--prompt-upsampling`, it might be due to server-side issues. Try running the script without this option.
  - Note that this API is in beta and subject to change. Refer to [the docs](https://docs.bfl.ml/) for latest changes.
  
## License

This project is licensed under the [MIT License](LICENSE).

---

**Happy Image Generating!**