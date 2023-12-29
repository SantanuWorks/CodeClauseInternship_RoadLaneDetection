import cv2
import numpy as np
from moviepy import editor 

def to_gray_scale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

def to_gaussian_blur(img):
    blur_img = cv2.GaussianBlur(img, (5, 5), 0)
    return blur_img

def canny_edge_detector(img):
    cannied_img = cv2.Canny(img, 100, 200)
    return cannied_img

def lane_color_separation(hsv_img, gray_img):
    ylw_low = np.array([20, 100, 100], dtype="uint8")
    ylw_high = np.array([30, 255, 255], dtype="uint8")
    mask_yellow = cv2.inRange(hsv_img, ylw_low, ylw_high)
    mask_white = cv2.inRange(gray_img, 200, 255)
    mask_colors = cv2.bitwise_or(mask_yellow, mask_white)
    lanned_img = cv2.bitwise_and(gray_img, mask_colors)
    return lanned_img

def select_area(img):
    pseudo_img = np.zeros_like(img)
    img_height = img.shape[0]
    img_width = img.shape[1]
    area = np.array([ [ (0, img_height), (0, int(img_height*0.7)), (int(img_width*0.5), int(img_height*0.55)), (img_width, int(img_height*0.7)), (img_width, img_height) ] ])
    pseudo_img = cv2.fillPoly(pseudo_img, area, 255)
    select_area = cv2.bitwise_and(img, pseudo_img)
    return select_area

def get_hough_transform_lines(img):
    img_lines = cv2.HoughLinesP(img, rho=2, theta=np.pi/180, threshold=100, lines=np.array([]), minLineLength=40, maxLineGap=5)
    return img_lines

def get_start_end_point(height, slop_incept):
    slop = slop_incept[0] # m
    incept = slop_incept[1] # c 
    
    # y1 = x1 x slop + incept ( y = mx + c )
    # y2 = x2 x slop + incept ( y = mx + c )

    y1 = height
    y2 = int(height/2 + 50)
    
    x1 = int((y1 - incept) // slop)
    x2 = int((y2 - incept) // slop)

    return np.array([x1, y1, x2, y2])

def get_left_right_line(img_height, lines):
    left_slop_incepts = []
    right_slop_incepts = []

    '''
        Line Equation: y = mx + c

        m = slop 

        c = y-intercept
 
        if slop is negative, then line is before 90 deg ( left line )
        
        else line is right
    '''  

    main_left_line = []    
    main_right_line = []

    if lines is not None:
        for line in lines:
            if line.size != 0:
                x1, y1, x2, y2 = line[0]
                slop_incept = np.polyfit((x1, x2), (y1, y2), 1)
                slop = slop_incept[0]
                incept = slop_incept[1]
                if slop < 0:
                    left_slop_incepts.append((slop, incept))
                else:
                    right_slop_incepts.append((slop, incept))
    
        '''
            find slop and intercept for the whole line 
            by taking the avg of them 
        '''
        
        whole_left_line_slop_incept = np.average(left_slop_incepts, axis=0)
        whole_right_line_slop_incept = np.average(right_slop_incepts, axis=0)

        main_left_line = get_start_end_point(img_height, whole_left_line_slop_incept)
        main_right_line = get_start_end_point(img_height, whole_right_line_slop_incept)

    return np.array([main_left_line, main_right_line])        

def put_lines(img, lines):
    lined_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            if line.size != 0:
                x1, y1, x2, y2 = line
                cv2.line(lined_img, (x1, y1), (x2, y2), (255, 0, 0), 20)
    return lined_img

def LaneDetector(og_img):
    hsv_img = cv2.cvtColor(og_img, cv2.COLOR_RGB2HSV)

    gray_img = to_gray_scale(og_img)

    lanned_img = lane_color_separation(hsv_img, gray_img)

    cannied_img = canny_edge_detector(lanned_img)

    selected_area_img = select_area(cannied_img)

    lines = get_hough_transform_lines(selected_area_img)

    left_right_line = get_left_right_line(og_img.shape[0], lines)

    lined_img = put_lines(og_img, left_right_line)

    line_detected_img = cv2.addWeighted(og_img, 0.8, lined_img, 1, 1)
    
    return line_detected_img

og_img = cv2.imread("media/test_images/img2.jpg")

cv2.imshow("Image", LaneDetector(og_img))
cv2.waitKey(0)

# test_video = "media/test_videos/video2.mp4"
# output_video = "media/results/resultvideo.mp4"

# input_video = editor.VideoFileClip(test_video, audio=False)

# processed = input_video.fl_image(LaneDetector)

# processed.write_videofile(output_video, audio=False)
