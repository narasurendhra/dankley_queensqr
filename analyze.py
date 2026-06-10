import collections
from PIL import Image

def get_top_colors(image_path):
    img = Image.open(image_path).convert("RGBA")
    colors = img.getcolors(maxcolors=100000)
    
    # Sort by count (descending)
    sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
    
    print(f"\nTop colors in {image_path}:")
    for count, color in sorted_colors[:5]:
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        print(f"  {hex_color} (Alpha: {color[3]}) - Count: {count}")

get_top_colors('C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/qr assets/queens_events/QUEENS_EVENTS_QR_Dark_Green.png')
get_top_colors('C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/qr assets/queens_events/QUEENS_EVENTS_QR_Terracotta.png')


