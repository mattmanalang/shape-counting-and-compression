class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""
        

        hist = [0]*256
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                pixel_value = image[row][col]
                hist[pixel_value] += 1

        return hist

    def find_threshold(self, hist):
        """analyses a histogram it to find the optimal threshold assuming that the input histogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value
        Note: Use the iterative method to calculate the histogram. Do not use the Otsu's method
        Write your code to compute the optimal threshold method.
        This should be implemented using the iterative algorithm discussed in class (See Week 4, Lecture 7, slide 42
        on teams). Do not implement the Otsu's thresholding method. No points are awarded for Otsu's method.
        """

        # Helper functions
        delta = lambda old, new: (new - old)
        def calc_expected_value(list, start_index):
            num_of_freqs = sum(list)
            probabilities = [(frequency/num_of_freqs) for frequency in list]
            return sum(index * value for index, value in enumerate(probabilities, start=start_index))

        # Initialize threshold to K/2
        threshold = round(len(hist)/2)

        # Do
        # meanLeft = expected value for all x less than the threshold
        # meanRight = expected value for all x greater than or equal to the threshold
        # threshold = average of meanLeft and meanRight
        # While delta(meanLeft) != 0 and delta(meanRight) != 0
        prev_meanLeft = 0
        prev_meanRight = 0

        while True:
            meanLeft = calc_expected_value(hist[ :threshold], 0)
            meanRight = calc_expected_value(hist[threshold: ], threshold)
            threshold = round((meanLeft + meanRight)/2)

            if delta(prev_meanLeft, meanLeft) == 0 and delta(prev_meanRight, meanRight) == 0:
                break
            else:
                prev_meanLeft = meanLeft
                prev_meanRight = meanRight

        return threshold

    def binarize(self, image, threshold):
        """Comptues the binary image of the input image based on histogram analysis and thresholding
        takes as input
        image: a grey scale image
        threshold: to binarize the greyscale image
        returns: a binary image"""

        bin_img = image.copy()
        for row in range(bin_img.shape[0]):
            for col in range(bin_img.shape[1]):
                bin_img[row][col] = 0 if image[row][col] <= threshold else 255

        return bin_img


