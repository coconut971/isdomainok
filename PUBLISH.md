# Checklist de publication okitsok 1.0.0

## Etape 1 : Remplacer OWNER par votre GitHub username

Fichiers a modifier :
- `ai-tool.yaml` (3 occurrences)
- `okitsok.tool.json` (3 occurrences)

Remplacer `OWNER` par votre username GitHub reel.

## Etape 2 : Verifier que tout fonctionne

```bash
# Test du binaire
.\dist\okitsok.exe google --json

# Test du module Python
py -m okitsok.cli example --json
```

## Etape 3 : Commit final

```bash
git add .
git commit -m "Release 1.0.0"
git tag -a v1.0.0 -m "okitsok 1.0.0 - Stable release"
git push origin main --tags
```

## Etape 4 : Creer la GitHub Release

1. Aller sur https://github.com/coconut971/okitsok/releases/new
2. Choisir le tag : v1.0.0
3. Titre : okitsok 1.0.0
4. Description : Copier le contenu de RELEASE.md
5. Upload des binaires :
   - okitsok.exe (Windows) - deja pret dans dist/
   - okitsok (macOS) - a generer sur macOS
   - okitsok (Linux) - a generer sur Linux
6. Cocher "Set as the latest release"
7. Publier

## Etape 5 : Verification post-publication

Tester que les URLs dans ai-tool.yaml fonctionnent :

```bash
# Windows
curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe -o okitsok.exe

# macOS/Linux
curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok -o okitsok
chmod +x okitsok
```

## Optionnel : Publication sur PyPI

Si vous voulez publier sur PyPI :

```bash
py -m build
py -m twine upload dist/*.tar.gz dist/*.whl
```

Note : Necessita un compte PyPI et la configuration de twine.

## Apres publication

okitsok existe officiellement des que :
- Le tag v1.0.0 est pushe
- La release GitHub est creee
- Le binaire Windows est telechargeable

Les agents et frameworks peuvent alors :
1. Lire ai-tool.yaml
2. Telecharger le binaire
3. Utiliser okitsok automatiquement

## Temps estime

- Etapes 1-3 : 5 minutes
- Etape 4 : 10 minutes
- Verification : 5 minutes

Total : 20 minutes (sans la generation des binaires macOS/Linux)
