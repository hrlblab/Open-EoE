import logging
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()
import numpy as np
import gc
import cv2
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(r'C:\openslide-win64-20230414\bin'):
        import openslide
else:
    import openslide


def read_scn(scn_file):
    try:
        slide = openslide.open_slide(scn_file)
        height = int(slide.properties['openslide.region[0].height'])
        width = int(slide.properties['openslide.region[0].width'])
        x = int(slide.properties['openslide.region[0].x'])
        y = int(slide.properties['openslide.region[0].y'])
        img_slide = slide.read_region((x, y), 0, (width, height))
        img = np.array(img_slide.convert('RGB'))
        del img_slide
        gc.collect()
        # pad image with white pixels
        if img.shape[1] % patch_size != 0 or img.shape[0] % patch_size != 0:
            pad_width = patch_size - img.shape[1] % patch_size
            pad_height = patch_size - img.shape[0] % patch_size
            padded_img = np.pad(img, ((0, pad_height), (0, pad_width), (0, 0)), mode='constant',constant_values=255)

            del img
            gc.collect()
            return padded_img
        else:
            return img        
    except Exception as e:
        logging.error(scn_file)
        return None



def divide_into_patches(pad_image, patch_size, out_path):
    for y in range(0, pad_image.shape[0], patch_size):
        for x in range(0, pad_image.shape[1], patch_size):
            patch = pad_image[y:y + patch_size, x:x + patch_size]
            patch_bgr = cv2.cvtColor(patch, cv2.COLOR_RGB2BGR)
            output_filename = os.path.join(out_path, f"{x}_{y}.jpg")
            cv2.imwrite(output_filename, patch_bgr)


def scn_to_patch(input_path, patch_size, output_path):
    for file_name in os.listdir(input_path):
        scn_file = os.path.join(input_path, file_name)
        image = read_scn(scn_file)
        if image is not None:
            output_folder = file_name.split('.')[0]
            full_output_folder = os.path.join(output_path, output_folder)
            if not os.path.exists(full_output_folder):
                os.makedirs(full_output_folder)
            divide_into_patches(image, patch_size, full_output_folder)



if __name__ == '__main__':
    path = 'WSIs'
    patch_size = 512
    output_path = 'Patches'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    logging.basicConfig(filename="failed_file.log", filemode="w", level=logging.INFO)
    scn_to_patch(path, patch_size,output_path)
