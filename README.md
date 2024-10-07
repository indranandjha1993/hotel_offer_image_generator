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
- CLI interface for easy command-line usage
- RESTful API for integration with other applications
- Dockerized setup for easy deployment and scaling

## Prerequisites

- Docker and Docker Compose
- OpenAI API key

## Installation and Setup

1. Clone this repository:
   ```
   git clone https://github.com/indranandjha1993/hotel-offer-image-generator.git
   cd hotel-offer-image-generator
   ```

2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

This will start two services:

- `web`: Runs the FastAPI application, accessible at `http://localhost:8000`
- `cli`: A service that you can use to run CLI commands

## Usage

### Using the CLI

To use the CLI within the Docker container, run:

```
docker-compose exec cli python /app/run_cli.py
```

Follow the prompts to generate hotel offer images.

### Using the API

The API will be available at `http://localhost:8000`. You can use tools like curl, Postman, or create a front-end
application to interact with the API.

Example API endpoints:

- `POST /generate-offer`: Generate a hotel offer image
- `GET /images/{image_name}`: Retrieve a generated image
- `GET /fonts`: List available fonts
- `POST /upload-font`: Upload a new font

For detailed API documentation, visit `http://localhost:8000/docs` in your browser.

## Available Options

- Text Positions: top-left, top-right, bottom-left, bottom-right, center-middle, center-bottom, center-top, center-left,
  center-right
- Text Colors: white, black, red, green, blue, yellow
- Background Colors: white, black, red, green, blue, yellow
- Font Sizes: 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72

## Customization

- To add more fonts, place TTF files in the `fonts` folder
- To add more colors, update the `TEXT_COLORS` and `BACKGROUND_COLORS` dictionaries in the configuration
- To change available font sizes, modify the `FONT_SIZES` list in the configuration

## Development

To make changes to the project:

1. Modify the code as needed
2. Rebuild the Docker images: `docker-compose build`
3. Restart the services: `docker-compose up`

## Acknowledgments

- OpenAI for GPT-4 and DALL-E 3
- Pillow library for image processing
- FastAPI for the REST API framework
- Docker for containerization

## Disclaimer

This tool uses AI-generated content. Please review and verify all generated text and images before using them in any
official capacity.