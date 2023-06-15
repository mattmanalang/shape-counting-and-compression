# Shape Counting and Compression
---
## Topics Covered
> Binary image processing, iterative thresholding, blob coloring

## Synopsis
This assignment focused on binary image processing and compression via run-length encoding.
For shape counting, a greyscale image is generated with a random amount of selected shapes. Region_analysis/binary_image.py contains functions that convert the greyscale image into a binary image by finding an optimal threshold using an iterative approach.
Following this, blob coloring is then performed on the binary image to identify regions of interest which are then recognized as their respective shape with at least 95% accuracy.
