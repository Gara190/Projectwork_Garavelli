import cv2
import os

# Caricamento del classificatore a cascata (gestisce i path relativi in modo robusto)
base_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(base_dir, 'assets', 'haarcascade_frontalface_default.xml')

# Se l'XML non è nella cartella assets, usa quello di default di cv2
if not os.path.exists(cascade_path):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(cascade_path)


def detect_faces(frame):
    """Rileva i volti nel frame e restituisce la lista dei rettangoli (x, y, w, h)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Ottimizzato per real-time su hardware limitati (es. Raspberry Pi)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
    return faces


def apply_blurred_background(frame, faces):
    """Sfoca pesantemente tutto il frame tranne le regioni in cui sono presenti i volti."""
    if len(faces) == 0:
        return frame  # Nessun volto? Nessuna sfocatura per evitare confusione

    # Crea la versione completamente sfocata del frame
    blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)

    # Crea una maschera nera delle stesse dimensioni del frame
    mask = frame.copy()
    mask[:] = 0

    # Disegna i rettangoli bianchi (pieni) sui volti rilevati nella maschera
    for (x, y, w, h) in faces:
        mask[y:y + h, x:x + w] = 255

    # Combina il frame nitido e quello sfocato usando la maschera
    output = frame.copy()
    # Dove la maschera è bianca (255) tieni il frame originale, altrove usa il blur
    output[mask == 0] = blurred_frame[mask == 0]
    return output