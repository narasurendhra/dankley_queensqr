from PIL import Image

# Open the original QR code
img = Image.open('qr assets/queens_events/QUEENS_EVENTS_QR_Dark_Green.png')
w, h = img.size

# A QR code logo is typically in the center. 
# Let's crop the center 25% of the image to see if we get the logo
crop_size = int(w * 0.25) 
left = (w - crop_size) // 2
top = (h - crop_size) // 2
right = (w + crop_size) // 2
bottom = (h + crop_size) // 2

logo = img.crop((left, top, right, bottom))
logo.save('logo_cropped.png')
print(f"Cropped logo saved as logo_cropped.png with size {logo.size}")
