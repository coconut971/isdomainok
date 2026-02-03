# AI Agent Integration Guide

okitsok is designed to be integrated into AI agents, frameworks, and automated workflows.

## Installation for Agents

Agents should download okitsok from GitHub Releases:

- **Windows:** https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe
- **macOS:** https://github.com/coconut971/okitsok/releases/latest/download/okitsok
- **Linux:** https://github.com/coconut971/okitsok/releases/latest/download/okitsok

## Tool Descriptor

okitsok includes machine-readable descriptors for automated discovery and integration:

- `ai-tool.yaml` - Primary descriptor (install, usage, schema)
- `okitsok.tool.json` - JSON version for automated parsers

Read these files from the repository root for complete specifications.

## Usage Pattern

### Basic Usage

```bash
okitsok {domain} --json
```

### Complete Workflow

1. Download binary (first time only)
2. Execute: `okitsok myapp --json`
3. Parse JSON output from stdout
4. Use exit code for decision making

## Output Schema

JSON output follows this strict schema:

```json
{
  "domain.tld": "available" | "taken" | "unknown"
}
```

### Status Meanings

- `available` - No DNS records found (NXDOMAIN)
- `taken` - DNS records detected (NS, SOA, A, or AAAA)
- `unknown` - Cannot determine (timeout, DNS error)

### Guaranteed Behavior

- Only JSON in stdout when using `--json`
- No text pollution or warnings in stdout
- Errors go to stderr only
- Deterministic output format

## Exit Codes

```
0   - At least one domain is available
1   - No domains available (all taken or unknown)
130 - User interrupted (Ctrl+C)
```

Agents can use exit codes for decision making:

```python
result = subprocess.run(["okitsok", "myapp", "--json"], capture_output=True)
if result.returncode == 0:
    # At least one domain available
    domains = json.loads(result.stdout)
else:
    # No domains available
    pass
```

## Error Handling

### Timeouts

- Recommended timeout: 15 seconds
- Covers 4 domains × 3s each + margin
- DNS queries may take 1-3 seconds each

### Parsing

Always use `--json` flag and parse stdout:

```python
result = subprocess.run(
    ["okitsok", "domain", "--json"],
    capture_output=True,
    text=True,
    timeout=15
)

if result.returncode in [0, 1]:  # Both are valid
    domains = json.loads(result.stdout)
else:
    # Handle error (check stderr)
    error = result.stderr
```

## Integration Examples

### Python (LangChain style)

```python
import subprocess
import json
from typing import Dict, List

class DomainCheckerTool:
    name = "domain_checker"
    description = "Check domain availability via DNS"
    
    def run(self, domain_name: str) -> Dict[str, str]:
        result = subprocess.run(
            ["./okitsok", domain_name, "--json"],
            capture_output=True,
            text=True,
            timeout=15
        )
        return json.loads(result.stdout)
    
    def find_available(self, domain_name: str) -> List[str]:
        domains = self.run(domain_name)
        return [d for d, s in domains.items() if s == "available"]
```

### Node.js (AutoGPT style)

```javascript
const { execSync } = require('child_process');

class DomainChecker {
  check(domainName) {
    const output = execSync(
      `./okitsok ${domainName} --json`,
      { encoding: 'utf8', timeout: 15000 }
    );
    return JSON.parse(output);
  }
  
  getAvailable(domainName) {
    const results = this.check(domainName);
    return Object.entries(results)
      .filter(([_, status]) => status === 'available')
      .map(([domain, _]) => domain);
  }
}
```

### System Prompt (Claude/GPT)

```markdown
You have access to okitsok for checking domain availability.

Usage: ./okitsok {domain} --json

Output: { "domain.tld": "available" | "taken" | "unknown" }

When user asks about domains:
1. Execute okitsok with domain name
2. Parse JSON output
3. Report available domains
4. Remind: DNS check only, verify with registrar
```

## Limitations

### What okitsok checks

- DNS records (NS, SOA, A, AAAA)
- Technical DNS availability only

### What okitsok does NOT check

- Registrar availability
- Domain prices
- Premium domains
- Reserved names
- TLD-specific restrictions

### Recommendation

Always inform users that:
- Results are DNS-based indicators
- Final verification needed with registrar
- "available" != guaranteed registrable

## TLDs Checked

Default TLDs: `.com`, `.fr`, `.io`, `.app`

These are hardcoded and cannot be changed without modifying the source.

## Performance

- Parallel DNS queries (4 concurrent by default)
- ~3 seconds total for 4 domains
- Configurable timeout: `--timeout SECONDS`

## Security

- No data sent to external services
- Pure DNS queries to public resolvers
- No tracking, no telemetry
- Standalone binary (no network dependencies)

## Deployment

### Docker

```dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y curl
RUN curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok -o /usr/local/bin/okitsok
RUN chmod +x /usr/local/bin/okitsok
CMD ["okitsok"]
```

### CI/CD

```yaml
- name: Check domain availability
  run: |
    curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok -o okitsok
    chmod +x okitsok
    ./okitsok ${{ env.DOMAIN_NAME }} --json
```

## Support

- Repository: https://github.com/coconut971/okitsok
- Issues: https://github.com/coconut971/okitsok/issues
- Examples: See EXAMPLES.md in repository

## License

MIT - Free for commercial and non-commercial use
