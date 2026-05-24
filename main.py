import cv2
import time
import os
from datetime import datetime

# Import dei moduli del progetto
import filters
import effects
import ui


def main():
    # Inizializzazione Webcam (ID 0 standard)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Errore: Impossibile accedere alla webcam.")
        return

    # Mappatura dei filtri associati ai tasti numerici
    filter_map = {
        ord('0'): 'Normale',
        ord('1'): 'Grigio',
        ord('2'): 'Negativo',
        ord('3'): 'Mappa Termica',
        ord('4'): 'Cartoon',
        ord('5'): 'Pixelate',
        ord('6'): 'Sfondo Sfocato (Face-Track)'
    }

    current_filter = 'Normale'
    mirror_mode = False

    # Variabili per il calcolo dei Real-time FPS
    prev_time = 0
    fps = 0

    # Configurazione VideoWriter (Registrazione)
    video_writer = None
    is_recording = False

    print("=== Webcam Real-Time Filters avviata ===")
    print("Controlli: 0-6 per i filtri | M: Mirror | S: Screenshot | R: Registra | Q: Esci")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Errore nella ricezione del frame dalla webcam.")
            break

        # Calcolo dinamico degli FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time

        # Applica l'effetto specchio se attivo prima di elaborare o salvare
        if mirror_mode:
            frame = filters.apply_mirror(frame)

        # Rilevamento facce (necessario sia per l'HUD che per lo sfondo sfocato)
        faces = effects.detect_faces(frame)
        face_count = len(faces)

        # Pipeline di elaborazione in base al filtro selezionato
        processed_frame = frame.copy()

        if current_filter == 'Grigio':
            processed_frame = filters.apply_grayscale(processed_frame)
        elif current_filter == 'Negativo':
            processed_frame = filters.apply_negative(processed_frame)
        elif current_filter == 'Mappa Termica':
            processed_frame = filters.apply_heatmap(processed_frame)
        elif current_filter == 'Cartoon':
            processed_frame = filters.apply_cartoon(processed_frame)
        elif current_filter == 'Pixelate':
            processed_frame = filters.apply_pixelate(processed_frame)
        elif current_filter == 'Sfondo Sfocato (Face-Track)':
            processed_frame = effects.apply_blurred_background(processed_frame, faces)

        # Scrittura dei flussi video su file se la registrazione è attiva (PRIMA dell'HUD per pulizia video)
        if is_recording and video_writer is not None:
            video_writer.write(processed_frame)

        # Generazione dell'HUD grafico a schermo
        display_frame = ui.draw_hud(processed_frame.copy(), current_filter, face_count, fps, is_recording)

        # Mostra il risultato nella finestra
        cv2.imshow("Webcam Real-Time Filters", display_frame)

        # Intercettazione input da tastiera
        key = cv2.waitKey(1) & 0xFF

        # Gestione Uscita Pulita
        if key == ord('q') or key == ord('Q'):
            break

        # Cambio Filtro
        if key in filter_map:
            current_filter = filter_map[key]

        # Toggle Mirror Mode
        if key == ord('m') or key == ord('M'):
            mirror_mode = not mirror_mode

        # Cattura Screenshot (Salva l'immagine elaborata SENZA HUD per scopi di pulizia, modificabile a piacimento)
        if key == ord('s') or key == ord('S'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, processed_frame)
            print(f"[*] Screenshot salvato correttamente come: {filename}")

        # Gestione Avvio/Arresto Registrazione Video (.mp4)
        if key == ord('r') or key == ord('R'):
            if not is_recording:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_filename = f"output_{timestamp}.mp4"
                height, width = processed_frame.shape[:2]

                # Codec universale H.264 / MP4
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(video_filename, fourcc, max(15, int(fps)), (width, height))
                is_recording = True
                print(f"[+] Registrazione avviata: {video_filename}")
            else:
                is_recording = False
                if video_writer is not None:
                    video_writer.release()
                    video_writer = None
                print("[-] Registrazione interrotta e salvata.")

    # Rilascio definitivo e pulito delle risorse hardware e software
    cap.release()
    if video_writer is not None:
        video_writer.release()
    cv2.destroyAllWindows()
    print("=== Applicazione terminata in modo pulito ===")


if __name__ == "__main__":
    main()