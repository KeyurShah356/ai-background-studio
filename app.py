from rembg import remove, new_session
import gradio as gr

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)

# =========================
# LOAD AI MODEL
# =========================
session = new_session("isnet-general-use")

# =========================
# COLOR BACKGROUND CREATOR
# =========================
def create_background(bg_type, size):

    colors = {

        # TRANSPARENT
        "No Background": None,

        # WHITE / GREY / BLACK
        "White": (255, 255, 255, 255),
        "Off White": (245, 245, 245, 255),
        "Cream": (255, 253, 208, 255),

        "Light Grey": (220, 220, 220, 255),
        "Grey": (180, 180, 180, 255),
        "Dark Grey": (80, 80, 80, 255),

        "Black": (0, 0, 0, 255),
        "Matte Black": (20, 20, 20, 255),

        # RED
        "Light Red": (255, 102, 102, 255),
        "Red": (255, 0, 0, 255),
        "Dark Red": (139, 0, 0, 255),

        # PINK
        "Light Pink": (255, 182, 193, 255),
        "Pink": (255, 105, 180, 255),
        "Dark Pink": (199, 21, 133, 255),

        # BLUE
        "Sky Blue": (135, 206, 235, 255),
        "Light Blue": (173, 216, 230, 255),
        "Blue": (0, 102, 255, 255),
        "Dark Blue": (0, 0, 139, 255),

        # GREEN
        "Mint Green": (152, 255, 152, 255),
        "Light Green": (144, 238, 144, 255),
        "Green": (0, 200, 0, 255),
        "Dark Green": (0, 100, 0, 255),

        # YELLOW / ORANGE
        "Yellow": (255, 255, 0, 255),
        "Golden Yellow": (255, 215, 0, 255),
        "Orange": (255, 165, 0, 255),

        # PURPLE
        "Lavender": (230, 230, 250, 255),
        "Purple": (128, 0, 128, 255),

        # SPECIAL
        "Beige": (245, 245, 220, 255),
        "Peach": (255, 218, 185, 255),
        "Coral": (255, 127, 80, 255),
        "Turquoise": (64, 224, 208, 255),
    }

    if bg_type == "No Background":
        return None

    color = colors.get(
        bg_type,
        (255, 255, 255, 255)
    )

    return Image.new(
        "RGBA",
        size,
        color
    )

# =========================
# IMAGE ENHANCEMENT
# =========================
def enhance_image(image):

    # Sharpen
    image = image.filter(
        ImageFilter.SHARPEN
    )

    # Sharpness
    sharpness = ImageEnhance.Sharpness(image)

    image = sharpness.enhance(2.5)

    # Contrast
    contrast = ImageEnhance.Contrast(image)

    image = contrast.enhance(1.2)

    # Color
    color = ImageEnhance.Color(image)

    image = color.enhance(1.1)

    return image

# =========================
# MAIN AI FUNCTION
# =========================
def process_image(image, bg_type):

    # Remove background
    output = remove(
        image,
        session=session
    )

    # Enhance quality
    output = enhance_image(output)

    # Transparent output
    if bg_type == "No Background":
        return output

    # Create background
    bg = create_background(
        bg_type,
        output.size
    )

    # Paste subject
    bg.paste(
        output,
        (0, 0),
        output
    )

    return bg

# =========================
# UI
# =========================
demo = gr.Interface(

    fn=process_image,

    inputs=[

        gr.Image(
            type="pil",
            label="Upload Your Image"
        ),

        gr.Dropdown(

            [

                "No Background",

                "White",
                "Off White",
                "Cream",

                "Light Grey",
                "Grey",
                "Dark Grey",

                "Black",
                "Matte Black",

                "Light Red",
                "Red",
                "Dark Red",

                "Light Pink",
                "Pink",
                "Dark Pink",

                "Sky Blue",
                "Light Blue",
                "Blue",
                "Dark Blue",

                "Mint Green",
                "Light Green",
                "Green",
                "Dark Green",

                "Yellow",
                "Golden Yellow",
                "Orange",

                "Lavender",
                "Purple",

                "Beige",
                "Peach",
                "Coral",
                "Turquoise"

            ],

            value="No Background",

            label="Choose Background Color"
        )
    ],

    outputs=gr.Image(
        type="pil",
        label="Enhanced AI Output"
    ),

    title="✨ AI Background Remover",

    description="""
Professional AI background remover with enhanced HD quality.
Create stunning transparent edits instantly.
""",

    submit_btn="✨ Generate",

    clear_btn="🗑 Clear",

    flagging_mode="never"
)

# =========================
# LAUNCH
# =========================
demo.launch()