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

# Logo SVG Path Data (extracted from the master brand vector assets)
PATH1 = "M266.23,0C119.2,0,0,119.2,0,266.23s119.2,266.23,266.23,266.23,266.23-119.2,266.23-266.23S413.27,0,266.23,0ZM375.68,398.18c-54.78,47.67-134.3,59.52-198.52,23.26-28.01-15.82-49.84-50.26-53.01-82.09-.92-9.25,6.13-16.67,10.74-23.97,5.5-8.7,10.8-17.51,15.83-26.49,10.04-17.94,18.96-36.56,25.88-55.94,4.77-13.36,10.36-28.93,9.99-43.41-.23-8.69-7.7-10.21-15.87-7.27-9.31,3.36-18.94,5.66-28.8,5.89-16.07.36-32.98-5.6-42.53-18.52-5.97-8.08-8.68-18.5-7.4-28.46,2.47-19.2,19.02-33.61,37.85-35.79,7.83-.91,15.87.24,23.18,3.16,2.36.94,5.6,2.47,6.49,5.03.4,1.15.23,2.53-.59,3.42-2.34,2.51-6.7.64-9.43.06-1.61-.34-3.26-.52-4.91-.5-5.79.1-12.78,3.3-12.5,10,.11,2.7,1.48,5.34,3.67,6.93,3.45,2.49,8.54,2.62,12.63,2.17,4.01-.44,7.89-1.62,11.71-2.9,3.02-1.01,6.03-2.08,9.01-3.22,37.69-14.39,72.85-31.93,114.29-31.77,41.84.16,82.67,14.59,112.7,44.27,4.65,4.59,8.96,9.47,12.93,14.59,19.58,25.29,30.72,56.52,32.07,88.65,2.38,56.77-22.47,115.55-65.39,152.9Z"
PATH2 = "M335.38,163.72c-30.48-16.92-67.83-19.79-100.51-7.98-4.05,1.46-8.02,3.14-11.93,4.94l-5.99,2.85c-.07.03-.14.07-.21.1-.2.19-.8.42-1.22.6-.1.05-.2.1-.3.15-2.73,1.62-.57,4.94,1.63,4.09.02,0,3.4-.67,3.42-.67,27.51-3.27,33.53,17.58,25.23,38.97-12.2,30.3-24.78,60.36-37.65,90.39-6.56,15.3-14.98,32.19-11.47,49.36,11.94,58.3,93.43,45.89,129.16,21.42,39.3-26.92,63.17-81.23,58.47-128.71-3.05-30.83-21.22-60.3-48.64-75.52Z"

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
    """Generates a high-res QR code with correct colors and an embedded logo on a fading cream circle."""
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
        # Outer circle canvas size (45% of QR size)
        logo_size = int(1290 * 0.45)
        # D logo shape size (keeps readability at 35% of QR size)
        d_size = int(1290 * 0.35)
        
        logo = Image.open(logo_file).convert("RGBA")
        logo_resized = logo.resize((d_size, d_size), Image.Resampling.LANCZOS)
        
        # 1. Extract raw masks at d_size (35%)
        d_mask_raw = Image.new("L", (d_size, d_size), 0)
        for y in range(d_size):
            for x in range(d_size):
                r, g, b, a = logo_resized.getpixel((x, y))
                if a == 255 and (r > 240 and g > 230 and b > 200):
                    d_mask_raw.putpixel((x, y), 255)
                    
        not_cream_mask_raw = Image.new("L", (d_size, d_size), 0)
        for y in range(d_size):
            for x in range(d_size):
                r, g, b, a = logo_resized.getpixel((x, y))
                if a == 0 or not (r > 240 and g > 230 and b > 200):
                    not_cream_mask_raw.putpixel((x, y), 255)
                    
        hollow_mask_raw = not_cream_mask_raw.copy()
        ImageDraw.floodfill(hollow_mask_raw, (0, 0), 0)
        
        # 2. Place these masks inside the larger logo_size (45%) canvas
        d_mask = Image.new("L", (logo_size, logo_size), 0)
        hollow_mask = Image.new("L", (logo_size, logo_size), 0)
        offset = (logo_size - d_size) // 2
        d_mask.paste(d_mask_raw, (offset, offset))
        hollow_mask.paste(hollow_mask_raw, (offset, offset))
        
        # 3. Create the radial gradient mask for the Cream background circle (fading at edges)
        gradient_mask = Image.new("L", (logo_size, logo_size), 0)
        cx, cy = logo_size / 2.0, logo_size / 2.0
        inner_r = logo_size * 0.14  # Solid interior core kept small for wider glow
        outer_r = logo_size * 0.5
        for y in range(logo_size):
            for x in range(logo_size):
                dx = x - cx
                dy = y - cy
                dist = (dx*dx + dy*dy) ** 0.5
                if dist <= inner_r:
                    val = 255
                elif dist >= outer_r:
                    val = 0
                else:
                    ratio = (dist - inner_r) / (outer_r - inner_r)
                    val = int(255 * (1.0 - ratio))
                gradient_mask.putpixel((x, y), val)
        
        # 4. Create solid Cream and D-color images
        cream_bg = Image.new("RGBA", (logo_size, logo_size), hex_to_rgb(CREAM_COLOR) + (255,))
        d_color_bg = Image.new("RGBA", (logo_size, logo_size), hex_to_rgb(d_color) + (255,))
        
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        
        # Layer 1: Paste Cream background with radial gradient mask
        img.paste(cream_bg, pos, mask=gradient_mask)
        
        # Layer 2: Paste Solid Cream in the hollow inside of the D
        img.paste(cream_bg, pos, mask=hollow_mask)
        
        # Layer 3: Paste D shape with d_mask
        img.paste(d_color_bg, pos, mask=d_mask)

    img.save(filename, "PNG")
    print(f"Generated Inverted Color QR: {filename}")

def is_eye(y, x, width, height):
    """Checks if a module coordinate is within one of the three corner finder patterns (eyes)."""
    return (
        (y < 7 and x < 7)
        or (y < 7 and width - x < 8)
        or (height - y < 8 and x < 7)
    )

def get_module_path(x, y, N, S, E, W, r=0.5):
    """Generates the SVG path for a single module with rounded corners merging with neighbors."""
    nw_rounded = not N and not W
    ne_rounded = not N and not E
    se_rounded = not S and not E
    sw_rounded = not S and not W

    path_parts = []
    # Start at top center of the module
    path_parts.append(f"M {x + 0.5:.4f} {y:.4f}")

    # Top-right corner (NE)
    if ne_rounded:
        path_parts.append(f"Q {x + 1:.4f} {y:.4f} {x + 1:.4f} {y + 0.5:.4f}")
    else:
        path_parts.append(f"L {x + 1:.4f} {y:.4f} L {x + 1:.4f} {y + 0.5:.4f}")

    # Bottom-right corner (SE)
    if se_rounded:
        path_parts.append(f"Q {x + 1:.4f} {y + 1:.4f} {x + 0.5:.4f} {y + 1:.4f}")
    else:
        path_parts.append(f"L {x + 1:.4f} {y + 1:.4f} L {x + 0.5:.4f} {y + 1:.4f}")

    # Bottom-left corner (SW)
    if sw_rounded:
        path_parts.append(f"Q {x:.4f} {y + 1:.4f} {x:.4f} {y + 0.5:.4f}")
    else:
        path_parts.append(f"L {x:.4f} {y + 1:.4f} L {x:.4f} {y + 0.5:.4f}")

    # Top-left corner (NW)
    if nw_rounded:
        path_parts.append(f"Q {x:.4f} {y:.4f} {x + 0.5:.4f} {y:.4f}")
    else:
        path_parts.append(f"L {x:.4f} {y:.4f} L {x + 0.5:.4f} {y:.4f}")

    path_parts.append("Z")
    return "".join(path_parts)

def generate_qr_svg(url, filename, fill_color, back_color, d_color):
    """Generates a high-res vector SVG QR code with correct colors and embedded vector logo."""
    # 1. Generate QR Code matrix
    qr = qrcode.QRCode(
        version=4, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    
    width = len(matrix)
    height = len(matrix[0])
    
    # 2. Build SVG XML
    svg_parts = []
    svg_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    
    # Background
    svg_parts.append(f'  <rect width="{width}" height="{height}" fill="{back_color}" />')
    
    # Defs (gradient & mask)
    svg_parts.append('  <defs>')
    svg_parts.append('    <radialGradient id="cream-fade" cx="50%" cy="50%" r="50%">')
    svg_parts.append('      <stop offset="0%" stop-color="#fcf3da" stop-opacity="1" />')
    svg_parts.append('      <stop offset="28%" stop-color="#fcf3da" stop-opacity="1" />')
    svg_parts.append('      <stop offset="100%" stop-color="#fcf3da" stop-opacity="0" />')
    svg_parts.append('    </radialGradient>')
    
    svg_parts.append('    <mask id="d-logo-mask">')
    svg_parts.append('      <circle cx="266.23" cy="266.23" r="266.23" fill="#ffffff" />')
    svg_parts.append(f'      <path d="{PATH1}" fill="#000000" />')
    svg_parts.append(f'      <path d="{PATH2}" fill="#000000" />')
    svg_parts.append('    </mask>')
    svg_parts.append('  </defs>')
    
    # Modules
    paths = []
    for y in range(height):
        for x in range(width):
            if matrix[y][x]:
                if is_eye(y, x, width, height):
                    # Eye module (sharp square)
                    paths.append(f"M {x} {y} h 1 v 1 h -1 Z")
                else:
                    # Data module (round corners merging with neighbors)
                    N = matrix[y - 1][x] if y > 0 else False
                    S = matrix[y + 1][x] if y < height - 1 else False
                    E = matrix[y][x + 1] if x < width - 1 else False
                    W = matrix[y][x - 1] if x > 0 else False
                    paths.append(get_module_path(x, y, N, S, E, W, r=0.5))
                    
    svg_parts.append(f'  <path d="{" ".join(paths)}" fill="{fill_color}" />')
    
    # Logo Group (Decoupled circle size: 45% circle, 35% D)
    circle_scale = 0.45
    d_scale = 0.35
    qr_width_modules = width - 4
    logo_size_modules = qr_width_modules * circle_scale
    d_size_modules = qr_width_modules * d_scale
    scale_factor = d_size_modules / 532.46
    
    # Center the D relative to the circle canvas
    tx = width / 2.0 - d_size_modules / 2.0
    ty = height / 2.0 - d_size_modules / 2.0
    
    # Circle center relative to the QR code
    circle_cx = width / 2.0
    circle_cy = height / 2.0
    circle_r_modules = logo_size_modules / 2.0
    
    svg_parts.append('  <!-- Fading Circle Background -->')
    svg_parts.append(f'  <circle cx="{circle_cx:.4f}" cy="{circle_cy:.4f}" r="{circle_r_modules:.4f}" fill="url(#cream-fade)" />')
    
    # Logo paths are shifted and scaled
    svg_parts.append(f'  <g transform="translate({tx:.4f}, {ty:.4f}) scale({scale_factor:.6f})">')
    svg_parts.append('    <!-- Solid Cream Hollow Inside -->')
    svg_parts.append(f'    <path d="{PATH2}" fill="#fcf3da" />')
    svg_parts.append('    <!-- Solid Inverted Color D -->')
    svg_parts.append(f'    <rect x="0" y="0" width="532.46" height="532.46" fill="{d_color}" mask="url(#d-logo-mask)" />')
    svg_parts.append('  </g>')
    
    svg_parts.append('</svg>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_parts))
    print(f"Generated Vector SVG QR: {filename}")

def main():
    print("Initializing Dankley Premium QR Code Generator...")

    for d in OUTPUT_DIRS.values():
        os.makedirs(d, exist_ok=True)

    print("\n--- Generating Store QR Codes ---")
    for color_name, palette in COLORS.items():
        filename_png = os.path.join(OUTPUT_DIRS["store"], f"QUEENS_STORE_QR_{color_name}.png")
        generate_qr(STORE_URL, filename_png, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])
        filename_svg = os.path.join(OUTPUT_DIRS["store"], f"QUEENS_STORE_QR_{color_name}.svg")
        generate_qr_svg(STORE_URL, filename_svg, palette["fill_color"], palette["back_color"], palette["d_color"])

    print("\n--- Generating FiDi Store QR Codes ---")
    for color_name, palette in COLORS.items():
        filename_png = os.path.join(OUTPUT_DIRS["fidi"], f"FIDI_STORE_QR_{color_name}.png")
        generate_qr(FIDI_URL, filename_png, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])
        filename_svg = os.path.join(OUTPUT_DIRS["fidi"], f"FIDI_STORE_QR_{color_name}.svg")
        generate_qr_svg(FIDI_URL, filename_svg, palette["fill_color"], palette["back_color"], palette["d_color"])

    print("\n--- Generating Events QR Codes ---")
    for color_name, palette in COLORS.items():
        filename_png = os.path.join(OUTPUT_DIRS["events"], f"QUEENS_EVENTS_QR_{color_name}.png")
        generate_qr(EVENTS_URL, filename_png, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])
        filename_svg = os.path.join(OUTPUT_DIRS["events"], f"QUEENS_EVENTS_QR_{color_name}.svg")
        generate_qr_svg(EVENTS_URL, filename_svg, palette["fill_color"], palette["back_color"], palette["d_color"])

    print("\n--- Generating Consultation QR Codes ---")
    for color_name, palette in COLORS.items():
        filename_png = os.path.join(OUTPUT_DIRS["consultation"], f"QUEENS_CONSULTATION_QR_{color_name}.png")
        generate_qr(CONSULTATION_URL, filename_png, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])
        filename_svg = os.path.join(OUTPUT_DIRS["consultation"], f"QUEENS_CONSULTATION_QR_{color_name}.svg")
        generate_qr_svg(CONSULTATION_URL, filename_svg, palette["fill_color"], palette["back_color"], palette["d_color"])

    print("\n--- Generating Directions QR Codes ---")
    for color_name, palette in COLORS.items():
        filename_png = os.path.join(OUTPUT_DIRS["directions"], f"QUEENS_DIRECTIONS_QR_{color_name}.png")
        generate_qr(DIRECTIONS_URL, filename_png, palette["fill_color"], palette["back_color"], palette["logo_file"], palette["d_color"])
        filename_svg = os.path.join(OUTPUT_DIRS["directions"], f"QUEENS_DIRECTIONS_QR_{color_name}.svg")
        generate_qr_svg(DIRECTIONS_URL, filename_svg, palette["fill_color"], palette["back_color"], palette["d_color"])

    print("\nAll premium QR codes successfully generated in the 'qr assets' folder!")

if __name__ == "__main__":
    main()
