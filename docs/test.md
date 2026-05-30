# Test

La cartella `tests` contiene test manuali e demo integrative per verificare i tre blocchi principali del progetto: video, audio e meccaniche di gioco.

## `tests/test_video.py`

Avvia una finestra OpenCV per controllare il tracciamento della mano tramite `HandController`.

Comando:

```bash
python tests/test_video.py
```

Con indice camera esplicito:

```bash
python tests/test_video.py 1
```

Controlli verificati:

| Input | Risultato atteso |
| --- | --- |
| Mano destra nel frame | Aggiornamento coordinate `x` e `y`. |
| Pugno con mano destra | `is_paused=True`. |
| Pinch pollice-indice | `is_attacking=True`. |
| Mano sinistra o due mani | `is_jumping=True`. |
| Tasto `q` | Chiusura del test. |

La finestra mostra overlay con numero di mani rilevate, posizione, pausa, attacco e salto.

## `tests/test_audio.py`

Avvia il microfono tramite `AudioController` e stampa una barra testuale che rappresenta il moltiplicatore di velocita'.

Comando:

```bash
python tests/test_audio.py
```

Comportamento atteso:

- sotto `silence_threshold=0.015`, la velocita' resta a `0.0`;
- aumentando il volume, la barra si riempie;
- a `max_volume=0.15` o oltre, la velocita' raggiunge il `100%`;
- `Ctrl+C` ferma il test e chiude lo stream audio.

## `tests/test_gui.py`

Esegue una demo Pygame autonoma delle meccaniche di gioco, usando mouse e tastiera al posto dei controller reali.

Comando:

```bash
python tests/test_gui.py
```

Controlli:

| Input | Azione simulata |
| --- | --- |
| Movimento mouse | Movimento del giocatore. |
| Click sinistro | Attacco/proiettile. |
| Barra spaziatrice | Salto temporaneo. |
| `W` | Aumenta il volume voce simulato. |
| `S` | Diminuisce il volume voce simulato. |
| Chiusura finestra | Termina la demo. |

Meccaniche coperte:

- il giocatore segue il mouse e resta nei limiti dello schermo;
- il salto rende temporaneamente invulnerabili;
- il click genera proiettili con cooldown;
- i nemici scendono piu' velocemente quando aumenta il volume simulato;
- il punteggio cresce con sopravvivenza, schivate e nemici distrutti;
- la collisione giocatore-nemico termina la partita se il giocatore non sta saltando.
