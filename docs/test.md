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
