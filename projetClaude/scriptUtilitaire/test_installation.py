"""
Script de test pour vérifier que l'installation est correcte
"""
import sys
import os

def test_imports():
    """Teste que tous les modules peuvent être importés"""
    print("🔍 Test des imports...")
    
    modules = [
        'pygame',
        'numpy',
        'ttkbootstrap',
        'constants',
        'config',
        'balle',
        'cercle',
        'carre',
        'common',
        'interaction',
        'note_sounds',
        'styleCercles',
        'styleApparence'
    ]
    
    failed = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed.append(module)
    
    return len(failed) == 0, failed


def test_files():
    """Teste que les fichiers nécessaires existent"""
    print("\n📁 Test des fichiers...")
    
    required_files = [
        'constants.py',
        'config.py',
        'balle.py',
        'cercle.py',
        'common.py',
        'interaction.py',
        'note_sounds.py',
        'styleCercles.py',
        'styleApparence.py',
        'jeu.py',
        'launcher.py',
        'requirements.txt',
        'config.json'
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (manquant)")
            missing.append(file)
    
    return len(missing) == 0, missing


def test_directories():
    """Teste que les dossiers nécessaires existent"""
    print("\n📂 Test des dossiers...")
    
    required_dirs = ['sounds', 'images', 'font/symbola']
    optional_dirs = ['frames', 'music']
    
    missing_required = []
    missing_optional = []
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"  ✅ {dir}")
        else:
            print(f"  ⚠️  {dir} (manquant - REQUIS)")
            missing_required.append(dir)
    
    for dir in optional_dirs:
        if os.path.exists(dir):
            print(f"  ✅ {dir}")
        else:
            print(f"  ℹ️  {dir} (manquant - optionnel)")
            missing_optional.append(dir)
    
    return len(missing_required) == 0, missing_required, missing_optional


def test_config():
    """Teste que la configuration est valide"""
    print("\n⚙️  Test de la configuration...")
    
    try:
        from sourceCode.config.config import GameConfig
        config = GameConfig()
        
        # Teste quelques propriétés
        assert config.timer > 0, "Timer doit être > 0"
        assert config.min_radius > 0, "Min radius doit être > 0"
        assert isinstance(config.cercles_color, list), "Cercles color doit être une liste"
        
        print("  ✅ Configuration valide")
        return True, None
    except Exception as e:
        print(f"  ❌ Erreur de configuration: {e}")
        return False, str(e)


def test_constants():
    """Teste que les constantes sont correctes"""
    print("\n🔢 Test des constantes...")
    
    try:
        import sourceCode.config.constants as C
        
        assert C.SCREEN_WIDTH > 0, "SCREEN_WIDTH doit être > 0"
        assert C.SCREEN_HEIGHT > 0, "SCREEN_HEIGHT doit être > 0"
        assert C.FPS > 0, "FPS doit être > 0"
        assert C.GRAVITY >= 0, "GRAVITY doit être >= 0"
        
        print("  ✅ Constantes valides")
        return True, None

    except Exception as e:
        print(f"  ❌ Erreur dans les constantes: {e}")
        return False, str(e)



def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("🎮 TEST D'INSTALLATION - TIKTOK BALL GAME v2.0")
    print("=" * 60)
    
    all_passed = True
    
    # Test des imports
    success, failed = test_imports()
    if not success:
        print(f"\n⚠️  Modules manquants: {', '.join(failed)}")
        print("   Installez-les avec: pip install -r requirements.txt")
        all_passed = False
    
    # Test des fichiers
    success, missing = test_files()
    if not success:
        print(f"\n⚠️  Fichiers manquants: {', '.join(missing)}")
        all_passed = False
    
    # Test des dossiers
    success, missing_req, missing_opt = test_directories()
    if not success:
        print(f"\n⚠️  Dossiers requis manquants: {', '.join(missing_req)}")
        print("   Créez-les avec: mkdir -p sounds images font/symbola")
        all_passed = False
    
    if missing_opt:
        print(f"\nℹ️  Dossiers optionnels manquants: {', '.join(missing_opt)}")
    
    # Test de la config
    success, error = test_config()
    if not success:
        all_passed = False
    
    # Test des constantes
    success, error = test_constants()
    if not success:
        all_passed = False
    
    # Résumé
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("\n🚀 Vous pouvez lancer le jeu avec:")
        print("   python launcher.py  (avec interface)")
        print("   python jeu.py       (sans interface)")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n🔧 Veuillez corriger les problèmes ci-dessus avant de lancer le jeu.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())