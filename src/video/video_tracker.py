import cv2
import mediapipe as mp
import math

class HandController:
    """
    pinch_threshold: Soglia per riconoscere l'attacco (pinch).
    MediaPipe per tracciare fino a 2 mani
    """
    def __init__(self, pinch_threshold=0.05):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.85, 
            min_tracking_confidence=0.85
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.pinch_threshold = pinch_threshold

    def is_fist(self, hand_landmarks):
        wrist = hand_landmarks.landmark[0] # Polso
        tips = [8, 12, 16, 20]             # Punte di Indice, Medio, Anulare, Mignolo
        mcps = [5, 9, 13, 17]              # Nocche di base delle stesse dita
        
        curled_fingers = 0
        for tip_idx, mcp_idx in zip(tips, mcps):
            tip = hand_landmarks.landmark[tip_idx]
            mcp = hand_landmarks.landmark[mcp_idx]
            
            dist_tip = math.hypot(tip.x - wrist.x, tip.y - wrist.y)
            dist_mcp = math.hypot(mcp.x - wrist.x, mcp.y - wrist.y)
            
            # Se la punta è più vicina al polso rispetto alla nocca, il dito è piegato
            if dist_tip < dist_mcp:
                curled_fingers += 1
                
        # Se almeno 3 sono piegate, lo consideriamo un pugno
        return curled_fingers >= 3

    def process_frame(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        game_data = {
            "x": 0.5,
            "y": 0.5,
            "is_attacking": False,
            "is_jumping": False,
            "is_paused": False,
            "hands_detected": 0
        }

        if results.multi_hand_landmarks and results.multi_handedness:
            game_data["hands_detected"] = len(results.multi_hand_landmarks)
            
            main_hand = None
            
            for idx, hand_info in enumerate(results.multi_handedness):
                hand_label = hand_info.classification[0].label 
                
                if hand_label == "Right": # Mano Destra (Movimento/Azioni)
                    main_hand = results.multi_hand_landmarks[idx]
                
                if hand_label == "Left":  # Mano Sinistra (Salto)
                    game_data["is_jumping"] = True
            
            if game_data["hands_detected"] == 2:
                game_data["is_jumping"] = True

            if main_hand:
                game_data["x"] = main_hand.landmark[9].x # Nocca centrale
                game_data["y"] = main_hand.landmark[9].y

                # Controllo Pausa (Pugno)
                if self.is_fist(main_hand):
                    game_data["is_paused"] = True
                else:
                    # Controllo attacco solo se non è in pausa
                    thumb_tip = main_hand.landmark[4]
                    index_tip = main_hand.landmark[8]
                    distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
                    if distance < self.pinch_threshold:
                        game_data["is_attacking"] = True

                self.mp_draw.draw_landmarks(frame, main_hand, self.mp_hands.HAND_CONNECTIONS)

        return game_data, frame