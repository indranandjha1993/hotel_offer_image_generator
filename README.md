# Hotel Offer Image Generator

This project is an AI-powered tool that generates custom hotel offer images with overlaid text. It uses OpenAI's GPT-4
for text generation and DALL-E 3 for image creation, allowing users to quickly produce professional-looking promotional
images for hotels.

## Features

- Generate custom hotel offer text using GPT-4
- Create high-quality promotional images with DALL-E 3
- Customize text overlay with various options:
    - Font selection
    - Font size
    - Text color
    - Text position (9 different positions available)
    - Background color and opacity for text
- Test text positioning without generating new images
- Save both raw generated images and final images with text overlay

## Prerequisites

- Python 3.12+
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/hotel-offer-image-generator.git
   cd hotel-offer-image-generator
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Create `fonts` and `images` folders in the project directory:
   ```
   mkdir fonts images
   ```

5. Add some TTF font files to the `fonts` folder.

## Usage

Run the script:

```
python main.py
```

Follow the prompts to:

1. Choose whether to test text positions or generate an offer image
2. Enter a hotel offer prompt
3. Specify the word limit for the offer text
4. Select font, font size, text position, colors, and opacity

The script will generate and save:

- A raw image based on your prompt (as `generated_image.png`)
- A final image with text overlay (as `final_offer_image.png`)

### Testing Text Positions

If you choose to test text positions:

1. The script will generate test images for all available text positions
2. Images will be saved in the `images` folder as `test_position_[position].png`

## Available Options

- Text Positions: top-left, top-right, bottom-left, bottom-right, center-middle, center-bottom, center-top, center-left,
  center-right
- Text Colors: white, black, red, green, blue, yellow
- Background Colors: white, black, red, green, blue, yellow
- Font Sizes: 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72

## Customization

- To add more fonts, place TTF files in the `fonts` folder
- To add more colors, update the `TEXT_COLORS` and `BACKGROUND_COLORS` dictionaries in the script
- To change available font sizes, modify the `FONT_SIZES` list

## Acknowledgments

- OpenAI for GPT-4 and DALL-E 3
- Pillow library for image processing

## Disclaimer

This tool uses AI-generated content. Please review and verify all generated text and images before using them in any
official capacity.
