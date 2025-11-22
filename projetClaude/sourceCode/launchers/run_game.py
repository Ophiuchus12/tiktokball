#!/usr/bin/env python3

import sys
from pathlib import Path

# Ajoute sourceCode/ au PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


import os
import sys
import subprocess

# Fix imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

def main():
    print("=" * 60)
    print("🎮 TikTok Ball Game v2.0 - Launcher")
    print("=" * 60)
    print()
    
    print("Choisissez le mode de lancement:")
    print("  1. Interface de configuration (launcher.py)")
    print("  2. Lancer directement le jeu (jeu.py)")
    print("  3. Quitter")
    print()
    
    choice = input("Votre choix (1/2/3): ").strip()
    
    launcher_path = os.path.join(current_dir, "launcher.py")
    jeu_path = os.path.join(current_dir, "jeu.py")
    
    if choice == "1":
        print("\n🚀 Lancement de l'interface de configuration...")
        os.chdir(project_root)
        subprocess.run([sys.executable, launcher_path])
    elif choice == "2":
        print("\n🚀 Lancement direct du jeu...")
        os.chdir(project_root)
        subprocess.run([sys.executable, jeu_path])
    elif choice == "3":
        print("\n👋 À bientôt!")
        return 0
    else:
        print("❌ Choix invalide")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt du launcher")
        sys.exit(0)