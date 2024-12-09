from PIL import Image

def load_and_resize_image(image_path, size):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.Resampling.LANCZOS)  
        return img
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        return None

def get_min_size(images):
    sizes = [img.size for img in images]
    min_width = min(size[0] for size in sizes)
    min_height = min(size[1] for size in sizes)
    return (min_width, min_height)

def create_collage(images, output_path, output_format):
    min_size = get_min_size(images)
    resized_images = [img.resize(min_size, Image.Resampling.LANCZOS) for img in images]

    collage_width = min_size[0] * 2
    collage_height = min_size[1] * 2
    collage = Image.new('RGB', (collage_width, collage_height))

    collage.paste(resized_images[0], (0, 0))
    collage.paste(resized_images[1], (min_size[0], 0))
    collage.paste(resized_images[2], (0, min_size[1]))
    collage.paste(resized_images[3], (min_size[0], min_size[1]))

    if output_format.lower() in ['jpg', 'jpeg']:
        collage = collage.convert('RGB')

    if output_format.lower() == 'jpg':
        output_format = 'JPEG'

    collage.save(output_path, format=output_format.upper())
    print(f"Collage saved as {output_path}")

def main():
    image_paths = []
    for i in range(1, 5):
        image_path = input(f"Please enter the path for Image {i}: ")
        image_paths.append(image_path)

    images = [load_and_resize_image(path, (300, 300)) for path in image_paths]
    images = [img for img in images if img]  # Filter out None (failed loads)

    if len(images) != 4:
        print("Error: Unable to load all 4 images. Please check the file paths and formats.")
        return

    output_format = input("Please specify the output file format (jpg, jpeg, png, tiff, bmp): ").lower()
    if output_format not in ['jpg', 'jpeg', 'png', 'tiff', 'bmp']:
        print("Error: Unsupported output format. Please use 'jpg', 'jpeg', 'png', 'tiff', or 'bmp'.")
        return
    output_path = f"collage.{output_format}"
    create_collage(images, output_path, output_format)

if __name__ == "__main__":
    main()
