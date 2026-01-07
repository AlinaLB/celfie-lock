# Contributing to Celfie Lock

First off, thank you for considering contributing to Celfie Lock! It's people like you that make Celfie Lock such a great tool for image protection.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this standard. Please be respectful and considerate in all interactions.

### Our Standards

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- A GitHub account

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/celfie-lock.git
   cd celfie-lock
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-owner/celfie-lock.git
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting a bug, include:**
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, library versions)
- Sample images if relevant (without sensitive data)
- Error messages or logs

### Suggesting Features

We love feature suggestions! Please:
- Use a clear, descriptive title
- Provide a detailed description of the proposed feature
- Explain why this feature would be useful
- Include examples or mockups if applicable

### Code Contributions

#### Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

#### Types of Contributions We Welcome

- Bug fixes
- New steganography algorithms
- Watermark enhancements
- Performance improvements
- Documentation improvements
- Test coverage expansion
- Accessibility improvements

## Development Setup

### Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=celfie

# Run specific test file
python -m pytest tests/test_encoding.py
```

### Code Quality

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking (if applicable)
mypy celfie.py
```

## Pull Request Process

### Before Submitting

1. **Update your fork** with the latest upstream changes:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following our style guidelines

4. **Test your changes** thoroughly

5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: brief description"
   ```

### Submitting Your PR

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub

3. Fill out the PR template with:
   - Description of changes
   - Related issue numbers
   - Screenshots (if UI changes)
   - Testing steps

### PR Review Process

- A maintainer will review your PR within a few days
- Address any feedback or requested changes
- Once approved, your PR will be merged

### After Your PR is Merged

- Delete your feature branch
- Pull the latest changes to your main branch
- Celebrate your contribution!

## Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Good
def encode_message(input_path, output_path, message, **options):
    """
    Hide a message inside an image using steganography.
    
    Args:
        input_path: Path to the source image
        output_path: Path for the output image
        message: The message to hide
        **options: Additional encoding options
    
    Returns:
        bool: True if successful
    """
    pass

# Avoid
def encode(i, o, m, **opts):
    pass
```

### Naming Conventions

- **Functions/Methods**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase`

### Documentation

- All public functions must have docstrings
- Use type hints where practical
- Update README.md for new features
- Add inline comments for complex logic

### Commit Messages

Use clear, descriptive commit messages:

```
# Good
Add watermark opacity support with 4 preset levels
Fix PNG output forcing for JPEG inputs
Update README with API reference table

# Avoid
fix stuff
update
wip
```

## Community

### Get Help

- Open a GitHub issue for bugs or questions
- Check existing issues and discussions first

### Stay Connected

- Star the repository to show support
- Watch for updates and new releases
- Share Celfie Lock with others

### Support the Project

If Celfie Lock has helped you, consider:
- [Supporting on Ko-fi](https://ko-fi.com/celfielock)
- Spreading the word
- Contributing code or documentation

---

## Thank You!

Your contributions make Celfie Lock better for everyone. Whether it's a bug report, feature suggestion, or code contribution - every bit helps!

<p align="center">
  <a href="https://ko-fi.com/celfielock">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support on Ko-fi">
  </a>
</p>
