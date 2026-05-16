from rembg import remove, new_session
import gradio as gr
from PIL import Image

# =========================
# LOAD AI MODEL
# =========================
session = new_session("isnet-general-use")


# =========================
# COLOR BACKGROUND CREATOR
# =========================
def create_background(bg_type, size):

    colors = {

        # WHITE / BLACK
        "No Background": None,
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
        "Wine Red": (114, 47, 55, 255),

        # PINK
        "Light Pink": (255, 182, 193, 255),
        "Pink": (255, 105, 180, 255),
        "Dark Pink": (199, 21, 133, 255),
        "Rose Pink": (255, 102, 204, 255),

        # BLUE
        "Sky Blue": (135, 206, 235, 255),
        "Light Blue": (173, 216, 230, 255),
        "Blue": (0, 102, 255, 255),
        "Dark Blue": (0, 0, 139, 255),
        "Navy Blue": (0, 0, 128, 255),
        "Cyan": (0, 255, 255, 255),

        # GREEN
        "Mint Green": (152, 255, 152, 255),
        "Light Green": (144, 238, 144, 255),
        "Green": (0, 200, 0, 255),
        "Dark Green": (0, 100, 0, 255),
        "Olive Green": (85, 107, 47, 255),

        # YELLOW / ORANGE
        "Yellow": (255, 255, 0, 255),
        "Golden Yellow": (255, 215, 0, 255),
        "Orange": (255, 165, 0, 255),
        "Dark Orange": (255, 140, 0, 255),

        # PURPLE
        "Lavender": (230, 230, 250, 255),
        "Purple": (128, 0, 128, 255),
        "Dark Purple": (75, 0, 130, 255),
        "Violet": (148, 0, 211, 255),

        # BROWN
        "Light Brown": (181, 101, 29, 255),
        "Brown": (139, 69, 19, 255),
        "Dark Brown": (92, 64, 51, 255),

        # SPECIAL
        "Beige": (245, 245, 220, 255),
        "Peach": (255, 218, 185, 255),
        "Coral": (255, 127, 80, 255),
        "Turquoise": (64, 224, 208, 255),

    }

    # Transparent Output
    if bg_type == "No Background":
        return None

    color = colors.get(bg_type, (255, 255, 255, 255))

    return Image.new("RGBA", size, color)


# =========================
# MAIN AI FUNCTION
# =========================
def process_image(image, bg_type):

    # Remove Background
    output = remove(image, session=session)

    # Transparent output
    if bg_type == "No Background":
        return output

    # Create selected color background
    bg = create_background(bg_type, output.size)

    # Paste cutout onto background
    bg.paste(output, (0, 0), output)

    return bg


# =========================
# GRADIO UI
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
                "Wine Red",

                "Light Pink",
                "Pink",
                "Dark Pink",
                "Rose Pink",

                "Sky Blue",
                "Light Blue",
                "Blue",
                "Dark Blue",
                "Navy Blue",
                "Cyan",

                "Mint Green",
                "Light Green",
                "Green",
                "Dark Green",
                "Olive Green",

                "Yellow",
                "Golden Yellow",
                "Orange",
                "Dark Orange",

                "Lavender",
                "Purple",
                "Dark Purple",
                "Violet",

                "Light Brown",
                "Brown",
                "Dark Brown",

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
        label="AI Generated Output"
    ),

    title="✨ AI Background Studio",

    description="""
Upload your image and generate professional AI background edits instantly.
Perfect for ecommerce, Instagram, brands, and creators.
""",

    submit_btn="✨ Generate",

    clear_btn="🗑 Clear",

    flagging_mode="never"
)

# =========================
# LAUNCH APP
# =========================
demo.launch()