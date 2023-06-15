import dip
import math

class ShapeCounting:
    def __init__(self):
        pass


    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes as input:
        image: binary image
        return: a list/dict of regions
        """
        def absorb_region(regions, target, into):
            for coordinate, region_no in regions.items():
                if region_no == target:
                    regions[coordinate] = into

        def group_by_region(region_list):
            regions_recompiled = dict()
            key_view = regions_recompiled.keys()
            for coordinate, region_no in region_list.items():
                if region_no not in key_view:
                    regions_recompiled[region_no] = [coordinate]
                else:
                    regions_recompiled[region_no].append(coordinate)
            return regions_recompiled

        region_map = dict() # Stored as {(i,j) : region_no}
        k = 1 # Region counter

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i][j] == 255 and image[i][j-1] == 0 and image[i-1][j] == 0:
                    region_map[(i,j)] = k
                    k += 1
                if image[i][j] == 255 and image[i][j-1] == 0 and image[i-1][j] == 255:
                    region_map[(i,j)] = region_map[(i-1,j)]
                if image[i][j] == 255 and image[i][j-1] == 255 and image[i-1][j] == 0:
                    region_map[(i,j)] = region_map[(i,j-1)]
                if image[i][j] == 255 and image[i][j-1] == 255 and image[i-1][j] == 255:
                    region_map[(i,j)] = region_map[(i-1,j)]
                    if region_map[(i,j-1)] != region_map[(i-1,j)]:
                        absorb_region(region_map, region_map[(i,j-1)], region_map[(i-1,j)]) # Absorbs the left region into the region found on top
        regions = group_by_region(region_map) # Stored as {region_no : [list of (i,j)'s]}
        return regions
    

    def identify_shapes(self, region):
        """Compute shape features area and centroid, and shape
        Ignore shapes smaller than 10 pixels in area.
        takes as input
        region: a list/dict of pixels in a region
        returns: shapes, a data structure with centroid, area, and shape (c, s, r, or e) for each region
        c - circle, s - squares, r - rectangle, and e - ellipse
        """
        # Please print your shape statistics to stdout, one line for each shape
        # Region: <region_no>, centroid: <centroid>, area: <shape area>, shape: <shape type>
        # Example: Region: 871, centroid: (969.11, 51.11), area: 707, shape: c
        def remove_small_regions(regions): # Remove small regions < 10px from the list
            filtered_regions = dict(regions)
            for region_no, coordinate_list in regions.items():
                if len(coordinate_list) < 10:
                    filtered_regions.pop(region_no)
                else:
                    pass
            return filtered_regions
        
        def regions_reach(coordinates): # Find the extremities of the region
            # Lower i's are higher up, and lower j's are more left
            top_most = min(coordinates, key=lambda point: point[0])[0]
            bottom_most = max(coordinates, key=lambda point: point[0])[0]
            left_most = min(coordinates, key=lambda point: point[1])[1]
            right_most = max(coordinates, key=lambda point: point[1])[1]
            return {"top":top_most, "right":right_most, "bottom":bottom_most, "left":left_most}
        
        def centroid(coordinates):
            # Grabbing the i's and j's that represent the farthest span of the region in all four directions
            span = regions_reach(coordinates)
            north_i = span["top"]
            south_i = span["bottom"]
            west_j = span["left"]
            east_j = span["right"]
            centroid_i = (north_i + south_i)/2
            centroid_j = (west_j + east_j)/2
            return (centroid_i, centroid_j)
        
        def classify_shape(coordinates):
            def distance(target, pixel): # Euclidean distance
                return math.sqrt((pixel[1] - target[1])**2 + (pixel[0] - target[0])**2)
        
            # Gathering features about the region
            span = regions_reach(coordinates)
            north_i = span["top"]
            south_i = span["bottom"]
            west_j = span["left"]
            east_j = span["right"]
            northwest_corner = (north_i, west_j)
            corner_area = [point for point in coordinates if distance(northwest_corner, point) < 5]
            true_area = len(coordinates)
            height = abs(north_i - south_i)
            width = abs(east_j - west_j)

            if any(point in corner_area for point in coordinates): # Corner area found, could be a SQUARE or a RECTANGLE
                return "s" if abs((width**2) - (height**2))/true_area < 0.03 else "r"
            else: # Corner area not found, could be a CIRCLE or an ELLIPSE
                return "c" if abs((3.14159 * (width/2)**2) - true_area)/true_area < 0.05 else "e"

        filtered_regions = remove_small_regions(region)
        shapes = dict() 
        for region_no, coordinates in filtered_regions.items():
            shapes[region_no] = {"Area" : len(coordinates)} # Establishes a nested dictionary as the value for each key
            shapes[region_no]["Centroid"] = centroid(coordinates)
            shapes[region_no]["Shape"] = classify_shape(coordinates)
            print("Region: {}, Centroid: {}, Area: {}, Shape: {}".format(region_no, shapes[region_no]["Centroid"], shapes[region_no]["Area"], shapes[region_no]["Shape"]))

        return shapes


    def count_shapes(self, shapes_data): 
        """Compute the count of shapes using the shapes data returned from identify shapes function
        takes as input
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: a dictionary with count of each shape
        Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
        """
        circles = sum(1 for region in shapes_data.values() if region["Shape"] == "c")
        ellipses = sum(1 for region in shapes_data.values() if region["Shape"] == "e")
        rectangles = sum(1 for region in shapes_data.values() if region["Shape"] == "r")
        squares = sum(1 for region in shapes_data.values() if region["Shape"] == "s")

        return {"circles": circles, "ellipses": ellipses, "rectangles": rectangles, "squares": squares}


    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""
        marked_image = image.copy()
        for region, stats in shapes_data.items():
            centroid = stats["Centroid"]
            text = stats["Shape"]
            position = (round(centroid[1]), round(centroid[0]))
            dip.putText(marked_image, text, position, dip.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

        return marked_image