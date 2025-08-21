# CRUSH.md - Caffeine Bedtime Calculator

## Commands
- **Run**: `uv run cbc <target> '<time:amount>' ...` or `uv run python cbc.py <target> '<time:amount>' ...`
- **Install deps**: `uv sync`
- **Add dependency**: `uv add <package>`
- **Update deps**: `uv lock --upgrade`
- **Test**: No test framework configured
- **Lint**: No linter configured (consider adding ruff)
- **Build**: `uv build`

## Code Style
- **Python version**: 3.13+ (shebang specifies 3.13)
- **Package manager**: uv (modern Python package manager)
- **Imports**: Standard library first, then third-party (click)
- **Constants**: UPPER_CASE with underscores
- **Functions**: snake_case with descriptive names
- **Variables**: snake_case, descriptive (e.g., `running_caffeine`, `target_caf_mg`)
- **Docstrings**: Triple quotes, brief description
- **Comments**: Block comments for formulas/calculations
- **Formatting**: 4-space indentation, line breaks around functions
- **Click**: Use for CLI with @click.command() decorator
- **Math**: Use math module for logarithms, explicit float() conversions
- **DateTime**: Use datetime module, format strings for display
- **Error handling**: Basic validation (split operations assume correct format)

## Project Structure
- Standard Python package structure with src/ layout
- Main module: `src/caffeine_bedtime_calculator/main.py`
- Uses Click for command-line interface
- Calculates caffeine decay using half-life of 5.7 hours
- Supports multiple caffeine intake times/amounts
- Configured as installable package with entry point (`cbc` command)