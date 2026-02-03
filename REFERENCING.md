# Plan de référencement okitsok

Plan d'actions concrètes pour rendre okitsok découvrable par les humains et les IA.

## Priorités

### Priorité 1 : Awesome Lists GitHub (impact maximum, effort minimal)
### Priorité 2 : Communautés techniques (visibilité ciblée)
### Priorité 3 : Documentation agents IA (adoption automatisée)

---

## 1. AWESOME LISTS GITHUB

### A. awesome-cli-apps (18.5k stars)
**Repo :** https://github.com/agarrharr/awesome-cli-apps
**Section :** Internet → Domain

**Texte à proposer :**
```markdown
- [okitsok](https://github.com/coconut971/okitsok) - DNS-based domain name availability checker. Local, fast, machine-readable output.
```

**Action :**
1. Fork https://github.com/agarrharr/awesome-cli-apps
2. Éditer `readme.md`, section "Internet"
3. Ajouter la ligne ci-dessus
4. Pull Request avec titre : "Add okitsok - DNS domain checker"
5. Description PR : "okitsok is a local CLI tool that checks domain availability using DNS queries. No external APIs, pure DNS-based checking with JSON output."

---

### B. awesome-dns
**Repo :** https://github.com/SoylentBob/awesome-dns
**Section :** Tools

**Texte à proposer :**
```markdown
- [okitsok](https://github.com/coconut971/okitsok) - Domain availability checker using DNS signals (NS/SOA/A/AAAA). Standalone binary, JSON output, no external APIs.
```

**Action :**
1. Fork https://github.com/SoylentBob/awesome-dns
2. Éditer `README.md`, section "Tools"
3. Ajouter la ligne ci-dessus
4. Pull Request avec titre : "Add okitsok - DNS domain availability tool"
5. Description PR : "okitsok checks domain availability by querying DNS records directly. Local-first, no registrar APIs, deterministic output."

---

### C. awesome-ai-tools
**Repo :** https://github.com/tankvn/awesome-ai-tools
**Section :** Developer Tools ou Code

**Texte à proposer :**
```markdown
- [okitsok](https://github.com/coconut971/okitsok) - DNS domain checker with machine-readable output. Declarable via ai-tool.yaml for automated integration.
```

**Action :**
1. Fork https://github.com/tankvn/awesome-ai-tools
2. Éditer le fichier approprié (2025 ou main)
3. Ajouter la ligne ci-dessus
4. Pull Request avec titre : "Add okitsok - AI-integrable domain checker"
5. Description PR : "okitsok is a CLI tool designed for AI agent integration. Includes ai-tool.yaml descriptor for automated installation and usage."

---

## 2. COMMUNAUTÉS TECHNIQUES

### A. Hacker News - Show HN

**Titre :**
```
Show HN: okitsok – DNS-based domain availability checker
```

**Texte :**
```
okitsok is a local CLI tool that checks if domain names are available by querying DNS records directly.

Key points:
- No external APIs or registrars
- Checks NS, SOA, A, AAAA records
- JSON output for scripting
- Standalone binary (Windows/macOS/Linux)
- Designed for both human and AI agent use

It doesn't guarantee a domain is registrable (DNS != registrar availability), but provides a fast technical signal for filtering names.

Includes ai-tool.yaml descriptor for automated integration into AI workflows.

GitHub: https://github.com/coconut971/okitsok
```

**Quand poster :** Mardi ou Mercredi, 8h-10h EST (meilleur engagement)

---

### B. Reddit - r/commandline

**Titre :**
```
[Tool] okitsok - Check domain availability via DNS queries
```

**Texte :**
```
I built okitsok, a CLI tool that checks domain name availability using DNS lookups.

How it works:
- Queries DNS for NS, SOA, A, AAAA records
- Returns: available, taken, or unknown
- Pure DNS-based (no WHOIS, no registrar APIs)
- JSON output for scripting

Usage:
okitsok example --json

Returns:
{
  "example.com": "taken",
  "example.io": "available"
}

Limitations:
- DNS signal only (not a registrar check)
- Won't catch reserved/premium domains

Good for: filtering domain ideas quickly before checking with a registrar.

GitHub: https://github.com/coconut971/okitsok
Binaries: Windows/macOS/Linux
License: MIT
```

---

### C. Reddit - r/AI_Agents (si existe) ou r/LocalLLaMA

**Titre :**
```
[Resource] okitsok - CLI tool with ai-tool.yaml descriptor for agent integration
```

**Texte :**
```
okitsok is a domain availability checker designed to be used by AI agents.

Why it's agent-friendly:
- Includes ai-tool.yaml descriptor (installation + usage schema)
- JSON-only output mode (no text pollution)
- Deterministic exit codes
- Standalone binary (no Python needed)

Agents can:
1. Read ai-tool.yaml from the repo
2. Download the appropriate binary
3. Execute: okitsok {domain} --json
4. Parse guaranteed JSON output

Use case: Agent helping user find available domain names for a project.

GitHub: https://github.com/coconut971/okitsok
```

---

## 3. EXEMPLES D'INTÉGRATION AGENTS IA

### Exemple 1 : Agent Python (LangChain style)

```python
import subprocess
import json
from typing import Dict, List

class DomainCheckerTool:
    """Tool for checking domain availability via okitsok."""
    
    name = "domain_checker"
    description = "Check if domain names are available using DNS queries"
    
    def __init__(self, okitsok_path: str = "./okitsok"):
        self.okitsok_path = okitsok_path
    
    def run(self, domain_name: str) -> Dict[str, str]:
        """Check domain availability.
        
        Args:
            domain_name: Base domain name without TLD
            
        Returns:
            Dict mapping full domains to status (available/taken/unknown)
        """
        result = subprocess.run(
            [self.okitsok_path, domain_name, "--json"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        return json.loads(result.stdout)
    
    def find_available(self, domain_name: str) -> List[str]:
        """Find available domains for a given name."""
        domains = self.run(domain_name)
        return [d for d, status in domains.items() if status == "available"]

# Usage
tool = DomainCheckerTool()
available = tool.find_available("myapp")
print(f"Available: {', '.join(available)}")
```

### Exemple 2 : Intégration Claude/GPT (prompt système)

```markdown
You have access to okitsok, a CLI tool for checking domain availability.

Tool location: ./okitsok
Usage: ./okitsok {domain} --json

Output format:
{
  "example.com": "taken",
  "example.fr": "available",
  "example.io": "taken",
  "example.app": "unknown"
}

Status meanings:
- "available": No DNS records found (domain appears free)
- "taken": DNS records exist (domain is registered)
- "unknown": Cannot determine (timeout or DNS error)

Exit codes:
- 0: At least one domain is available
- 1: No domains available

Limitations:
- DNS-based only (not a registrar check)
- Results are indicative, not guaranteed

When user asks about domain availability:
1. Execute: ./okitsok {name} --json
2. Parse JSON output
3. Report available domains
4. Remind user to verify with registrar
```

### Exemple 3 : Agent Node.js (AutoGPT style)

```javascript
const { execSync } = require('child_process');

class DomainChecker {
  constructor(okitsokPath = './okitsok') {
    this.okitsokPath = okitsokPath;
  }
  
  check(domainName) {
    try {
      const output = execSync(
        `${this.okitsokPath} ${domainName} --json`,
        { encoding: 'utf8', timeout: 15000 }
      );
      return JSON.parse(output);
    } catch (error) {
      if (error.status === 1) {
        // No domains available, but output is still valid
        return JSON.parse(error.stdout);
      }
      throw error;
    }
  }
  
  getAvailable(domainName) {
    const results = this.check(domainName);
    return Object.entries(results)
      .filter(([_, status]) => status === 'available')
      .map(([domain, _]) => domain);
  }
}

// Usage
const checker = new DomainChecker();
const available = checker.getAvailable('myproject');
console.log('Available domains:', available);
```

---

## 4. DOCUMENTATION POUR FRAMEWORKS AI

### Fichier à créer : AI_INTEGRATION.md

```markdown
# AI Agent Integration Guide

## Installation

Agents should download okitsok from GitHub Releases:

- Windows: https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe
- macOS: https://github.com/coconut971/okitsok/releases/latest/download/okitsok
- Linux: https://github.com/coconut971/okitsok/releases/latest/download/okitsok

## Tool Descriptor

Read ai-tool.yaml from the repository root for machine-readable specifications.

## Usage Pattern

1. Execute: okitsok {domain} --json
2. Parse JSON output
3. Use exit code for decision making

## Output Schema

{
  "domain.tld": "available" | "taken" | "unknown"
}

## Exit Codes

- 0: At least one domain available
- 1: No domains available
- 130: User interrupted

## Error Handling

Always use --json flag and parse stdout.
Timeout: Recommended 15 seconds (covers 4 domains × 3s each + margin).

## Limitations

DNS-based checking only. Results are technical indicators, not registrar confirmations.
Always recommend users verify with official registrars.

## Example Integration

See EXAMPLES.md for Python, Node.js, and other language integrations.
```

---

## 5. CHECKLIST D'ACTIONS

### Actions Prioritaires (faire en premier)

- [ ] **PR #1 : awesome-cli-apps**
  - Fork + éditer + PR
  - Impact : 18.5k stars, très visible
  - Effort : 10 minutes

- [ ] **PR #2 : awesome-dns**
  - Fork + éditer + PR
  - Impact : communauté DNS technique
  - Effort : 10 minutes

- [ ] **Show HN**
  - Poster sur Hacker News
  - Impact : visibilité tech, feedback
  - Effort : 5 minutes
  - Timing : Mardi/Mercredi 8h-10h EST

### Actions Secondaires (optionnel, après)

- [ ] **PR #3 : awesome-ai-tools**
  - Fork + éditer + PR
  - Impact : communauté AI/agents
  - Effort : 10 minutes

- [ ] **Reddit r/commandline**
  - Poster avec texte préparé
  - Impact : communauté CLI
  - Effort : 5 minutes

- [ ] **Reddit r/LocalLLaMA ou r/AI_Agents**
  - Poster avec texte préparé
  - Impact : communauté AI
  - Effort : 5 minutes

- [ ] **Créer AI_INTEGRATION.md**
  - Ajouter au repo
  - Impact : documentation agents
  - Effort : 5 minutes (texte déjà prêt)

---

## 6. ORDRE D'EXÉCUTION RECOMMANDÉ

### Semaine 1 (maintenant)
1. PR awesome-cli-apps
2. PR awesome-dns
3. Show HN (attendre merge des PR pour mentionner)

### Semaine 2 (si bon feedback)
4. Reddit r/commandline
5. PR awesome-ai-tools

### Semaine 3 (si adoption)
6. Reddit AI/LLM
7. Créer AI_INTEGRATION.md
8. Documenter cas d'usage réels

---

## 7. MÉTRIQUES DE SUCCÈS

**Court terme (1 mois) :**
- 2-3 PR mergées dans awesome lists
- 50+ stars sur GitHub
- 1-2 issues/questions d'utilisateurs

**Moyen terme (3 mois) :**
- 100+ stars
- Mentionné dans 1-2 projets tiers
- 1-2 contributions externes

**Long terme (6 mois) :**
- 200+ stars
- Intégré dans 1+ framework/agent
- Utilisé par la communauté sans intervention

---

## 8. CE QU'IL NE FAUT PAS FAIRE

- Ne pas spam les communautés
- Ne pas poster plusieurs fois le même contenu
- Ne pas faire de marketing agressif
- Ne pas promettre plus que ce que fait l'outil
- Ne pas créer de faux comptes pour promouvoir
- Ne pas poster dans des communautés non techniques

---

## RÉSUMÉ : 3 ACTIONS POUR COMMENCER

1. **Fork + PR awesome-cli-apps** (10 min)
2. **Fork + PR awesome-dns** (10 min)
3. **Post Show HN** (5 min)

Total : 25 minutes pour lancer le référencement.

Le reste peut attendre le feedback initial.
