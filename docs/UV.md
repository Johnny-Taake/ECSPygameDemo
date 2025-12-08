# Using `uv` (or plain `pip`) with this project

You can work with this project in two ways:

1. **Recommended:** use [`uv`](https://docs.astral.sh/uv/getting-started/installation/) as the package/dependency manager.
2. **Alternative:** use classic `pip` + virtualenv.

Both approaches are compatible with this repo.

---

## 1. Install `uv` (recommended)

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or, if you prefer wget:
wget -qO- https://astral.sh/uv/install.sh | sh
````

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, make sure `uv` is on your `PATH` (usually `~/.local/bin` on Unix-like systems, or `%USERPROFILE%\.local\bin` on Windows).

Full installation options and package-manager alternatives are described here:
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

## 2. Alternative: use `pip` instead of `uv`

If you don’t want to install `uv`, you can run the project with standard `pip`:

### 2.1. Create and activate a virtual environment

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2.2. Install dependencies from `requirements.txt`

If you’ve exported requirements (or use the one provided):

```bash
pip install -r requirements.txt
```

Then run the app:

```bash
python main.py
```

---

## 3. Using `uv` with this project

Below are the common `uv` flows for this repo.

### 3.1. Install main app dependencies only

```bash
uv sync
```

### 3.2. Install with build dependencies (for running `build.py`)

```bash
uv sync --extra build
```

### 3.3. Install with test dependencies

```bash
uv sync --extra test
```

### 3.4. Install with dev dependencies

```bash
uv sync --extra dev
```

### 3.5. Install everything (all extras)

```bash
uv sync --all-extras
```

---

## 4. Running things with `uv`

### 4.1. Run your app

```bash
uv run python main.py
```

### 4.2. Run build script

```bash
uv run --extra build python build.py
```

### 4.3. Run tests

```bash
uv run --extra test pytest
```

If you prefer plain `pip`, you can always translate these to:

```bash
python main.py
python build.py
pytest
```
