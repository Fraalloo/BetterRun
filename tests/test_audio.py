import time
from src.audio.audio_tracker import AudioController

def main():
    print("Inizializzazione microfono")
    
    audio = AudioController(silence_threshold=0.015, max_volume=0.15)
    audio.start()
    
    print("Microfono in ascolto! Parla o fai rumore.")
    print("Premi Ctrl+C nel terminale per uscire.\n")
    
    try:
        while True:
            speed = audio.get_speed_multiplier()
            
            # Barra dell'audio
            bar_length = 40
            filled = int(speed * bar_length)
            bar = '█' * filled + '-' * (bar_length - filled)
            
            # Usiamo \r per sovrascrivere la stessa riga nel terminale
            print(f"\rVelocità: [{bar}] {speed*100:05.1f}%", end="")
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\n\nUscita in corso...")
    finally:
        audio.stop()
        print("Microfono spento.")

if __name__ == "__main__":
    main()