# Contributing to ExpressionEngine MCP Server

Thank you for considering contributing to the ExpressionEngine MCP Server project! This document provides guidelines and steps for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ee-mcp.git`
3. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add feature: description"`
7. Push to your branch: `git push origin feature/your-feature-name`
8. Submit a pull request

## Development Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -e .
   ```

3. Copy `env.example` to `.env` and configure it with your ExpressionEngine site details

## Pull Request Guidelines

- Include a clear description of the changes
- Update documentation as needed
- Add/update tests if applicable
- Ensure your code follows the project coding style
- Make sure all tests pass before submitting

## Bug Reports and Feature Requests

Please use GitHub Issues to report bugs or request features.

When reporting a bug, please include:
- A clear title and description
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or screenshots

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License). 