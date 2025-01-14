from PIL import Image

# Paths to your images
image_paths = [
    "plots/subsidy.png",  # Replace with the actual paths to your images
    "plots/material_tax.png",
    "plots/waste_penalty.png",
    "plots/consumer_prefs.png"
]

# Open all images
images = [Image.open(img) for img in image_paths]

# Get the dimensions of each image (assuming all are the same size)
width, height = images[0].size

# Define the gap size (in pixels)
vertical_gap = 100  # Adjust as needed
horizontal_gap = 10

# Create a blank canvas for the 2x2 grid with gaps
grid_width = 2 * width + horizontal_gap
grid_height = 2 * height + vertical_gap
grid_image = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))  # White background

# Paste images into the grid with gaps
grid_image.paste(images[0], (0, 0))                                     # Top-left
grid_image.paste(images[1], (width + horizontal_gap, 0))                # Top-right
grid_image.paste(images[2], (0, height + vertical_gap))                 # Bottom-left
grid_image.paste(images[3], (width + horizontal_gap, height + vertical_gap))  # Bottom-right

# Save the combined grid or display it
grid_image.save("combined_2x2_grid_with_gap.png")
grid_image.show()