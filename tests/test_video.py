import cv2
import sys

from src.video.video_tracker import HandController

def run_video_test(camera_index):
    print(f"\n--- Inizializzazione Webcam (Indice: {camera_index}) ---")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"❌ Errore: Impossibile aprire la fotocamera con indice {camera_index}.")
        return

    controller = HandController()
    print("Controlli Rilevati:")
    print("- Sposta la mano nel rettangolo per il movimento")
    print("- Pugno chiuso: PAUSA")
    print("- Punta Pollice + Indice: ATTACCO")
    print("- Seconda mano: SALTO")
    print("\nPremi 'q' sulla finestra video per uscire.")

    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Errore durante la cattura del frame.")
            break

        frame = cv2.flip(frame, 1)
        game_data, debug_frame = controller.process_frame(frame)

        # "Tappetino" di movimento
        h, w, _ = debug_frame.shape
        start_point = (int(w * 0.3), int(h * 0.3))
        end_point = (int(w * 0.7), int(h * 0.7))
        cv2.rectangle(debug_frame, start_point, end_point, (0, 255, 0), 2)

        # Overlay dati a schermo
        y_offset = 30
        status_text = [
            f"Mani rilevate: {game_data['hands_detected']}",
            f"Posizione X/Y: {game_data['x']:.2f}, {game_data['y']:.2f}",
            f"Pausa (Pugno): {game_data['is_paused']}",
            f"Attacco (Pinch): {game_data['is_attacking']}",
            f"Salto (Mano L): {game_data['is_jumping']}"
        ]

        for text in status_text:
            cv2.putText(debug_frame, text, (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 30

        cv2.imshow("Test Modulo Video - Voice & Vision", debug_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Test Video concluso correttamente.")

if __name__ == "__main__":
    target_camera = 0
    if len(sys.argv) > 1:
        try:
            target_camera = int(sys.argv[1])
        except ValueError:
            print("⚠️ Argomento camera non valido, uso 0.")

    run_video_test(target_camera)