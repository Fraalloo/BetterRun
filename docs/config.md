# Configurazione

La configurazione del progetto e' raccolta in `src/config` ed espone costanti semplici da importare negli altri moduli.

## `src/config/config.py`

Contiene le impostazioni base della finestra di gioco:

| Costante | Valore | Descrizione |
| --- | ---: | --- |
| `WIDTH` | `1280` | Larghezza della finestra o superficie di gioco. |
| `HEIGHT` | `720` | Altezza della finestra o superficie di gioco. |
| `FPS` | `60` | Frame al secondo target per il game loop. |

Esempio d'uso:

```python
from src.config.config import WIDTH, HEIGHT, FPS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock.tick(FPS)
```

## `src/config/colors.py`

Definisce una palette RGB condivisa:

| Costante | Valore RGB | Uso suggerito |
| --- | --- | --- |
| `WHITE` | `(255, 255, 255)` | Testo e elementi chiari. |
| `BLACK` | `(0, 0, 0)` | Sfondo o testo scuro. |
| `RED` | `(255, 50, 50)` | Nemici, errori o pericoli. |
| `GREEN` | `(50, 255, 50)` | Proiettili, conferme o indicatori positivi. |
| `BLUE` | `(50, 150, 255)` | Giocatore o elementi principali. |
| `YELLOW` | `(255, 255, 0)` | Salto, warning o stato speciale. |
| `DARK_GRAY` | `(40, 40, 40)` | Sfondo scuro neutro. |

Esempio d'uso:

```python
from src.config.colors import BLUE, YELLOW

pygame.draw.circle(surface, BLUE, (x, y), radius)
```
