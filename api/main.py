import os
from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from configs.config import Config
from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator
from models import TextStyle
from services.image_processor import ImageProcessor
from services.offer_generator_service import OfferGeneratorService

app = FastAPI()

# Initialize services
text_generator = TextGenerator(service_name=Config.AI_SERVICE)
image_generator = ImageGenerator(service_name=Config.AI_SERVICE)
image_processor = ImageProcessor()
offer_service = OfferGeneratorService(text_generator, image_generator, image_processor)


class OfferRequest(BaseModel):
    prompt: str
    word_limit: int = Config.DEFAULT_WORD_LIMIT
    font_name: str = Config.DEFAULT_FONT
    font_size: int = Config.DEFAULT_FONT_SIZE
    position: str = Config.DEFAULT_TEXT_POSITION
    text_color: str = Config.DEFAULT_TEXT_COLOR
    bg_color: str = Config.DEFAULT_BG_COLOR
    bg_opacity: float = Config.DEFAULT_BG_OPACITY


class OfferResponse(BaseModel):
    offer_text: str
    initial_image_url: str
    final_image_url: str


@app.post("/generate-offer", response_model=OfferResponse)
async def generate_offer(offer_request: OfferRequest):
    try:
        style = TextStyle(
            font_name=offer_request.font_name,
            font_size=offer_request.font_size,
            position=offer_request.position,
            text_color=Config.TEXT_COLORS[offer_request.text_color],
            bg_color=Config.BACKGROUND_COLORS[offer_request.bg_color],
            bg_opacity=offer_request.bg_opacity
        )

        offer_text, initial_image, final_image = offer_service.generate_offer(
            offer_request.prompt, offer_request.word_limit, style
        )

        # Save images
        initial_image_filename = image_processor.get_timestamp_filename(f"{offer_text[:20]}_initial.jpg")
        final_image_filename = image_processor.get_timestamp_filename(f"{offer_text[:20]}_final.jpg")

        initial_image_path = os.path.join(Config.IMAGES_FOLDER, initial_image_filename)
        final_image_path = os.path.join(Config.IMAGES_FOLDER, final_image_filename)

        image_processor.save_image(initial_image, initial_image_path)
        image_processor.save_image(final_image, final_image_path)

        return OfferResponse(
            offer_text=offer_text,
            initial_image_url=f"/images/{initial_image_filename}",
            final_image_url=f"/images/{final_image_filename}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(Config.IMAGES_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


@app.get("/fonts", response_model=List[str])
async def list_fonts():
    return os.listdir(Config.FONTS_FOLDER)


@app.post("/upload-font")
async def upload_font(font: UploadFile = File(...)):
    try:
        font_path = os.path.join(Config.FONTS_FOLDER, font.filename)
        with open(font_path, "wb") as buffer:
            buffer.write(await font.read())
        return {"message": f"Font {font.filename} uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
