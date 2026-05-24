import cv2
import numpy as np


def apply_grayscale(frame):
    """Converte il frame in scala di grigi mantenendo i 3 canali BGR."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_negative(frame):
    """Inverte i colori del frame (effetto negativo)."""
    return cv2.bitwise_not(frame)


def apply_heatmap(frame):
    """Applica un effetto mappa termica usando la colormap JET."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return heatmap


def apply_cartoon(frame):
    """Semplifica i colori con un filtro bilaterale e sovrappone i bordi Canny."""
    # Riduce i dettagli mantenendo i bordi netti
    color = frame.copy()
    for _ in range(2):
        color = cv2.bilateralFilter(color, d=9, sigmaColor=9, sigmaSpace=7)

    # Rilevamento dei bordi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 5)
    edges = cv2.Canny(gray_blur, 50, 150)

    # Inverte i bordi (da bianchi su nero a neri su bianco)
    edges_inv = cv2.bitwise_not(edges)
    edges_bgr = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # Combina l'immagine stilizzata con i bordi neri
    cartoon = cv2.bitwise_and(color, edges_bgr)
    return cartoon


def apply_pixelate(frame, pixel_size=16):
    """Riduce la risoluzione del frame e la riespande per un effetto pixel-art."""
    h, w = frame.shape[:2]
    # Ridimensionamento verso il basso
    temp = cv2.resize(frame, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    # Riporto alla dimensione originale senza smoothing (NEAREST)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)


def apply_mirror(frame):
    """Capovolge l'immagine orizzontalmente (Modalità Selfie)."""
    return cv2.flip(frame, 1)