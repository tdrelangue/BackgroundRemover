import os
from PIL import Image, ImageFilter
import re


def blur_edges(image, rad):
    # Apply a Gaussian blur to smooth out jagged edges
    smoothed_image = image.filter(ImageFilter.GaussianBlur(radius=rad))
    return smoothed_image


def update_filename_suffix(input_filename):
    # Check if there is a number between parentheses at the end of the filename
    match = re.search(r'\((\d+)\)\.jpg$', input_filename)

    if match:
        # Increment the found number by 1
        number = int(match.group(1))
        updated_number = number + 1
        updated_filename = re.sub(r'\(\d+\)\.jpg$', f'({updated_number})', input_filename)
    else:
        # Add "(1)" if there is no number between parentheses at the end
        updated_filename = f'{input_filename[:-3]}(1)'

    return updated_filename


def smooth_lines(image, percentage, gauss_index):
    # smoothed_image = blur_edges(image, 0.5 + 0.5 * (gauss_index ** 1.5))
    smoothed_image = blur_edges(image, 0.5)

    # Convert pixels based on the specified condition
    for x in range(smoothed_image.width):
        for y in range(smoothed_image.height):
            pixel_value = smoothed_image.getpixel((x, y))
            if pixel_value < percentage * 255:  # Assuming 128 as the threshold for 50% gray
                smoothed_image.putpixel((x, y), 0)  # Set pixel to black
            else:
                smoothed_image.putpixel((x, y), 255)  # Set pixel to white
    return smoothed_image


def convert_to_bw(input_directory, output_directory, percentage, desired_res):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Construct full paths for input and output images
            input_image_path = os.path.join(input_directory, filename)
            output_file_name = update_filename_suffix(filename)
            output_image_path = os.path.join(output_directory, f"{output_file_name}")

            # Open the JPG image
            pil_image = Image.open(input_image_path)

            # Convert the image to grayscale
            grayscale_image = pil_image.convert("L")
            i = 0
            smoothed_image = smooth_lines(grayscale_image, percentage, i)
            (width, height) = smoothed_image.size

            # while width < desired_res:
            for i in range(1, 50):
                # Smooth out jagged edges
                # resized_image = ic(smoothed_image.resize((width*2, height*2)))
                # smoothed_image = smooth_lines(resized_image, percentage, i)
                smoothed_image = smooth_lines(smoothed_image, percentage, i)
                i += 1
                (width, height) = smoothed_image.size

            # Save the modified image as JPG in the output directory
            smoothed_image.save(update_filename_suffix(output_image_path), "JPEG", quality=100)
            # Adjust quality as needed


def transform_white_to_transparent(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            input_image_path = os.path.join(input_directory, filename)

            # Ouvrir l'image avec Pillow
            img = Image.open(input_image_path)

            output_file_name = update_filename_suffix(filename)
            output_image_path = os.path.join(output_directory, f"{output_file_name}")

            # Convertir l'image en mode RGBA (si elle n'est pas déjà dans ce mode)
            img = img.convert("RGBA")

            # Obtenir les données des pixels
            data = img.getdata()

            # Parcourir chaque pixel
            new_data = []
            for item in data:
                # Si le pixel est blanc (255, 255, 255), le rendre transparent (0)
                if item[:3] >= (125, 125, 125):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            # Mettre à jour les données de l'image
            img.putdata(new_data)

            # Enregistrer l'image transformée
            img.save(update_filename_suffix(output_image_path)+".png")


if __name__ == "__main__":
    input_jpg_path = "input"
    output_path = "output"

    # convert_to_bw(input_jpg_path, output_path, 0.75, 5000)
    transform_white_to_transparent(input_jpg_path, output_path)
