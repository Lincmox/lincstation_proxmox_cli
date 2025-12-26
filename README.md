# lincmox-cli

LincMox CLI to control LincStation N1 LEDs

## Features



## Installation

### From Stable Channel (Recommended)

```bash
echo "deb https://gitea.stela.ovh/api/packages/Lincmox/debian trixie main" | sudo tee /etc/apt/sources.list.d/lincmox.list
sudo apt update
sudo apt install lincmox-cli
```

### From Testing Channel (Pre-releases & Development)

```bash
echo "deb https://gitea.stela.ovh/api/packages/Lincmox/debian trixie testing" | sudo tee /etc/apt/sources.list.d/lincmox-testing.list
sudo apt update
sudo apt install lincmox-cli  # Latest version
sudo apt install lincmox-cli/testing  # Explicitly from testing
```

## Versioning & Release Management

### Commit Message Format

Commits should follow the Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Test changes
- `chore:` - Build, CI, dependency updates

**Example:**
```
fix(i2c): correct initialization timeout

Fixes the I2C initialization hanging on certain devices.
Reduces default timeout from 10s to 5s.

Closes: #42
```

### Version & Tag Format

The package uses Semantic Versioning: `MAJOR.MINOR.PATCH`

**Release Tags:**
```bash
git tag v1.0.0         # Stable release
git tag v1.0.1-1       # Debian revision 1
git tag v1.0.1-2       # Debian revision 2
```

**Pre-release Tags (published to `testing` channel):**
```bash
git tag v1.0.0-alpha1  # Alpha release (converted to 1.0.0~alpha1 in Debian)
git tag v1.0.0-beta1   # Beta release (converted to 1.0.0~beta1 in Debian)
git tag v1.0.0-rc1     # Release candidate (converted to 1.0.0~rc1 in Debian)
```

**Development Builds (automatic from `dev` branch push):**
```
X.Y.Z~dev+<commit_hash>  # e.g., 1.0.0~dev+a1b2c3d
```
- Version is extracted from `pyproject.toml`
- Automatically published to `testing` channel on every commit to `dev`
- Format ensures dev versions are always less than final releases in APT version comparison

### Channels

#### `main` - Stable Releases
- Used for production deployments
- Only stable release tags (e.g., `v1.0.0-1`)
- Recommended for most users

**Add to sources:**
```bash
deb https://gitea.stela.ovh/api/packages/Lincmox/debian trixie main
```

#### `testing` - Development & Pre-releases
- Used for testing new features
- Pre-release tags: `v1.0.0-alpha1`, `v1.0.0-rc1`, etc.
- Automatic builds from `dev` branch: `X.Y.Z~dev+<commit>`
- Not recommended for production

**Add to sources:**
```bash
deb https://gitea.stela.ovh/api/packages/Lincmox/debian trixie testing
```

**Install from testing channel:**
```bash
apt install lincmox-cli/testing
apt install lincmox-cli=1.0.1-1~alpha1
```

### Release Workflow

1. **Development:** Push commits to `dev` branch → Auto-builds to `testing` channel
2. **Pre-release Testing:** Create tag `v1.0.0-rc1` → Published to `testing`
3. **Final Release:** Create tag `v1.0.0-1` → Published to `main`

**Example release process:**
```bash
# Create release tag
git tag v1.0.0-1

# Push tag (triggers workflow)
git push origin v1.0.0-1
```

---

## Development

```bash
export LINCMOX_ENV=dev
```
