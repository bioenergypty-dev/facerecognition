import cv2, dlib
from scipy.spatial import distance

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
EAR_UMBRAL = 0.23

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def procesar(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)
    if len(faces)==0: return None
    shape = predictor(gray, faces[0])
    puntos = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
    ojo_izq = puntos[36:42]
    ojo_der = puntos[42:48]
    ear = (eye_aspect_ratio(ojo_izq)+eye_aspect_ratio(ojo_der))/2
    return puntos, ear
