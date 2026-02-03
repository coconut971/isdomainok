# okitsok 1.0.0 - Pret pour publication

## Fichiers mis a jour avec coconut971

- ai-tool.yaml (3 URLs)
- okitsok.tool.json (3 URLs)
- TOOLS.md (1 URL)
- PUBLISH.md (2 URLs)
- pyproject.toml (2 URLs)

## Commandes de publication (copier-coller)

```bash
# Verification finale
py -m okitsok.cli example --json

# Commit et tag
git add .
git commit -m "Release 1.0.0"
git tag -a v1.0.0 -m "okitsok 1.0.0 - Stable release"
git push origin main --tags
```

## GitHub Release

URL directe : https://github.com/coconut971/okitsok/releases/new

1. Tag : v1.0.0
2. Titre : okitsok 1.0.0
3. Description : Copier le contenu de RELEASE.md
4. Upload : dist/okitsok.exe
5. Cocher "Set as the latest release"
6. Publier

## URLs finales apres publication

- Repository : https://github.com/coconut971/okitsok
- Release : https://github.com/coconut971/okitsok/releases/tag/v1.0.0
- Binary Windows : https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe

## Test post-publication

```bash
# Telecharger et tester
curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe -o test-okitsok.exe
.\test-okitsok.exe google --json
```

## Temps estime : 20 minutes

okitsok existera officiellement des que le tag v1.0.0 sera pushe et la release creee.
