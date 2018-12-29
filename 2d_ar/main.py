import cv2
from glyphdatabase import *
from glyphfunctions import *
from webcam import Webcam

webcam = Webcam()
webcam.start()

QUADRILATERAL_POINTS = 4
SHAPE_RESIZE = 100.0
BLACK_THRESHOLD = 100
WHITE_THRESHOLD = 155

while True:

    # Stage 1: Read an image from our webcam
    image = webcam.get_current_frame()

    # Stage 2: Detect edges in image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 100, 200)
   

    # Stage 3: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:

        # Stage 4: Shape check
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

        if len(approx) == QUADRILATERAL_POINTS:

            # Stage 5: Perspective warping
            topdown_quad = get_topdown_quad(gray, approx.reshape(4, 2))

            # Stage 6: Border check
            resized_shape = resize_image(topdown_quad, SHAPE_RESIZE)
            # if resized_shape[5, 5] > BLACK_THRESHOLD: continue
            if resized_shape[(resized_shape.shape[0] / 100.0) * 5,
                             (resized_shape.shape[1] / 100.0) * 5] > BLACK_THRESHOLD: continue

            # Stage 7: Glyph pattern
            glyph_pattern = get_glyph_pattern(resized_shape, BLACK_THRESHOLD, WHITE_THRESHOLD)
            glyph_found, glyph_rotation, glyph_substitute = match_glyph_pattern(glyph_pattern)

            if glyph_found:

                # Stage 8: Substitute glyph
                substitute_image = cv2.imread('{}.jpg'.format(glyph_substitute))

                for _ in range(glyph_rotation):
                    substitute_image = rotate_image(substitute_image, 90)

                image = add_substitute_quad(image, substitute_image, approx.reshape(4, 2))

    # Stage 9: Show augmented reality
    cv2.imshow('2D Augmented Reality using Glyphs', image)
    cv2.waitKey(10)