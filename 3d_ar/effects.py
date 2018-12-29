import cv2
import numpy as np


class Effects:

    def render_cube(self, image, points):
        # load calibration data
        with np.load('outfile.npz') as X:
            mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]

        # set up criteria, image, points and axis
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        imgp = np.array(points, dtype="float32")

        objp = np.array([[0., 0., 0.], [1., 0., 0.],
                         [1., 1., 0.], [0., 1., 0.]], dtype="float32")

        axis = np.float32([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0],
                           [0, 0, -1], [0, 1, -1], [1, 1, -1], [1, 0, -1]])

        # project 3D points to image plane
        cv2.cornerSubPix(gray, imgp, (11, 11), (-1, -1), criteria)
        rvecs, tvecs, _ = cv2.solvePnPRansac(objp, imgp, mtx, dist)
        imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

        # draw cube
        self._draw_cube(image, imgpts)

        return image

    def _draw_cube(self, image, imgpts):
        imgpts = np.int32(imgpts).reshape(-1, 2)

        # draw pillars
        for i, j in zip(range(4), range(4, 8)):
            cv2.line(image, tuple(imgpts[i]), tuple(imgpts[j]), (100, 100, 100), 4)

        # draw roof
        cv2.drawContours(image, [imgpts[4:]], -1, (100, 100, 100), 4)