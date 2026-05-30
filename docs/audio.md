# Audio

Il modulo audio si trova in `src/audio/audio_tracker.py` e fornisce la classe `AudioController`, usata per trasformare il volume del microfono in un moltiplicatore di velocita' tra `0.0` e `1.0`.

## Dipendenze

Il modulo usa:

- `sounddevice` per leggere l'input del microfono.
- `numpy` per calcolare il volume RMS del buffer audio.

## `AudioController`

```python
from src.audio.audio_tracker import AudioController

audio = AudioController(silence_threshold=0.015, max_volume=0.15)
audio.start()
speed = audio.get_speed_multiplier()
audio.stop()
```

### Parametri

| Parametro | Default | Descrizione |
| --- | ---: | --- |
| `silence_threshold` | `0.015` | Sotto questa soglia il volume viene considerato silenzio e la velocita' restituita e' `0.0`. |
| `max_volume` | `0.15` | A questo volume, o sopra, la velocita' restituita arriva a `1.0`. |

All'inizializzazione viene creato uno stream di input mono:

```python
sd.InputStream(channels=1, callback=self._audio_callback)
```

## Flusso di funzionamento

1. `start()` avvia lo stream del microfono.
2. `_audio_callback(...)` riceve i campioni audio e calcola il volume RMS:

   ```python
   rms = np.sqrt(np.mean(indata**2))
   ```

3. Il valore RMS viene salvato in `current_volume`.
4. `get_speed_multiplier()` converte `current_volume` in un valore normalizzato.
5. `stop()` ferma e chiude lo stream.

## Calcolo della velocita'

Se `current_volume < silence_threshold`, il risultato e' `0.0`.

Altrimenti viene applicata questa formula:

```python
speed = (current_volume - silence_threshold) / (max_volume - silence_threshold)
```

Il valore finale viene limitato tra `0.0` e `1.0`.
