#!/usr/bin/env python3

import os
import shutil
from PIL import Image

script_directory = os.path.dirname(os.path.abspath("combine_img.py"))

def merge_images(file1, file2):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGBA', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    
    return result

def getfiles(folder):
    folder_path = os.path.join(script_directory, folder)
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    image_files.sort()

    # for every file in a folder, combine, 1 + next one, replacing the first image result as file 1
    inside_path = os.path.join(folder_path, image_files[0])
    tempfile = os.path.join(folder_path,"temp.png")
    shutil.copy(inside_path, tempfile)
    if image_files:
        for i in range(1, len(image_files)):
            merged_image = merge_images(os.path.join(folder_path, image_files[0]), os.path.join(folder_path, image_files[i]))
            merged_image.save(inside_path, format="PNG", compress_level=0, optimize=False)
        shutil.move(inside_path, script_directory)
        shutil.move(os.path.join(tempfile),inside_path)
        print(f"Merging complete in folder {folder}. Result saved as {image_files[0]}")
    else:
        print(f"No image files found in folder {folder}")

def elimzeros():
    files = os.listdir(script_directory)
    for file_name in files:
        if file_name.endswith("_00000.png"):
            new_name = file_name.replace("_00000", "")
            os.rename(file_name, new_name)

    print("All done")
# Get a list of subfolders in the current working directory
folders = [f for f in os.listdir(script_directory) if os.path.isdir(f)]

# Iterate over subfolders
for folder in folders:
    getfiles(folder)
elimzeros()

