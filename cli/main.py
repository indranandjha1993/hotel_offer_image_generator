import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.table import Table

from configs.config import Config
from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator
from models import TextStyle
from services.image_processor import ImageProcessor
from services.offer_generator_service import OfferGeneratorService

console = Console()


def validate_word_limit(value):
    try:
        value = int(value)
        if 1 <= value <= 100:
            return value
        raise ValueError
    except ValueError:
        console.print("[bold red]Invalid word limit. Please enter a number between 1 and 100.[/bold red]")
        return None


def validate_opacity(value):
    try:
        value = float(value)
        if 0 <= value <= 1:
            return value
        raise ValueError
    except ValueError:
        console.print("[bold red]Invalid opacity. Please enter a number between 0 and 1.[/bold red]")
        return None


def prompt_with_choices(prompt, choices, default):
    table = Table(title=prompt)
    table.add_column("Option", style="cyan")
    table.add_column("Value", style="magenta")

    for i, choice in enumerate(choices, 1):
        table.add_row(f"{i}", str(choice))

    console.print(table)

    while True:
        value = click.prompt(f"Enter your choice (default: {default})", default=default)
        if str(value) in [str(choice) for choice in choices]:
            return value
        try:
            index = int(value) - 1
            if 0 <= index < len(choices):
                return choices[index]
        except ValueError:
            pass
        console.print("[bold red]Invalid choice. Please try again.[/bold red]")


@click.command()
@click.option('--prompt', prompt='Enter the hotel offer prompt', default="Luxurious beach resort",
              help="Hotel offer prompt")
@click.option('--word-limit', prompt='Enter word limit', default=Config.DEFAULT_WORD_LIMIT,
              help="Word limit for the offer text (1-100)")
def generate_offer(prompt, word_limit):
    try:
        # Validate word limit
        while True:
            word_limit = validate_word_limit(word_limit)
            if word_limit is not None:
                break
            word_limit = click.prompt('Enter word limit', default=Config.DEFAULT_WORD_LIMIT)

        font = prompt_with_choices("Choose a font", os.listdir(Config.FONTS_FOLDER), Config.DEFAULT_FONT)
        font_size = int(prompt_with_choices("Choose font size", [str(size) for size in Config.FONT_SIZES],
                                            str(Config.DEFAULT_FONT_SIZE)))
        position = prompt_with_choices("Choose text position", list(Config.TEXT_POSITIONS.keys()),
                                       Config.DEFAULT_TEXT_POSITION)
        text_color = prompt_with_choices("Choose text color", list(Config.TEXT_COLORS.keys()),
                                         Config.DEFAULT_TEXT_COLOR)
        bg_color = prompt_with_choices("Choose background color", list(Config.BACKGROUND_COLORS.keys()),
                                       Config.DEFAULT_BG_COLOR)

        # Validate opacity
        while True:
            bg_opacity = validate_opacity(
                prompt_with_choices("Choose background opacity", [f"{i / 10:.1f}" for i in range(11)],
                                    str(Config.DEFAULT_BG_OPACITY)))
            if bg_opacity is not None:
                break

        style = TextStyle(
            font_name=font,
            font_size=font_size,
            position=position,
            text_color=Config.TEXT_COLORS[text_color],
            bg_color=Config.BACKGROUND_COLORS[bg_color],
            bg_opacity=bg_opacity
        )

        with console.status("[bold green]Initializing services...") as status:
            text_generator = TextGenerator(service_name=Config.AI_SERVICE)
            image_generator = ImageGenerator(service_name=Config.AI_SERVICE)
            image_processor = ImageProcessor()
            service = OfferGeneratorService(text_generator, image_generator, image_processor)
            status.update("[bold green]Services initialized!")

        with console.status("[bold green]Initializing services...") as status:
            text_generator = TextGenerator(service_name=Config.AI_SERVICE)
            image_generator = ImageGenerator(service_name=Config.AI_SERVICE)
            image_processor = ImageProcessor()
            service = OfferGeneratorService(text_generator, image_generator, image_processor)
            status.update("[bold green]Services initialized!")

        with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                console=console
        ) as progress:
            text_task = progress.add_task("[red]Generating offer text...", total=None)
            image_task = progress.add_task("[green]Generating initial image...", total=None)
            overlay_task = progress.add_task("[blue]Applying text overlay...", total=None)

            def update_text_progress(value):
                if value == 100:
                    progress.update(text_task, completed=100, total=100)

            def update_image_progress(value):
                if value == 100:
                    progress.update(image_task, completed=100, total=100)

            def update_overlay_progress(value):
                if value == 100:
                    progress.update(overlay_task, completed=100, total=100)

            offer_text, initial_image, final_image = service.generate_offer(
                prompt, word_limit, style,
                text_progress=update_text_progress,
                image_progress=update_image_progress,
                overlay_progress=update_overlay_progress
            )

        console.print(Panel(f"[bold cyan]Generated offer text:[/bold cyan] {offer_text}", expand=False))

        filename = image_processor.get_timestamp_filename(offer_text.lower().strip().replace(" ", "_"))

        initial_image_name = f"{filename}_initial.jpg"
        image_processor.save_image(initial_image, initial_image_name)
        console.print(f"[green]Base image saved as:[/green] {initial_image_name}")

        final_image_name = f"{filename}_final.jpg"
        image_processor.save_image(final_image, final_image_name)
        console.print(f"[green]Final image saved as:[/green] {final_image_name}")

    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
