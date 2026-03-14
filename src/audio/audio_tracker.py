import sounddevice as sd
import numpy as np

class AudioController:
    def __init__(self, silence_threshold=0.015, max_volume=0.15):
        """
        silence_threshold: Sotto questo valore di volume, la velocità è 0.
        max_volume: A questo valore (o superiore), la velocità è al 100%.
        """
        self.silence_threshold = silence_threshold
        self.max_volume = max_volume
        self.current_volume = 0.0
        
        # Mono (channels=1), campionamento standard
        self.stream = sd.InputStream(channels=1, callback=self._audio_callback)

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
            
        # Volume tramite RMS (Root Mean Square)
        rms = np.sqrt(np.mean(indata**2))
        self.current_volume = rms

    def get_speed_multiplier(self):
        """
        Return: tra 0.0 (silenzio) e 1.0 (volume massimo/superiore)
        """
        if self.current_volume < self.silence_threshold:
            return 0.0
            
        # Calcolo velocità
        speed = (self.current_volume - self.silence_threshold) / (self.max_volume - self.silence_threshold)
        
        # valore compreso tra 0.0 e 1.0
        return max(0.0, min(speed, 1.0))