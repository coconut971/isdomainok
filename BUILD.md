# Guide de build - okitsok

Ce document explique comment créer les binaires standalone d'okitsok.

## Prérequis

```bash
pip install pyinstaller
```

## Build pour votre plateforme

```bash
pyinstaller okitsok.spec
```

Le binaire sera généré dans le dossier `dist/`.

## Résultats par plateforme

- **Windows** : `dist/okitsok.exe` (~10-15 MB)
- **macOS** : `dist/okitsok` (~10-15 MB)
- **Linux** : `dist/okitsok` (~10-15 MB)

## Test du binaire

```bash
# Windows
.\dist\okitsok.exe google

# macOS / Linux
./dist/okitsok google
```

## Build multi-plateforme

PyInstaller génère des binaires natifs pour la plateforme sur laquelle il est exécuté.

Pour créer des binaires pour plusieurs plateformes :

1. **Windows** : Exécutez le build sur Windows
2. **macOS** : Exécutez le build sur macOS
3. **Linux** : Exécutez le build sur Linux

Ou utilisez des solutions de CI/CD comme GitHub Actions.

## Notes

- Le binaire inclut Python et toutes les dépendances (dnspython)
- Aucune installation Python requise sur la machine cible
- Le binaire peut être distribué tel quel
- Taille approximative : 10-15 MB (compressé avec UPX)
