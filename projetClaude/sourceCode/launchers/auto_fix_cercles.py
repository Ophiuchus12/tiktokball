#!/usr/bin/env python3
"""
Script d'auto-correction pour le problème des cercles invisibles
Applique automatiquement le patch au fichier jeu.py
"""
import os
import sys
import shutil
from pathlib import Path


def find_jeu_py():
    """Trouve le fichier jeu.py"""
    possible_paths = [
        "sourceCode/launchers/jeu.py",
        "launchers/jeu.py",
        "jeu.py",
        "../jeu.py",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def backup_file(filepath):
    """Crée une sauvegarde du fichier"""
    backup_path = filepath + ".backup"
    shutil.copy2(filepath, backup_path)
    print(f"✅ Sauvegarde créée: {backup_path}")
    return backup_path


def apply_patch(filepath):
    """Applique le patch au fichier jeu.py"""
    
    print(f"\n📝 Lecture de {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patch 1 : Forcer couleur blanche après création des cercles
    patch1 = """
        # ⭐ AUTO-PATCH: Forcer couleur visible
        print(f"🔍 DEBUG: {len(self.cercles)} cercles créés")
        for i, cercle in enumerate(self.cercles[:5]):
            print(f"  Cercle {i}: pos=({cercle.x:.0f},{cercle.y:.0f}), r={cercle.rayon:.0f}, color={cercle.color}")
            cercle.color = (255, 255, 255)  # Forcer blanc
        if len(self.cercles) > 5:
            for cercle in self.cercles[5:]:
                cercle.color = (255, 255, 255)
        print("  → Tous les cercles forcés en BLANC")
        # ⭐ FIN AUTO-PATCH
"""
    
    # Chercher où insérer le patch
    # Après la ligne qui contient "chooseStyleGame" ou "self.cercles ="
    lines = content.split('\n')
    patched_lines = []
    patch_applied = False
    
    for i, line in enumerate(lines):
        patched_lines.append(line)
        
        # Détecter la création des cercles
        if not patch_applied and ('chooseStyleGame' in line or 
                                   ('self.cercles' in line and '=' in line)):
            # Vérifier que le patch n'est pas déjà là
            if i + 1 < len(lines) and 'AUTO-PATCH' not in lines[i + 1]:
                # Ajouter le patch avec l'indentation appropriée
                indent = len(line) - len(line.lstrip())
                indented_patch = '\n'.join(' ' * indent + l for l in patch1.strip().split('\n'))
                patched_lines.append(indented_patch)
                patch_applied = True
                print(f"✅ Patch appliqué après la ligne {i+1}")
    
    if not patch_applied:
        print("⚠️  Impossible de trouver où appliquer le patch automatiquement")
        print("   Vous devrez l'appliquer manuellement")
        return False
    
    # Écrire le fichier patché
    patched_content = '\n'.join(patched_lines)
    
    print(f"\n💾 Écriture du fichier patché...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patched_content)
    
    print(f"✅ Patch appliqué avec succès!")
    return True


def main():
    """Point d'entrée"""
    print("="*60)
    print("🔧 AUTO-PATCH - Correction Cercles Invisibles")
    print("="*60)
    print()
    
    # Trouver jeu.py
    jeu_path = find_jeu_py()
    
    if jeu_path is None:
        print("❌ Impossible de trouver jeu.py")
        print("\n💡 Exécutez ce script depuis:")
        print("   - La racine du projet")
        print("   - Le dossier launchers/")
        print("   - Le dossier contenant jeu.py")
        return 1
    
    print(f"📂 Fichier trouvé: {jeu_path}")
    print()
    
    # Créer backup
    backup_path = backup_file(jeu_path)
    
    # Appliquer patch
    success = apply_patch(jeu_path)
    
    if success:
        print()
        print("="*60)
        print("✅ PATCH APPLIQUÉ AVEC SUCCÈS")
        print("="*60)
        print()
        print("🚀 Testez maintenant:")
        print(f"   python3 {jeu_path}")
        print()
        print("📝 Les cercles devraient maintenant être BLANCS et VISIBLES")
        print()
        print("💡 Si vous voulez annuler:")
        print(f"   cp {backup_path} {jeu_path}")
        print()
        return 0
    else:
        print()
        print("="*60)
        print("⚠️  PATCH NON APPLIQUÉ")
        print("="*60)
        print()
        print("💡 Appliquez manuellement le patch:")
        print()
        print("Dans jeu.py, après la ligne qui crée self.cercles, ajoutez:")
        print()
        print("""
    for cercle in self.cercles:
        cercle.color = (255, 255, 255)  # Blanc
        """)
        print()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Annulé")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)