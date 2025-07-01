import cv2, numpy as np

class HarrisCorner():
    def __init__(self, MAP):
        self.map_data = np.array(MAP, dtype=np.uint8)


    #Apply Gaussian blur to the map
    def gaussianBlur(self, map, ksize=(9,9), sigX=0, sigY=0):
        blurred_map = cv2.GaussianBlur(
            src=np.array(map,dtype=np.uint8),
            ksize=ksize,
            sigmaX=sigX,
            sigmaY=sigY
            )
        return blurred_map
    
    
    #Non-Maximum Suppression
    def non_max_suppression(self, response, nmx_threshold=0.1, dilate_size=5):
        dilated = cv2.dilate(response, np.ones((dilate_size, dilate_size), np.uint8))
        det = np.zeros_like(dilated)
        det[(response == dilated) & (response > nmx_threshold)] = 1
        
        return det
    
    
    #Harris corner detection
    def harrisCorner(self, map, block_size=3, ksize=3, k=0.05, threshold=0.01):
        # 1) Harris corner detection
        harris_response = cv2.cornerHarris(
                                    src=np.array(map, dtype=np.float32),
                                    blockSize=block_size,
                                    ksize=ksize,
                                    k=k )
        # 2) Set threshold dynamically 
        harris_threshold = threshold * harris_response.max()
        harris_response[harris_response < harris_threshold] = 0

        return harris_response
    
    
    #filter out close corners based on Euclidean distance
    def filter_close_corners(self, points, min_distance=5):
        filtered_points = []
        for p in points:
            if all(np.linalg.norm(np.array(p) - np.array(fp)) >= min_distance for fp in filtered_points):
                filtered_points.append(p)
        return filtered_points
    
    
    #return final corner coordinates
    def extract(self, map):
        # (y, x) --> (x, y) conversion
        points = np.where(map == 1)
        raw_corners = list(zip(points[1], points[0]))
        
        return self.filter_close_corners(raw_corners)



    def run(self, map, block_size=3, ksize=3, k=0.05, dilate_size=5):
        #1)Apply Gaussian blur
        blurred = self.gaussianBlur(map)
        
        #2)Harris corner detection
        harris_response = self.harrisCorner(blurred, block_size, ksize, k, 0.1)
        temp=(0.1*harris_response.max())
        
        #3)Non-Maximum Suppression
        dilated = self.non_max_suppression(harris_response, temp, dilate_size=dilate_size)
 
        #4-1)Extract corners
        corners = self.extract(dilated)
        #4-2)Filter close corners
        corners = self.filter_close_corners(corners, min_distance=5)
        return corners


