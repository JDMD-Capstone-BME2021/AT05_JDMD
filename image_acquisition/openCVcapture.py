import cv2

camera = cv2.VideoCapture(0)
cv2.namedWindow("my image")

while(True):
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if camera.isOpened() == False:
    print ("Camera is not working!")

camera.release()
cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
