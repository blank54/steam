### 2. _HarrisCorner_ Class
The _HarrisCorner_ class provides a simple interface for detecting corner points in a given 2D map using the Harris corner detection algorithm in OpenCV.
You just need to provide your map(as a NumPy array) to initialize the detector.

```python
import numpy as np
from _MAPS_.<your_map_repo>.<your_map_file> import MAP
from _HarrisCorner.HCD_tools import HarrisCorner  #HCD:Harris Corner Detector

HCD_instance = HarrisCorner(MAP) # When you create the HCD instance, simply pass your MAP as the argument:
```

The _HarrisCorner_ class provides 6 main methods. described below:

1. **`.gaussianBlur(self, map, ksize, sigX, sigY)`**
  Applies a Gaussian blur to the input map to reduce noise and improve corner detection robustness.

  - ***Parameters:***
    - `ksize`: (Tuple) The kernel size for the Gaussian filter, given as a tuple `(height, width)`. For example, `(9, 9)` means the filter covers a 9×9 window.

    - `sigX`: (Int) Standard deviation in the X direction. Controls the amount of smoothing horizontally. Default is `0`, which means it is automatically calculated from `ksize`.

    - `sigY`: (Int) Standard deviation in the Y direction. Controls the amount of smoothing vertically. Default is `0`.

  - **Notes:**  
    Similarly to convolution in image processing, a larger kernel size or larger sigma values result in a smoother (more blurred) image.

---

2. **`.non_max_suppression(self, response, nmx_threshold, dilate_size)`**  
   Applies Non-Maximum Suppression (NMS) to the Harris corner response map, keeping only the local maxima above a specified threshold. This process removes redundant or closely located corner points, ensuring that only the most prominent corners are detected.

   - ***Parameters:***
     - `response`: (NP.uint8) The Harris corner response map (2D NumPy array) to be filtered.

     - `nmx_threshold`: (Int) The threshold value. Only peaks with a response greater than this value are kept as corners.

     - `dilate_size`: (Int) The size of the dilation window used to find local maxima. For example, `dilate_size=5` means that a 5×5 neighborhood is used when checking for peak values. Default is `5`.

   - **Notes:**  
     - Increasing `dilate_size` will make NMS more selective, possibly resulting in fewer, more widely spaced corners.
     - Choosing an appropriate `nmx_threshold` helps filter out weak or insignificant corner responses.

---

3. **`.harrisCorner(self, map, block_size, ksize, k, threshold)`**  
   Computes the Harris corner response map using OpenCV's Harris corner detector.  
   Pixels with a response below the threshold (a ratio of the maximum response) are set to zero.

   - ***Parameters:***
     - `map`: (NP.uint8) A 2D NumPy array where detected corner points are marked with the value `1` (all other pixels are `0`).

     - `block_size`: (Int) The size of the neighborhood considered for corner detection. Larger values result in more regional analysis, smaller values are more local. Default is `3`.

     - `ksize`: (Int) Aperture parameter of the Sobel derivative used internally. Typical values are 3, 5, or 7. Default is `3`.

     - `k`: (Float) Harris detector free parameter, usually in the range [0.04, 0.06]. Default is `0.05`.

     - `threshold`: (Float) The threshold ratio used to filter out weak corner responses. For example, `threshold=0.01` means only pixels with a response at least 1% of the max will be kept. Default is `0.01`.

   - **Notes:**  
     - The output is a response map of the same size as the input map, with strong corners having higher values.
     - Thresholding helps remove weak or noisy detections, retaining only the most prominent corners.

---

4. **`.filter_close_corners(self, points, min_distance)`**  
   Filters out corner points that are too close to each other based on Euclidean distance.  
   This helps to remove redundant detections and ensures spatial diversity among detected corners.

   - ***Parameters:***
     - `points`: (Tuple) A list of corner point coordinates, typically as (x, y) tuples.

     - `min_distance`: (Int) The minimum allowed distance between any two corner points. If two points are closer than this value, only one is retained. Default is `5`.

   - **Notes:**  
     - This function processes the list of detected corners and keeps only those that are sufficiently spaced apart.
     - Helps to prevent clusters of corner points in dense regions, improving the quality of the final detection results.

---

5. **`.extract(self, map)`**  
   Extracts the final corner coordinates from a processed map (typically the output of non-maximum suppression).  
   Converts detected pixel positions from (row, column) tuple format to (x, y) coordinate pairs.

   - ***Parameters:***
     - `map`: (NP.uint8) A 2D NumPy array where detected corner points are marked with the value `1` (all other pixels are `0`).

   - **Returns:**  
     - A list of `(x, y)` tuples representing the coordinates of detected corner points,  
       filtered to ensure they are not too close (via `filter_close_corners`).

   - **Notes:**  
     - This function converts indices from NumPy's default (row, column) to (x, y) for consistency with typical plotting and image processing conventions.
     - It is usually used after non-maximum suppression to retrieve the positions of valid corner points.

---

6. **`.run(self, map, block_size, ksize, k, dilate_size)`**  
   Runs the full Harris corner detection pipeline on the given map, including blurring, corner response, non-maximum suppression, and filtering.

   - **Processing Steps:**
     1. **Apply Gaussian Blur:**  
        Reduces noise in the input map to improve the reliability of corner detection.
     2. **Harris Corner Detection:**  
        Computes the corner response map using specified parameters.
     3. **Non-Maximum Suppression:**  
        Retains only local maxima in the response map that are above a threshold, eliminating redundant or weak corners.
     4. **Extract Corner Coordinates:**  
        Retrieves (x, y) locations of detected corners from the suppressed map.
     5. **Filter Close Corners:**  
        Further removes corner points that are too close to each other for better spatial distribution.

   - ***Parameters:***
     - `map`: (NP.uint8) The input map or grayscale image (2D NumPy array) to process. 

     - `block_size`: (Int) Neighborhood size for corner detection. Default is `3`.

     - `ksize`: (Int) Aperture size for the Sobel operator. Default is `3`.

     - `k`: (Float) Harris detector free parameter. Default is `0.05`.

     - `dilate_size`: (Int) Size of the dilation window for non-maximum suppression. Default is `5`.

   - **Returns:**  
     - A list of `(x, y)` tuples representing the final detected corner coordinates.

   - **Notes:**  
     - This method provides an easy, single-call interface for full corner detection workflow.
     - All default parameters are chosen for general robustness, but can be tuned as needed.

