# okitsok 1.0.0 - Release Notes

## Vue d'ensemble

okitsok 1.0.0 est la première version stable de cet outil de vérification de disponibilité de noms de domaine via DNS.

## Qu'est-ce que okitsok ?

okitsok est un **indicateur technique** qui interroge les serveurs DNS pour déterminer si un nom de domaine possède des enregistrements DNS actifs. C'est un outil :

- **Local** : Aucun service web, aucune API externe
- **Simple** : Une seule commande, sortie claire
- **Universel** : Utilisable par des humains, des scripts et des IA
- **Fiable** : Pas de dépendance à des services tiers

## Nouveautés de la version 1.0.0

### Distribution standalone

- **Binaires autonomes** pour Windows, macOS et Linux
- Aucune installation Python requise
- Taille : ~9-10 MB (incluant Python et dépendances)
- Prêt à l'emploi, zero-configuration

### CLI standardisée

- Commande simple : `okitsok example`
- Sortie JSON pure pour les scripts : `okitsok example --json`
- Exit codes documentés pour intégration dans des workflows
- Non interactive, déterministe

### Logique DNS robuste

- Vérification hiérarchique : NS → SOA → A → AAAA
- Vérifications parallèles pour rapidité
- Timeout configurable
- Gestion d'erreurs complète

### Documentation complète

- **README** : Guide complet pour humains et IA
- **EXAMPLES.md** : Intégrations Python, Node.js, Shell, Go, Rust
- **BUILD.md** : Instructions de build des binaires
- **CHANGELOG.md** : Historique des versions

## Téléchargement

### Binaires (recommandé)

- **Windows** : `okitsok.exe` (~9 MB)
- **macOS** : `okitsok` (~9 MB)
- **Linux** : `okitsok` (~9 MB)

### Installation pip

```bash
pip install okitsok
```

### Installation pipx (isolation)

```bash
pipx install okitsok
```

## Utilisation rapide

```bash
# Vérification basique
okitsok example

# Sortie JSON
okitsok example --json

# Avec timeout
okitsok example --timeout 5
```

## Statuts retournés

- **`available`** : Aucun enregistrement DNS (NXDOMAIN)
- **`taken`** : Enregistrements DNS détectés
- **`unknown`** : Impossible de déterminer (timeout, erreur)

## Exit codes

- **`0`** : Au moins un domaine disponible
- **`1`** : Aucun domaine disponible
- **`130`** : Interruption utilisateur

## Utilisation par des IA

okitsok est conçu pour être appelé par des agents conversationnels, des scripts ou d'autres outils :

```python
import subprocess
import json

result = subprocess.run(
    ["okitsok", "example", "--json"],
    capture_output=True,
    text=True
)
domains = json.loads(result.stdout)
print(domains["example.com"])  # "taken" | "available" | "unknown"
```

Voir **EXAMPLES.md** pour plus d'intégrations.

## Limites importantes

okitsok fournit un **indicateur technique**, pas une **certification** :

- ❌ Ne garantit PAS qu'un domaine est enregistrable
- ❌ Ne vérifie PAS les prix ou restrictions
- ❌ Ne contacte PAS les registrars
- ✅ Vérifie UNIQUEMENT les enregistrements DNS publics

**Recommandation** : Utilisez okitsok comme filtre initial, vérifiez toujours auprès d'un registrar pour confirmation finale.

## Philosophie

okitsok est construit pour durer :

- **Simple** : Une seule fonctionnalité, bien faite
- **Honnête** : Pas de marketing, limites clairement documentées
- **Universel** : Pour humains et machines
- **Local** : Aucune dépendance à des services externes
- **Responsable** : Pas de fausses promesses

## Support

- **Issues** : Rapportez des bugs ou suggestions sur le dépôt
- **Documentation** : README.md, EXAMPLES.md, BUILD.md
- **Licence** : MIT (libre d'utilisation)

## Contributeurs

Merci à tous ceux qui ont contribué à faire d'okitsok un outil simple et fiable.

---

**okitsok 1.0.0** - Février 2026
