# Publishing Guide

This document provides instructions for publishing the IEBPTPCH PDS Extractor to PyPI and maintaining the GitHub repository.

## Prerequisites

1. **Python Environment**: Python 3.6 or higher
2. **Build Tools**: Install build dependencies
   ```bash
   pip install build twine
   ```
3. **PyPI Account**: Create accounts on:
   - [TestPyPI](https://test.pypi.org/) (for testing)
   - [PyPI](https://pypi.org/) (for production)

## Building the Package

1. **Clean Previous Builds**:
   ```bash
   rm -rf dist/ build/ src/*.egg-info/
   ```

2. **Build the Package**:
   ```bash
   python -m build
   ```

   This creates:
   - `dist/iebptpch_pds_extractor-X.X.X.tar.gz` (source distribution)
   - `dist/iebptpch_pds_extractor-X.X.X-py3-none-any.whl` (wheel distribution)

## Testing the Package

### Test on TestPyPI

1. **Upload to TestPyPI**:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

2. **Install from TestPyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ iebptpch-pds-extractor
   ```

3. **Test Installation**:
   ```bash
   iebptpch-pds-extractor --help
   ```

### Local Testing

1. **Install in Development Mode**:
   ```bash
   pip install -e .
   ```

2. **Run Tests**:
   ```bash
   python -m pytest tests/
   ```

3. **Test Command Line**:
   ```bash
   iebptpch-pds-extractor --help
   ```

## Publishing to PyPI

### First Time Setup

1. **Configure PyPI Credentials**:
   Create `~/.pypirc`:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-your-api-token-here

   [testpypi]
   username = __token__
   password = pypi-your-test-api-token-here
   ```

### Publishing Steps

1. **Update Version**: Update version in:
   - `pyproject.toml`
   - `setup.py`
   - `src/iebptpch_pds_extractor/__init__.py`

2. **Update Changelog**: Add new version entry to `CHANGELOG.md`

3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Release version X.X.X"
   git tag vX.X.X
   git push origin main --tags
   ```

4. **Build and Upload**:
   ```bash
   rm -rf dist/ build/ src/*.egg-info/
   python -m build
   python -m twine upload dist/*
   ```

## GitHub Repository Setup

### Initial Setup

1. **Create Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/arunkumars-mf/iebptpch-pds-extractor.git
   git push -u origin main
   ```

2. **Configure Repository Settings**:
   - Add description: "Extract PDS members from IEBPTPCH output files with support for both ASCII and EBCDIC formats"
   - Add topics: `mainframe`, `pds`, `iebptpch`, `ebcdic`, `ascii`, `extractor`, `ibm`, `z-os`, `mvs`
   - Enable Issues and Wiki if desired

### Release Management

1. **Create GitHub Release**:
   - Go to repository → Releases → Create a new release
   - Tag version: `vX.X.X`
   - Release title: `Version X.X.X`
   - Description: Copy from CHANGELOG.md
   - Attach built distributions from `dist/`

2. **Automated Releases** (Optional):
   Set up GitHub Actions for automated testing and publishing.

## Version Management

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Checklist Before Publishing

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version numbers are updated consistently
- [ ] CHANGELOG.md is updated
- [ ] Examples work with new version
- [ ] Package builds without errors
- [ ] Package installs and runs correctly
- [ ] Git repository is clean and committed
- [ ] Tags are created and pushed

## Post-Publication

1. **Verify Installation**:
   ```bash
   pip install iebptpch-pds-extractor
   iebptpch-pds-extractor --help
   ```

2. **Update Documentation**: Ensure all links and references are correct

3. **Announce**: Consider announcing on relevant forums or communities

## Troubleshooting

### Common Issues

1. **Build Errors**: Check `pyproject.toml` and `setup.py` syntax
2. **Upload Errors**: Verify PyPI credentials and package name availability
3. **Import Errors**: Check package structure and `__init__.py` files
4. **Version Conflicts**: Ensure version is higher than existing versions

### Getting Help

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
