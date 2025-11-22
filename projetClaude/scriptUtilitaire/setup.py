#!/usr/bin/env python3
"""
Script d'installation automatique pour TikTok Ball Game v2.0
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Affiche un en-tête formaté"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_step(step_num, text):
    """Affiche une étape"""
    print(f"\n[{step_num}] {text}")


def run_command(cmd, description, required=True):
    """Exécute une commande shell"""
    print(f"  → {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {description} réussi")
            return True
        else:
            print(f"  ❌ {description} échoué")
            if result.stderr:
                print(f"     Erreur: {result.stderr[:200]}")
            if required:
                return False
            return True
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        if required:
            return False
        return True


def create_directory(path, description):
    """Crée un répertoire"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Dossier {path} créé")
        return True
    except Exception as e:
        print(f"  ❌ Impossible de créer {path}: {e}")
        return False


def create_dummy_sound():
    """Crée un fichier son minimal pour les tests"""
    try:
        import wave
        import struct
        
        sound_path = "sounds/a.wav"
        print(f"  → Création d'un son de test...")
        
        # Paramètres
        sample_rate = 44100
        duration = 0.1  # 100ms
        frequency = 440  # La (A4)
        
        # Génère une onde sinusoïdale
        num_samples = int(sample_rate * duration)
        
        with wave.open(sound_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                value = int(32767.0 * 0.3 * 
                          __import__('math').sin(2.0 * __import__('math').pi * frequency * i / sample_rate))
                wav_file.writeframes(struct.pack('h', value))
        
        print(f"  ✅ Son de test créé")
        return True
    except Exception as e:
        print(f"  ⚠️  Impossible de créer le son: {e}")
        print(f"     Veuillez ajouter manuellement un fichier a.wav dans sounds/")
        return False


def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} détecté")
        print(f"     Python 3.8+ requis")
        return False


def download_font():
    """Instructions pour télécharger la police"""
    print("\n  📝 POLICE REQUISE")
    print("     La police Symbola est nécessaire pour l'affichage.")
    print()
    print("     Option 1: Télécharger Symbola")
    print("     → https://fontlibrary.org/en/font/symbola")
    print("     → Placez Symbola.ttf dans font/symbola/")
    print()
    print("     Option 2: Utiliser une police système")
    print("     → Modifiez constants.py ligne 31:")
    print("       FONT_PATH = None")
    print("     → Et styleApparence.py ligne 7:")
    print("       font = pygame.font.Font(None, FONT_SIZE)")
    print()
    
    response = input("  Appuyez sur Entrée pour continuer...")


def create_sample_image():
    """Crée une image de fond simple"""
    try:
        from PIL import Image
        
        img_path = "images/noir.jpg"
        if os.path.exists(img_path):
            print(f"  ✅ Image de fond déjà présente")
            return True
        
        print(f"  → Création d'une image de fond simple...")
        
        # Crée une image noire simple
        img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
        img.save(img_path)
        
        print(f"  ✅ Image de fond créée")
        return True
    except ImportError:
        print(f"  ⚠️  PIL/Pillow non installé")
        print(f"     Veuillez ajouter manuellement une image etoile.jpeg dans images/")
        return False
    except Exception as e:
        print(f"  ⚠️  Impossible de créer l'image: {e}")
        return False


def main():
    """Installation principale"""
    print_header("🎮 INSTALLATION - TIKTOK BALL GAME v2.0")
    
    print("\nCe script va:")
    print("  1. Vérifier Python")
    print("  2. Installer les dépendances")
    print("  3. Créer les dossiers nécessaires")
    print("  4. Créer des ressources de test")
    print("  5. Tester l'installation")
    
    response = input("\nContinuer? (o/n): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("Installation annulée.")
        return 1
    
    # Étape 1: Vérifier Python
    print_step(1, "Vérification de Python")
    if not check_python_version():
        print("\n❌ Version de Python incompatible")
        return 1
    
    # Étape 2: Installer les dépendances
    print_step(2, "Installation des dépendances")
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installation des packages Python"
    ):
        print("\n⚠️  Certains packages n'ont pas pu être installés")
        print("   Vous pouvez réessayer avec: pip install -r requirements.txt")
    
    # Étape 3: Créer les dossiers
    print_step(3, "Création des dossiers")
    directories = [
        ("sounds", "Sons"),
        ("images", "Images"),
        ("font/symbola", "Polices"),
        ("frames", "Frames (optionnel)"),
        ("music", "Musique (optionnel)")
    ]
    
    for dir_path, desc in directories:
        create_directory(dir_path, desc)
    
    # Étape 4: Créer des ressources de test
    print_step(4, "Création des ressources de test")
    create_dummy_sound()
    create_sample_image()
    
    # Info sur la police
    download_font()
    
    # Étape 5: Test de l'installation
    print_step(5, "Test de l'installation")
    print("\n  Lancement du script de test...")
    
    try:
        result = subprocess.run([sys.executable, "test_installation.py"], 
                              capture_output=False)
        test_passed = result.returncode == 0
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {e}")
        test_passed = False
    
    # Résumé
    print_header("📋 RÉSUMÉ DE L'INSTALLATION")
    
    if test_passed:
        print("\n✅ Installation réussie!")
        print("\n🚀 Prochaines étapes:")
        print("   1. Ajoutez une vraie police dans font/symbola/Symbola.ttf")
        print("      (ou configurez une police système)")
        print("   2. Ajoutez de vrais sons dans sounds/")
        print("   3. Ajoutez des images de fond dans images/")
        print()
        print("   Puis lancez le jeu:")
        print("   → python launcher.py  (avec interface)")
        print("   → python jeu.py       (direct)")
        print()
        print("📚 Consultez QUICKSTART.md pour plus d'informations")
    else:
        print("\n⚠️  Installation incomplète")
        print("\n🔧 Actions nécessaires:")
        print("   1. Vérifiez les erreurs ci-dessus")
        print("   2. Corrigez les problèmes")
        print("   3. Relancez: python setup.py")
        print()
        print("   Ou consultez QUICKSTART.md pour une installation manuelle")
    
    print("\n" + "=" * 60)
    return 0 if test_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation interrompue par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)