import os
import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

# Configuration
STORE_URL = "https://dankley-queensqr.vercel.app"
FIDI_URL = "https://dankley-queensqr.vercel.app/fidi"
EVENTS_URL = "https://dankley-queensqr.vercel.app/events"
CONSULTATION_URL = "https://dankley-queensqr.vercel.app/consultation"
DIRECTIONS_URL = "https://dankley-queensqr.vercel.app/directions"

# Brand Colors & Logos
CREAM_COLOR = "#fcf3da"

COLORS = {
    "Dark_Green": {
        "back_color": "#2c4d43", # Dark Green background
        "fill_color": CREAM_COLOR, # Cream pixels
        "logo_file": "logo_terracotta.png", # Original mask source
        "d_color": "#cd6b48" # Terracotta D
    },
    "Terracotta": {
        "back_color": "#cd6b48", # Terracotta background
        "fill_color": CREAM_COLOR, # Cream pixels
        "logo_file": "logo_dark_green.png", # Original mask source
        "d_color": "#2c4d43" # Dark Green D
    }
}

OUTPUT_DIRS = {
    "events": "qr assets/queens_events",
    "store": "qr assets/queens_store",
    "fidi": "qr assets/fidi_store",
    "consultation": "qr assets/queens_consultation",
    "directions": "qr assets/queens_directions"
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr(url, filename, fill_color, back_color, logo_file, d_color):
    """Generates a high-res QR code with correct colors and an embedded logo on a solid cream circle."""
    qr = qrcode.QRCode(
        version=4, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=30,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate QR code image with specified colors and rounded styling
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=hex_to_rgb(back_color), 
            front_color=hex_to_rgb(fill_color)
        )
    ).convert("RGBA")
    img = img.resize((1290, 1290), Image.Resampling.NEAREST)

    if os.path.exists(logo_file):
        logo = Image.open(logo_file).convert("RGBA")
        logo_size = int(1290 * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Create an alpha mask of the 'D' shape from the logo
        gray = logo.convert("L")
        d_mask = gray.point(lambda p: 0 if p < 150 else (255 if p > 220 else int((p - 150) * (255.0 / 70.0))))
        
        # 1. Create a pure circular alpha mask for the background circle
        circle_mask = Image.new("L", (logo_size, logo_size), 0)
        draw = ImageDraw.Draw(circle_mask)
        draw.ellipse((0, 0, logo_size, logo_size), fill=255)
        
        # 2. Create a solid Cream square image
        cream_bg = Image.new("RGBA", (logo_size, logo_size), hex_to_rgb(CREAM_COLOR) + (255,))
        
        # 3. Paste the solid Cream circle onto the QR code
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(cream_bg, pos, mask=circle_mask)
        
        # 4. Create a solid square image using the exact color intended for the 'D' 
        d_color_bg = Image.new("RGBA", (logo_size, logo_size), hex_to_rgb(d_color) + (255,))
        
        # 5. Paste the solid colored 'D' onto the QR code exactly over the cream circle
        img.paste(d_color_bg, pos, mask=d_mask)

    img.save(filename, "PNG")
    print(f"Generated Inverted Color QR: {filename}")

def main():
    print("Initializing Dankley Premium QR Code Generator...")

    for d in OUTPUT_DIRS.values():
        os.makedirs(d, exist_ok=True)

    print("\n--- Generating Store QR Codes ---")
    for color_name, palette in COLORS.items():
        filename = os.path.join(OUTPUT_DIRS["store"], f"QUEENS_STORE_QR_{color_name}.png")
        generate_qr(STORE_URL, filename, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])

    print("\n--- Generating FiDi Store QR Codes ---")
    for color_name, palette in COLORS.items():
        filename = os.path.join(OUTPUT_DIRS["fidi"], f"FIDI_STORE_QR_{color_name}.png")
        generate_qr(FIDI_URL, filename, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])

    print("\n--- Generating Events QR Codes ---")
    for color_name, palette in COLORS.items():
        filename = os.path.join(OUTPUT_DIRS["events"], f"QUEENS_EVENTS_QR_{color_name}.png")
        generate_qr(EVENTS_URL, filename, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])

    print("\n--- Generating Consultation QR Codes ---")
    for color_name, palette in COLORS.items():
        filename = os.path.join(OUTPUT_DIRS["consultation"], f"QUEENS_CONSULTATION_QR_{color_name}.png")
        generate_qr(CONSULTATION_URL, filename, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])

    print("\n--- Generating Directions QR Codes ---")
    for color_name, palette in COLORS.items():
        filename = os.path.join(OUTPUT_DIRS["directions"], f"QUEENS_DIRECTIONS_QR_{color_name}.png")
        generate_qr(DIRECTIONS_URL, filename, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])

    print("\nAll premium QR codes successfully generated in the 'qr assets' folder!")

if __name__ == "__main__":
    main()
