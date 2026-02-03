# Publication Checklist - okitsok 1.0.0

## Step 1: Replace OWNER with your GitHub username

Files to modify:
- `ai-tool.yaml` (3 occurrences)
- `okitsok.tool.json` (3 occurrences)

Replace `OWNER` with your actual GitHub username.

## Step 2: Verify everything works

```bash
# Test the binary
.\dist\okitsok.exe google --json

# Test the Python module
py -m okitsok.cli example --json
```

## Step 3: Final commit

```bash
git add .
git commit -m "Release 1.0.0"
git tag -a v1.0.0 -m "okitsok 1.0.0 - Stable release"
git push origin main --tags
```

## Step 4: Create GitHub Release

1. Go to https://github.com/coconut971/okitsok/releases/new
2. Choose tag: v1.0.0
3. Title: okitsok 1.0.0
4. Description: Copy content from RELEASE.md
5. Upload binaries:
   - okitsok.exe (Windows) - already ready in dist/
   - okitsok (macOS) - to be generated on macOS
   - okitsok (Linux) - to be generated on Linux
6. Check "Set as the latest release"
7. Publish

## Step 5: Post-publication verification

Test that URLs in ai-tool.yaml work:

```bash
# Windows
curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok.exe -o okitsok.exe

# macOS/Linux
curl -L https://github.com/coconut971/okitsok/releases/latest/download/okitsok -o okitsok
chmod +x okitsok
```

## Optional: PyPI publication

If you want to publish to PyPI:

```bash
py -m build
py -m twine upload dist/*.tar.gz dist/*.whl
```

Note: Requires PyPI account and twine configuration.

## After publication

okitsok officially exists when:
- Tag v1.0.0 is pushed
- GitHub release is created
- Windows binary is downloadable

Agents and frameworks can then:
1. Read ai-tool.yaml
2. Download the binary
3. Use okitsok automatically

## Estimated time

- Steps 1-3: 5 minutes
- Step 4: 10 minutes
- Verification: 5 minutes

Total: 20 minutes (without macOS/Linux binary generation)
