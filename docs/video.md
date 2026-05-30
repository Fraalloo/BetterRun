# Video

Il modulo video si trova in `src/video/video_tracker.py` e fornisce la classe `HandController`, responsabile del tracciamento delle mani tramite OpenCV e MediaPipe.

## Dipendenze

Il modulo usa:

- `opencv-python` (`cv2`) per conversione colore, acquisizione e disegno dei frame.
- `mediapipe` per il riconoscimento dei landmark delle mani.
- `math` per il calcolo delle distanze tra landmark.

## `HandController`

```python
from src.video.video_tracker import HandController

controller = HandController(pinch_threshold=0.05)
game_data, frame = controller.process_frame(frame)
```

### Parametri

| Parametro | Default | Descrizione |
| --- | ---: | --- |
| `pinch_threshold` | `0.05` | Distanza massima tra punta del pollice e punta dell'indice per riconoscere l'attacco. |

All'inizializzazione, MediaPipe viene configurato con:

- `static_image_mode=False`
- `max_num_hands=2`
- `min_detection_confidence=0.85`
- `min_tracking_confidence=0.85`

## Output di `process_frame`

`process_frame(frame)` riceve un frame OpenCV in formato BGR, lo converte in RGB per MediaPipe e restituisce una tupla:

```python
game_data, frame = controller.process_frame(frame)
```

`game_data` contiene:

| Chiave | Tipo | Default | Significato |
| --- | --- | --- | --- |
| `x` | `float` | `0.5` | Coordinata X normalizzata della mano principale. |
| `y` | `float` | `0.5` | Coordinata Y normalizzata della mano principale. |
| `is_attacking` | `bool` | `False` | `True` quando pollice e indice della mano destra sono abbastanza vicini. |
| `is_jumping` | `bool` | `False` | `True` quando viene rilevata la mano sinistra o quando sono rilevate due mani. |
| `is_paused` | `bool` | `False` | `True` quando la mano destra e' riconosciuta come pugno. |
| `hands_detected` | `int` | `0` | Numero di mani rilevate nel frame. |

Il frame restituito e' lo stesso frame in ingresso, con i landmark della mano principale disegnati quando disponibili.

## Mappatura dei gesti

| Gesto | Condizione nel codice | Azione |
| --- | --- | --- |
| Mano destra aperta | Presenza di una mano con label MediaPipe `Right` | Movimento tramite landmark `9`, la nocca centrale. |
| Pinch | Distanza tra landmark `4` e `8` minore di `pinch_threshold` | Attacco. |
| Pugno | Almeno 3 dita hanno la punta piu' vicina al polso della nocca base | Pausa. |
| Mano sinistra | Presenza di una mano con label `Left` | Salto. |

Quando viene riconosciuto il pugno, l'attacco non viene valutato nello stesso frame.
