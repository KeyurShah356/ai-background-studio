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
# CUSTOM DARK CSS
# =========================
custom_css = """

body {
    background: #000000 !important;
}

.gradio-container {
    background: #000000 !important;
    color: white !important;
}

footer {
    display: none !important;
}

.dark {
    background: #000000 !important;
}

input, textarea, select {
    background: #1a1a1a !important;
    color: white !important;
    border: 1px solid #333 !important;
}

button {
    background: #ff6600 !important;
    color: white !important;
    border: none !important;
}

button:hover {
    background: #ff7b1a !important;
}

.block {
    background: #111111 !important;
    border: 1px solid #333 !important;
    border-radius: 14px !important;
}

"""

# =========================
# COLOR BACKGROUND CREATOR
# =========================
def create_background(bg_type, size):

    colors = {

        "No Background": None,

        "White": (255, 255, 255, 255),
        "Off White": (245, 245, 245, 255),
        "Cream": (255, 253, 208, 255),

        "Light Grey": (220, 220, 220, 255),
        "Grey": (180, 180, 180, 255),
        "Dark Grey": (80, 80, 80, 255),

        "Black": (0, 0, 0, 255),
        "Matte Black": (20, 20, 20, 255),

        "Light Red": (255, 102, 102, 255),
        "Red": (255, 0, 0, 255),

        "Light Pink": (255, 182, 193, 255),
        "Pink": (255, 105, 180, 255),

        "Sky Blue": (135, 206, 235, 255),
        "Blue": (0, 102, 255, 255),

        "Mint Green": (152, 255, 152, 255),
        "Green": (0, 200, 0, 255),

        "Yellow": (255, 255, 0, 255),
        "Orange": (255, 165, 0, 255),

        "Lavender": (230, 230, 250, 255),
        "Purple": (128, 0, 128, 255),

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

    # Remove Background
    output = remove(
        image,
        session=session
    )

    # Enhance Quality
    output = enhance_image(output)

    # Transparent Output
    if bg_type == "No Background":
        return output

    # Create Background
    bg = create_background(
        bg_type,
        output.size
    )

    # Paste Subject
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

                "Light Pink",
                "Pink",

                "Sky Blue",
                "Blue",

                "Mint Green",
                "Green",

                "Yellow",
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

    title="✨ AI Background Studio",

    description="""
Professional AI background remover with enhanced HD quality.
Create stunning transparent edits instantly.
""",

    submit_btn="✨ Generate",

    clear_btn="🗑 Clear",

    flagging_mode="never",

    css=custom_css
)

# =========================
# LAUNCH
# =========================
demo.launch()