from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = list()
        current_mode = binary_image[0][0]
        rle_code.append(1 if current_mode == 255 else 0) # First pixel value for reference
        run_counter = 1
        for i in range(binary_image.shape[0]):
            for j in range(binary_image.shape[1]):
                if (i, j) == (0, 0):
                    continue
                if (binary_image[i][j] == current_mode): 
                    run_counter += 1
                else:
                    current_mode = binary_image[i][j]
                    rle_code.append(run_counter)
                    run_counter = 1
        rle_code.append(run_counter) # Capture the last bits of pixels
        return rle_code

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        reconstructed_img = zeros((height, width), uint8) # Start with black image
        current_color = 0 if rle_code[0] == 0 else 1
        rle_index = 1

        for i in range(reconstructed_img.shape[0]):
            for j in range(reconstructed_img.shape[1]):
                if rle_code[rle_index] == 0: # No more pixels to add of this color
                    current_color = (current_color + 1) % 2 # Allows alternating between 0 and 1
                    rle_index += 1
                reconstructed_img[i][j] = 0 if current_color == 0 else 255
                rle_code[rle_index] -= 1
        return reconstructed_img