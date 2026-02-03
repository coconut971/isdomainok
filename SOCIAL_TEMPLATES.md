# Templates pour réseaux sociaux (optionnel)

Templates sobres et techniques pour annoncer okitsok sur les réseaux sociaux.

## Twitter/X

### Version courte (limite 280 caractères)

```
Built okitsok: CLI tool to check domain availability via DNS queries.

Local, fast, JSON output. No APIs needed.

Includes ai-tool.yaml for AI agent integration.

https://github.com/coconut971/okitsok
```

### Version détaillée (thread)

**Tweet 1/3:**
```
Built okitsok: a DNS-based domain availability checker.

Checks NS/SOA/A/AAAA records to determine if domains are taken or available.

Local tool, no external APIs, JSON output.

https://github.com/coconut971/okitsok
```

**Tweet 2/3:**
```
Why DNS-only?

- Fast (no rate limits)
- Local (no API keys)
- Deterministic (pure technical signal)

Limitation: DNS ≠ registrar availability. Use for filtering, verify with registrars.
```

**Tweet 3/3:**
```
Designed for humans + AI agents.

Includes ai-tool.yaml descriptor for automated integration.

Agents can discover, install, and use okitsok without manual configuration.

MIT licensed. Windows/macOS/Linux binaries available.
```

---

## LinkedIn

### Post simple

```
I built okitsok, a command-line tool for checking domain name availability using DNS queries.

What it does:
- Queries DNS records (NS, SOA, A, AAAA)
- Returns: available, taken, or unknown
- JSON output for scripting
- Standalone binary (no installation)

What it doesn't do:
- Contact registrars
- Guarantee availability
- Check pricing

Use case: Quickly filter domain ideas before checking with registrars.

Designed for developers, DevOps, and AI agents (includes ai-tool.yaml descriptor).

Open source (MIT): https://github.com/coconut971/okitsok

#OpenSource #CLI #DNS #DeveloperTools
```

### Post technique (avec code)

```
Released okitsok v1.0.0 - DNS-based domain availability checker.

Technical highlights:

1. Pure DNS approach
   - Queries NS, SOA, A, AAAA records
   - No external APIs or WHOIS
   - Local and fast

2. Machine-readable output
   - JSON format: {"domain.tld": "available|taken|unknown"}
   - Deterministic exit codes
   - No text pollution

3. AI agent ready
   - Includes ai-tool.yaml descriptor
   - Automated installation & usage
   - Standard integration pattern

Example:
$ okitsok myapp --json
{
  "myapp.com": "taken",
  "myapp.io": "available"
}

Limitations: DNS signal only. Always verify with registrars.

MIT licensed. Binaries for Windows/macOS/Linux.

GitHub: https://github.com/coconut971/okitsok

#DevTools #CLI #OpenSource #DNS #AIAgents
```

---

## Mastodon / Bluesky

### Post court

```
Built okitsok: DNS-based domain availability checker

✓ Local (no APIs)
✓ Fast (parallel DNS queries)
✓ JSON output
✓ AI-integrable (ai-tool.yaml)

Check domain availability via DNS records.
Not a registrar check, but a fast technical filter.

https://github.com/coconut971/okitsok

#OpenSource #CLI #DNS
```

---

## Dev.to / Hashnode (article)

### Titre suggéré

```
Building okitsok: A DNS-based Domain Availability Checker for Humans and AI
```

### Outline (si vous voulez écrire un article)

1. **Why I built okitsok**
   - Need for quick domain checks
   - Avoiding API rate limits
   - Local-first approach

2. **How it works**
   - DNS record checking (NS, SOA, A, AAAA)
   - Parallel queries
   - JSON output

3. **Design for AI agents**
   - ai-tool.yaml descriptor
   - Deterministic behavior
   - Exit codes

4. **Limitations and honesty**
   - DNS != registrar
   - Use cases and non-use cases
   - Responsible tooling

5. **Technical stack**
   - Python + dnspython
   - PyInstaller for binaries
   - No external dependencies

6. **Open source release**
   - MIT license
   - GitHub + releases
   - Community contributions welcome

---

## Reddit (technique détaillé)

### r/programming

**Titre:**
```
[Project] okitsok - DNS-based domain availability checker with AI integration support
```

**Texte:**
```
I built okitsok, a CLI tool for checking domain availability using DNS queries.

Technical approach:
- Queries DNS records: NS → SOA → A → AAAA
- Returns first signal (if NS exists, domain is taken)
- Parallel execution (concurrent.futures)
- Timeout: 3s per query, 4 queries default

Output:
- Human: aligned text with status
- Machine: strict JSON (no text pollution)
- Exit codes: 0 (available found), 1 (none available)

AI integration:
- Includes ai-tool.yaml descriptor
- Agents can auto-install from GitHub releases
- Deterministic behavior for automated workflows

Implementation:
- Python 3.7+ + dnspython
- PyInstaller for standalone binaries
- ~9MB executable (includes Python runtime)

Limitations (important):
- DNS signal only (not WHOIS, not registrar)
- Can't detect: reserved names, premium pricing, grace periods
- Use case: filtering, not final confirmation

Why DNS-only:
- No API keys needed
- No rate limits
- Local execution
- Fast (parallel queries)

Trade-offs:
- Less accurate than registrar checks
- Won't catch all edge cases
- Good for filtering, not certification

GitHub: https://github.com/coconut971/okitsok
License: MIT
Binaries: Windows/macOS/Linux

Open to feedback and contributions.
```

---

## Guidelines d'utilisation

### Fréquence
- Twitter: 1 post initial
- LinkedIn: 1 post après quelques retours positifs
- Reddit: 1 post par subreddit pertinent (max 2-3 subreddits)
- Dev.to: 1 article si vous avez le temps

### Timing
- Attendre que les PR awesome lists soient mergées
- Mentionner dans les posts si déjà référencé
- Ne pas tout poster le même jour

### Ton
- Technique, sobre, factuel
- Mentionner les limitations
- Pas de marketing agressif
- Répondre aux questions/critiques honnêtement

### À éviter
- Self-promotion excessive
- Poster dans des subreddits non techniques
- Promettre plus que ce que l'outil fait
- Ignorer les critiques constructives

---

## Mesure d'impact (optionnel)

Si vous voulez suivre l'impact des posts sociaux:

1. Créer des UTM parameters (Google Analytics)
   ```
   https://github.com/coconut971/okitsok?utm_source=twitter&utm_medium=social&utm_campaign=launch
   ```

2. Suivre sur GitHub:
   - Traffic → Sources
   - Insights → Traffic

3. Observer:
   - Stars sur 24h après post
   - Issues/questions d'utilisateurs
   - Forks et contributions

---

## Priorités

**Priorité 1:** Awesome lists + Show HN (voir START_HERE.md)

**Priorité 2:** Twitter/LinkedIn (si vous avez une audience tech)

**Priorité 3:** Reddit r/programming ou r/commandline

**Optionnel:** Article blog, Mastodon, autres réseaux

Le plus important est que le code soit bon et que l'outil soit utile.
Les réseaux sociaux sont secondaires.
