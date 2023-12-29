import cv2
import numpy as np
from moviepy import editor



def average_slope_intercept(lines):

    left_lines    = [] #(slope, intercept)
    left_weights  = [] #(length,)
    right_lines   = [] #(slope, intercept)
    right_weights = [] #(length,)
     
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            # calculating slope of a line
            slope = (y2 - y1) / (x2 - x1)
            # calculating intercept of a line
            intercept = y1 - (slope * x1)
            # calculating length of a line
            length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
            # slope of left lane is negative and for right lane slope is positive
            if slope < 0:
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:
                right_lines.append((slope, intercept))
                right_weights.append((length))
    # 
    left_lane  = np.dot(left_weights,  left_lines) / np.sum(left_weights)  if len(left_weights) > 0 else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
    return left_lane, right_lane
   
def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)
    return ((x1, y1), (x2, y2))
   
def lane_lines(image, lines):

    left_lane, right_lane = average_slope_intercept(lines)
    y1 = image.shape[0]
    y2 = y1 * 0.6
    left_line  = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)
    return left_line, right_line

def DetectLine(img):

    ogimg = img

    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    edge_highlighed_img = cv2.Canny(gray_img, 100, 200)

    roi_pos = np.array([[
        (0, 500),
        (1000, 500),
        (0, 700),
        (1000, 700)
    ]], np.int32)

    img = edge_highlighed_img

    blank_img = np.zeros_like(img)
    color_pixels = (255, ) * 3
    cv2.fillPoly(blank_img, roi_pos, color_pixels)
    color_filled_img = cv2.bitwise_and(img, blank_img)

    lined_img_pixels =  cv2.HoughLinesP(
        color_filled_img,
        rho = 3,
        theta = np.pi / 150,
        threshold = 170,
        lines = np.array([]),
        minLineLength = 40,
        maxLineGap = 20
    )

    lines = lined_img_pixels

    lines  = lane_lines(ogimg, lines)

    line_img = np.zeros_like(ogimg)

    for line in lines:
        if line is not None:
            cv2.line(line_img, *line,  [165, 42, 42], 15)
        # for x1, y1, x2, y2 in line:
        #     cv2.line(line_img, (x1, y1), (x2, y2), [0, 0, 255], 3)

    line_img = cv2.addWeighted(ogimg, 0.8, line_img, 1.0, 0.0)

    return line_img

test_video = "media/test_videos/video3.mp4"
output_video = "media/results/resultvideo.mp4"

input_video = editor.VideoFileClip(test_video, audio=False)

processed = input_video.fl_image(DetectLine)

processed.write_videofile(output_video, audio=False)