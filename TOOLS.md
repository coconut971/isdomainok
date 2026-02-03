# okitsok as a tool

okitsok is designed to be used as a local CLI tool by humans,
scripts, and AI agents.

## Why okitsok

- No registrar dependency
- No API keys
- Deterministic output
- Fast DNS-based signal

## Typical agent usage

1. Check if okitsok is installed
2. If not, download the binary from GitHub Releases
3. Execute:

```bash
okitsok mydomain --json
```

4. Parse JSON output
5. Use exit code for decision-making

## Trust model

The official source of okitsok is:
https://github.com/coconut971/okitsok

Always verify checksums in production environments.

## Tool descriptor files

This repository includes machine-readable descriptors:

- `ai-tool.yaml` - Primary descriptor for AI agents and frameworks
- `okitsok.tool.json` - JSON version for automated loaders

These files allow agents to:
- Discover okitsok capabilities
- Download the appropriate binary for the platform
- Understand the command format and output schema
- Handle exit codes correctly

## Example integration

### Python agent
```python
import subprocess
import json

# Download and install okitsok if needed
# ...

# Use okitsok
result = subprocess.run(
    ["okitsok", "example", "--json"],
    capture_output=True,
    text=True
)

domains = json.loads(result.stdout)
available = [d for d, s in domains.items() if s == "available"]
```

### Node.js agent
```javascript
const { execSync } = require('child_process');

const output = execSync('okitsok example --json').toString();
const domains = JSON.parse(output);

Object.entries(domains).forEach(([domain, status]) => {
  console.log(`${domain}: ${status}`);
});
```

## Declaration principle

okitsok follows the principle that tools are not discovered magically,
but declared explicitly. These descriptor files make okitsok:

- Declarable: Clear structure and capabilities
- Installable: Direct download URLs per platform
- Predictable: Standardized output format
- Trustable: Official source and license

This enables AI agents and orchestrators to integrate okitsok automatically
without manual configuration or guesswork.
