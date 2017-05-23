import picamera
from time import sleep
from vision import *
from control import *

# setup camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_preview()

sleep(0.2)  # wait for camera to start and focus

# process image one frame at a time, calculate movement after each frame
while True:
    # empty 1D array that is a template for the captured image data
    img = np.empty((WIDTH * HEIGHT * 3), dtype=np.uint8)

    camera.capture(img, 'bgr')

    dir_p = find_dir(img)

    speeds = motor_speeds(dir_p)
    set_motors(speeds)

    # exit when q is pressed
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cleanup()
