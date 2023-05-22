import cv2

detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

while True:
    res, b = video_capture.read()
    grey = cv2.cvtColor(b ,cv2.COLOR_BGR2GRAY)
    faces = detect.detectMultiScale(grey,1.1,4)
    for(x,y,w,h) in faces:
        cv2.rectangle(b,(x,y),(x+w, y+h),(255,255,0),2)
    cv2.imshow("video",b)
    if cv2.waitKey(1) and 0xFF == ord("q"):
        break
video_capture.release()

cv2.destroyAllWindows()
