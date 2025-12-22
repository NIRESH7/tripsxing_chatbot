from PIL import Image
from collections import Counter

def get_dominant_colors(image_path, num_colors=2):
    try:
        image = Image.open(image_path)
        image = image.resize((150, 150))
        result = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
        result = result.convert('RGB')
        main_colors = result.getcolors(150*150)
        
        # Sort by count
        sorted_colors = sorted(main_colors, key=lambda x: x[0], reverse=True)
        
        hex_colors = []
        for count, col in sorted_colors:
            hex_colors.append('#{:02x}{:02x}{:02x}'.format(col[0], col[1], col[2]))
            
        print(f"Extracted Colors from {image_path}:")
        for i, color in enumerate(hex_colors):
            print(f"Color {i+1}: {color}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_dominant_colors(r"c:\tripsxing_chatbot\frontend\logo.png")
