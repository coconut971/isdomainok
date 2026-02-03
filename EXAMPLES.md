# Exemples d'utilisation - okitsok

Ce document contient des exemples concrets d'intégration d'okitsok dans différents contextes.

## CLI de base

### Vérification simple
```bash
okitsok example
```

### Sortie JSON
```bash
okitsok example --json
```

### Avec timeout personnalisé
```bash
okitsok example --timeout 5 --json
```

## Intégration Python

### Vérification simple
```python
import subprocess
import json

def check_domains(name: str) -> dict:
    """Vérifie la disponibilité d'un nom de domaine."""
    result = subprocess.run(
        ["okitsok", name, "--json"],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"okitsok error: {result.stderr}")

# Utilisation
domains = check_domains("myapp")
for domain, status in domains.items():
    print(f"{domain}: {status}")
```

### Vérification avec exit code
```python
import subprocess

def has_available_domain(name: str) -> bool:
    """Retourne True si au moins un domaine est disponible."""
    result = subprocess.run(
        ["okitsok", name, "--json"],
        capture_output=True,
        timeout=15
    )
    return result.returncode == 0

# Utilisation
if has_available_domain("myapp"):
    print("✓ Au moins un domaine disponible")
else:
    print("✗ Aucun domaine disponible")
```

### Agent conversationnel
```python
import subprocess
import json
from typing import Dict, List

class DomainChecker:
    """Agent pour vérifier la disponibilité de domaines."""
    
    def check(self, name: str) -> Dict[str, str]:
        """Vérifie un nom de domaine."""
        result = subprocess.run(
            ["okitsok", name, "--json"],
            capture_output=True,
            text=True,
            timeout=15
        )
        return json.loads(result.stdout)
    
    def find_available(self, name: str) -> List[str]:
        """Retourne la liste des domaines disponibles."""
        domains = self.check(name)
        return [d for d, status in domains.items() if status == "available"]
    
    def all_taken(self, name: str) -> bool:
        """Vérifie si tous les domaines sont pris."""
        domains = self.check(name)
        return all(status == "taken" for status in domains.values())

# Utilisation dans un agent
checker = DomainChecker()
available = checker.find_available("myapp")
print(f"Domaines disponibles: {', '.join(available)}")
```

## Intégration Node.js

### Vérification simple
```javascript
const { execSync } = require('child_process');

function checkDomains(name) {
  const output = execSync(`okitsok ${name} --json`).toString();
  return JSON.parse(output);
}

// Utilisation
const domains = checkDomains('example');
console.log(domains['example.com']); // "taken" | "available" | "unknown"
```

### Avec gestion d'erreurs
```javascript
const { execSync } = require('child_process');

function checkDomains(name) {
  try {
    const output = execSync(`okitsok ${name} --json`, {
      encoding: 'utf8',
      timeout: 15000
    });
    return JSON.parse(output);
  } catch (error) {
    if (error.status === 1) {
      // Aucun domaine disponible, mais l'outil a fonctionné
      return JSON.parse(error.stdout);
    }
    throw new Error(`okitsok error: ${error.message}`);
  }
}

// Utilisation
const domains = checkDomains('myapp');
Object.entries(domains).forEach(([domain, status]) => {
  console.log(`${domain}: ${status}`);
});
```

## Intégration Shell

### Vérification avec jq
```bash
#!/bin/bash
NAME="myapp"
STATUS=$(okitsok $NAME --json | jq -r '.["'$NAME'.com"]')

if [ "$STATUS" = "available" ]; then
  echo "$NAME.com est disponible"
else
  echo "$NAME.com est $STATUS"
fi
```

### Boucle sur plusieurs noms
```bash
#!/bin/bash
NAMES=("myapp" "mysite" "mytool")

for name in "${NAMES[@]}"; do
  echo "Checking $name..."
  okitsok "$name" --json | jq '.'
  echo ""
done
```

### Utilisation de l'exit code
```bash
#!/bin/bash
if okitsok myapp --json > /dev/null 2>&1; then
  echo "✓ Au moins un domaine disponible"
  okitsok myapp --json | jq -r 'to_entries[] | select(.value=="available") | .key'
else
  echo "✗ Aucun domaine disponible"
fi
```

## Intégration Go

```go
package main

import (
    "encoding/json"
    "os/exec"
)

type DomainStatus map[string]string

func checkDomains(name string) (DomainStatus, error) {
    cmd := exec.Command("okitsok", name, "--json")
    output, err := cmd.Output()
    if err != nil && cmd.ProcessState.ExitCode() != 0 {
        return nil, err
    }
    
    var domains DomainStatus
    if err := json.Unmarshal(output, &domains); err != nil {
        return nil, err
    }
    
    return domains, nil
}

func main() {
    domains, err := checkDomains("example")
    if err != nil {
        panic(err)
    }
    
    for domain, status := range domains {
        println(domain, ":", status)
    }
}
```

## Intégration Rust

```rust
use std::process::Command;
use serde_json::Value;

fn check_domains(name: &str) -> Result<Value, Box<dyn std::error::Error>> {
    let output = Command::new("okitsok")
        .args(&[name, "--json"])
        .output()?;
    
    let domains: Value = serde_json::from_slice(&output.stdout)?;
    Ok(domains)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let domains = check_domains("example")?;
    
    if let Some(obj) = domains.as_object() {
        for (domain, status) in obj {
            println!("{}: {}", domain, status);
        }
    }
    
    Ok(())
}
```

## Cas d'usage avancés

### Vérification de plusieurs variantes
```python
import subprocess
import json

def check_variants(base_name: str, variants: list) -> dict:
    """Vérifie plusieurs variantes d'un nom."""
    results = {}
    for variant in variants:
        name = base_name + variant
        result = subprocess.run(
            ["okitsok", name, "--json"],
            capture_output=True,
            text=True,
            timeout=15
        )
        results[name] = json.loads(result.stdout)
    return results

# Utilisation
variants = ["", "app", "io", "dev"]
all_results = check_variants("myproject", variants)

for variant, domains in all_results.items():
    available = [d for d, s in domains.items() if s == "available"]
    if available:
        print(f"{variant}: {', '.join(available)}")
```

### Recommandations par une IA
```python
import subprocess
import json

def recommend_available_names(base_name: str) -> list:
    """Recommande des noms de domaine disponibles."""
    result = subprocess.run(
        ["okitsok", base_name, "--json"],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    domains = json.loads(result.stdout)
    available = [
        domain for domain, status in domains.items()
        if status == "available"
    ]
    
    if available:
        return available
    else:
        return ["Tous les domaines sont pris. Essayez une autre variante."]

# Utilisation dans un agent conversationnel
suggestions = recommend_available_names("myapp")
print("Domaines disponibles suggérés :")
for suggestion in suggestions:
    print(f"  - {suggestion}")
```

## Notes pour les développeurs

### Timeout recommandé
- Défaut : 3 secondes par domaine
- 4 domaines par défaut = ~12 secondes maximum
- Ajouter une marge : timeout de 15 secondes conseillé

### Gestion des erreurs
- Exit code 0 : Au moins un domaine disponible
- Exit code 1 : Aucun domaine disponible (sortie JSON toujours valide)
- Exit code 130 : Interruption utilisateur

### Parsing de la sortie
- Mode `--json` : stdout contient UNIQUEMENT du JSON valide
- stderr peut contenir des messages d'erreur (en cas d'échec)
- Toujours parser stdout, pas stderr
