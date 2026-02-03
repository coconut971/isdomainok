# okitsok

**Indicateur technique de disponibilité de noms de domaine via DNS**

`okitsok` est un outil local en ligne de commande qui interroge les serveurs DNS pour déterminer si un nom de domaine possède des enregistrements DNS actifs.

## Qu'est-ce que okitsok ?

okitsok est :
- Un **indicateur technique** basé sur le DNS
- Un **outil local** sans dépendance à un service web
- Une **brique simple** utilisable par un humain, un script ou une IA
- Un **outil non interactif** avec sortie standardisée

okitsok n'est PAS :
- Un service de certification de disponibilité
- Un outil de registrar
- Une garantie qu'un domaine est enregistrable
- Un service web ou une API

## Installation

### Option 1 : Binaire standalone (recommandé)

**Aucune installation de Python requise.**

1. Téléchargez le binaire pour votre plateforme :
   - **Windows** : `okitsok.exe`
   - **macOS** : `okitsok`
   - **Linux** : `okitsok`

2. Utilisez directement :
   ```bash
   # Windows
   okitsok.exe example
   
   # macOS / Linux
   ./okitsok example
   ```

### Option 2 : pipx (isolation)

```bash
pipx install okitsok
okitsok example
```

### Option 3 : pip (développeurs)

```bash
pip install okitsok
okitsok example
```

## Utilisation

### Utilisation basique

```bash
okitsok example
```

Sortie :
```
example.com  taken
example.fr   taken
example.io   taken
example.app  available
```

### Format JSON (machine-readable)

```bash
okitsok example --json
```

Sortie strictement JSON :
```json
{
  "example.com": "taken",
  "example.fr": "taken",
  "example.io": "taken",
  "example.app": "available"
}
```

### Options

- `--json` : Sortie JSON pure (pas de texte supplémentaire)
- `--timeout SECONDS` : Timeout par requête DNS (défaut : 3.0)
- `--version` : Affiche la version
- `--help` : Affiche l'aide

## Statuts retournés

okitsok retourne UNIQUEMENT trois statuts :

| Statut | Signification | Description |
|--------|---------------|-------------|
| `available` | Aucun enregistrement DNS trouvé | NXDOMAIN retourné par les serveurs DNS |
| `taken` | Enregistrements DNS détectés | Au moins un enregistrement NS, SOA, A ou AAAA existe |
| `unknown` | Impossible de déterminer | Timeout, erreur DNS ou serveur inaccessible |

## Exit codes

Les exit codes permettent l'intégration dans des scripts :

| Code | Condition |
|------|-----------|
| `0` | Au moins un domaine est `available` |
| `1` | Aucun domaine `available` (tous `taken` ou `unknown`) |
| `130` | Interruption utilisateur (Ctrl+C) |

Exemple d'utilisation en script :
```bash
if okitsok mysite --json > /dev/null 2>&1; then
  echo "Au moins un domaine disponible"
else
  echo "Aucun domaine disponible"
fi
```

## Utilisation par une IA ou un agent

### Cas d'usage

okitsok peut être appelé par :
- Un agent conversationnel
- Un script Python/Node.js/Shell
- Un workflow automatisé
- Un autre outil en ligne de commande

### Appel depuis un agent

```python
import subprocess
import json

def check_domain_availability(name: str) -> dict:
    """Vérifie la disponibilité d'un domaine via okitsok."""
    result = subprocess.run(
        ["okitsok", name, "--json"],
        capture_output=True,
        text=True,
        timeout=15
    )
    return json.loads(result.stdout)

# Utilisation
domains = check_domain_availability("example")
print(domains["example.com"])  # "taken" ou "available" ou "unknown"
```

### Format de sortie garanti

En mode `--json`, okitsok garantit :
- ✅ Sortie JSON valide uniquement
- ✅ Aucun texte parasite (pas de messages, pas d'avertissements dans stdout)
- ✅ Structure stable : `{ "domaine.ext": "statut" }`
- ✅ Statuts limités à : `available`, `taken`, `unknown`
- ✅ Comportement déterministe

### Intégration multi-langage

**Node.js :**
```javascript
const { execSync } = require('child_process');
const domains = JSON.parse(execSync('okitsok example --json').toString());
console.log(domains['example.com']);
```

**Shell :**
```bash
okitsok example --json | jq '.["example.com"]'
```

**Rust :**
```rust
use std::process::Command;
let output = Command::new("okitsok")
    .args(&["example", "--json"])
    .output()
    .expect("Failed to execute okitsok");
let domains: serde_json::Value = serde_json::from_slice(&output.stdout)?;
```

## Fonctionnement technique

okitsok interroge les serveurs DNS publics dans cet ordre :

1. Enregistrements **NS** (nameservers)
2. Enregistrements **SOA** (Start of Authority)
3. Enregistrements **A** (IPv4)
4. Enregistrements **AAAA** (IPv6)

Dès qu'un enregistrement est trouvé, le statut est `taken`.

### Extensions vérifiées par défaut

`.com`, `.fr`, `.io`, `.app`

## Limites importantes

**okitsok fournit un indicateur technique DNS, pas une certification de disponibilité.**

### Ce que okitsok NE fait PAS

- ❌ Ne contacte AUCUN registrar
- ❌ Ne vérifie PAS les prix
- ❌ Ne vérifie PAS les restrictions d'enregistrement
- ❌ Ne garantit PAS qu'un domaine est enregistrable
- ❌ N'utilise PAS de base de données WHOIS
- ❌ N'utilise PAS d'API externe

### Ce que okitsok vérifie

- ✅ Présence d'enregistrements DNS publics au moment de la requête

### Pourquoi un domaine `available` peut être indisponible

1. **Période de grâce/rédemption** : Domaine expiré non encore libéré
2. **Réservation** : Certains noms sont bloqués (marques, termes réservés)
3. **Domaine premium** : Disponible mais à prix élevé
4. **Restrictions TLD** : Règles spécifiques (ex: `.fr` nécessite une adresse UE)
5. **Propagation DNS** : Domaine fraîchement enregistré, DNS pas encore propagé

### Recommandation d'usage

✅ **Filtrage initial** : Éliminer rapidement les noms déjà pris
❌ **Décision finale** : Toujours confirmer auprès d'un registrar officiel

## Détails techniques

- **Langage** : Python 3.7+
- **Dépendance** : dnspython (incluse dans le binaire)
- **Vérifications** : Parallèles (concurrent.futures)
- **Plateformes** : Windows, macOS, Linux
- **Mode** : 100% local, aucun service externe

## Utilisation par des frameworks et orchestrateurs

okitsok inclut des descripteurs machine-readable pour faciliter l'intégration automatique :

- `ai-tool.yaml` : Descripteur principal pour agents et frameworks IA
- `okitsok.tool.json` : Version JSON pour loaders automatiques
- `TOOLS.md` : Documentation complète sur l'intégration

Ces fichiers permettent aux agents de :
- Découvrir les capacités d'okitsok
- Télécharger le binaire approprié pour la plateforme
- Comprendre le format de commande et le schéma de sortie
- Gérer correctement les exit codes

Voir [TOOLS.md](TOOLS.md) pour plus de détails.

## Build depuis les sources

Voir [BUILD.md](BUILD.md) pour générer les binaires standalone.

## Licence

MIT
