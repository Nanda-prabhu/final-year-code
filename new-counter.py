from email_services import send_mail
import supervision as sv
import cv2
from ultralytics import YOLO
from datetime import datetime, timedelta

# Define a function for image resizing
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

# Load YOLO model
model = YOLO('yolov8n.pt')

# Open video file
cap = cv2.VideoCapture("source.mp4")

lastMailSentTime = datetime.now() - timedelta(seconds=30)
print("last mail sent time beginning: ", lastMailSentTime)

# Loop indefinitely for live webcam feed
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Resize frame
    resized_frame = image_resize(frame, height=400)

    if ret:
        # Get detections from YOLO model
        results = model(resized_frame, imgsz=1280)[0]

        detections = sv.Detections.from_yolov8(results)
        detections = detections[detections.class_id == 0]

        # Annotate detections on the frame
        box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=1)
        frame_annotated = box_annotator.annotate(scene=resized_frame, detections=detections)

        # Display count of detections
        count_text = "Count=" + str(len(detections))
        cv2.putText(frame_annotated, count_text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (225, 225, 225), 2)

        # email if count > 40 with a mail buffer of one minute
        if len(detections) > 45:
            if datetime.now() > lastMailSentTime + timedelta(seconds=30):
                cv2.imwrite("captures/capture.png", frame_annotated)
                send_mail(from_gmail="dummybb63@gmail.com", to_gmail="nanda96here@gmail.com", from_gmail_key="jrfjmgkesvswcxjf")
                lastMailSentTime = datetime.now()
            else:
                print("Should habe sent mail but last mail was sent only one minute ago")

        # Display the frame
        cv2.imshow('Webcam', frame_annotated)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error reading frame from the webcam")
        break

# Release the webcam and close the display window
cap.release()
cv2.destroyAllWindows()
