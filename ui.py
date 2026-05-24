import cv2

def draw_hud(frame, filter_name, face_count, fps, is_recording):
    """Disegna l'interfaccia utente (HUD) in overlay sul frame."""
    # Colore verde per il testo dell'HUD standard
    color = (0, 255, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2

    # Stringhe informative
    txt_filter = f"Filtro: {filter_name.upper()}"
    txt_faces = f"Volti: {face_count}"
    txt_fps = f"FPS: {int(fps)}"

    # Posizionamento testi nell'angolo in alto a sinistra
    cv2.putText(frame, txt_filter, (15, 30), font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.putText(frame, txt_faces, (15, 55), font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.putText(frame, txt_fps, (15, 80), font, font_scale, color, thickness, cv2.LINE_AA)

    # Indicatore di registrazione in alto a destra
    if is_recording:
        h, w = frame.shape[:2]
        # Cerchio rosso lampeggiante/fisso
        cv2.circle(frame, (w - 120, 30), 8, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (w - 100, 37), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)

    # Nota di comando rapida in basso
    cv2.putText(frame, "[Q]: Esci  [S]: Screenshot  [R]: Rec  [0-6]: Filtri",
                (15, frame.shape[0] - 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return frame