from webcam import Webcam
import cv2
from datetime import datetime

webcam = Webcam()
webcam.start()
i = 0
while True:

    # get image from webcam
    image = webcam.get_current_frame()

    # display image
    cv2.imshow('grid', image)
    cv2.waitKey(3000)

    # save image to file, if pattern found
    ret, corners = cv2.findChessboardCorners(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (7, 6), None)
    print (ret)

    if ret == True:
        i += 1
        print (i)
        if i == 10:
            break
        filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
        cv2.imwrite("sample_images/" + filename, image)