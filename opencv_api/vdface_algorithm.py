from __future__ import print_function
import cv2
from django.conf import settings
from .models import VideoUploadModel

work_percent = 0
number_faces = 0


def count_frames(path, override=False):
    video = cv2.VideoCapture(path)
    if override:
        total = count_frames_manual(video)
    else:
        try:
            total = int(video.get(cv2.CV_CAP_PROP_FRAME_COUNT))
        except Exception:
            total = count_frames_manual(video)
    video.release()
    return total


def count_frames_manual(video):
    total = 0
    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
            break
        total += 1
    return total


def detect(frame, face_cascade):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)

    faces = face_cascade.detectMultiScale(frame_gray)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return len(faces)


def opencv_detect(path, video_id):
    global work_percent, number_faces
    work_percent = 0
    number_faces = 0

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    face_cascade = cv2.CascadeClassifier(base_url + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(path)

    all_frames_count = count_frames(path)
    print(all_frames_count)
    frame_counter = 0
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    if VideoUploadModel.objects.filter(id=video_id).get().status != 'canceled':
        VideoUploadModel.objects.filter(id=video_id).update(status='processing')
    while True:
        db_video = VideoUploadModel.objects.filter(id=video_id).get()
        if db_video.status == 'canceled':
            print('--(!) Processing video is canceled -- Break!')
            break
        else:
            ret, frame = cap.read()
            if frame is None:
                print('--(!) No captured frame -- Break!')
                VideoUploadModel.objects.filter(id=video_id).update(status='completed')
                break
            if db_video.status == 'waiting' or 'processing':
                number_faces += detect(frame, face_cascade)
                frame_counter += 1
                work_percent = round((frame_counter / all_frames_count) * 100)
                if work_percent > db_video.current_progress:
                    VideoUploadModel.objects.filter(id=video_id).update(current_progress=work_percent,
                                                                        faces_count=number_faces, )
                    print('update db')
            if cv2.waitKey(10) == 27:
                break
    return {'current_progress': work_percent, 'faces_count': number_faces}
