import os
import sys
import subprocess

def main():
    tests_dir = "tests"
    if not os.path.isdir(tests_dir):
        print(f"❌ Errore: La cartella '{tests_dir}' non esiste.")
        return

    # Lista di tutti gli script di test
    test_files = [f for f in os.listdir(tests_dir) if f.endswith('.py') and f != '__init__.py']
    test_files.sort()

    if not test_files:
        print(f"⚠️ Nessuno script trovato in '{tests_dir}'.")
        return

    print("\n" + "="*50)
    print(" 🧪 TEST RUNNER CLI")
    print("="*50)
    
    for i, file_name in enumerate(test_files):
        print(f" [{i + 1}] {file_name}")
    print(" [0] Esci")
    print("="*50)

    while True:
        try:
            user_input = input("\nScegli il test da avviare: ").strip()
            if user_input == '0':
                print("👋 Uscita.")
                break
            
            choice = int(user_input)
            if 1 <= choice <= len(test_files):
                selected_file = test_files[choice - 1]
                script_path = os.path.join(tests_dir, selected_file)
                
                # Argomenti base del subprocess
                cmd_args = [sys.executable, script_path]

                # Argomenti specifici del subprocess
                if "video" in selected_file.lower():
                    cam_idx = input("👉 Inserisci l'indice della fotocamera [Default 0]: ").strip()
                    if cam_idx == "":
                        cam_idx = "0"
                    cmd_args.append(cam_idx)

                print(f"\n🚀 Esecuzione: {' '.join(cmd_args)}")
                print("-" * 50)
                
                # Configurazione ambiente di test
                env = os.environ.copy()
                env["PYTHONPATH"] = os.getcwd()

                try:
                    subprocess.run(cmd_args, env=env, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"\n❌ Lo script è terminato con un errore (Exit Code: {e.returncode})")
                except KeyboardInterrupt:
                    print("\n🛑 Test interrotto dall'utente.")

                print("-" * 50)
                
                again = input("Vuoi eseguire un altro test? (s/n): ").lower().strip()
                if again != 's':
                    break
                
                print("\n" + "="*50)
                for i, file_name in enumerate(test_files):
                    print(f" [{i + 1}] {file_name}")
                print(" [0] Esci")
                print("="*50)

            else:
                print("❌ Numero non valido.")
        except ValueError:
            print("❌ Per favore, inserisci un numero.")

if __name__ == "__main__":
    main()