# Changelog

## [1.0.0] - 2026-02-03

### Vision

okitsok est finalisé comme **brique universelle** utilisable par des humains ET des IA :
- Outil local, non interactif, déterministe
- Sortie JSON strictement machine-readable
- Distribution en binaire standalone (aucune installation Python requise)
- Documentation complète pour intégrations multi-langages

### Fonctionnalités finalisées

- **Logique DNS robuste** : Vérification hiérarchique (NS → SOA → A → AAAA)
- **CLI stable** : Non interactive, sortie standardisée
- **Sortie JSON pure** : Aucun texte parasite, format garanti
- **Exit codes documentés** : Intégration facile dans scripts
- **Distribution standalone** : Binaires Windows/macOS/Linux avec PyInstaller

### Documentation

- **README restructuré** : Sections humain + IA
- **BUILD.md** : Instructions de génération des binaires
- **EXAMPLES.md** : Exemples d'intégration (Python, Node.js, Shell, Go, Rust)
- Exit codes et comportement déterministe documentés

### Technique

- Dépendance : `dnspython>=2.0.0` (incluse dans les binaires)
- Vérifications DNS parallèles (concurrent.futures)
- Fallback socket si dnspython absent
- Spec PyInstaller pour build multi-plateforme

### Philosophie (inchangée)

- **Indicateur technique** : Pas de certification, pas de garantie
- **Responsabilité** : Limites clairement documentées
- **Simplicité** : Outil fondamental, durable, universel
- **Transparence** : Ce que okitsok fait ET ne fait pas

### Statuts (standardisés)

- `available` : Aucun enregistrement DNS (NXDOMAIN)
- `taken` : Au moins un enregistrement DNS existe
- `unknown` : Impossible de déterminer (timeout, erreur)

### Exit codes

- `0` : Au moins un domaine disponible
- `1` : Aucun domaine disponible
- `130` : Interruption utilisateur
