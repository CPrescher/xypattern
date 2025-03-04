# xypattern Documentation

This directory contains the Sphinx documentation for the xypattern project.

## Building the Documentation

To build the documentation:

1. Make sure you have the development dependencies installed:
   ```bash
   poetry install --with dev
   ```

2. Navigate to the docs directory:
   ```bash
   cd docs
   ```

3. Build the HTML documentation:
   ```bash
   make html
   ```

4. The built documentation will be available in the `_build/html` directory.

## Viewing the Documentation

After building, you can view the documentation by opening `_build/html/index.html` in your web browser.

## Documentation Structure

- `index.rst`: Main documentation page
- `installation.rst`: Installation instructions
- `usage.rst`: Usage examples
- `api.rst`: API reference
- `contributing.rst`: Contributing guidelines
- `changelog.rst`: Version history

## Adding New Documentation

To add new documentation:

1. Create a new `.rst` file in the `docs` directory
2. Add the file to the toctree in `index.rst`
3. Rebuild the documentation 