#!/bin/bash

# Comprehensive auto-fix script for all code quality issues

echo "🔧 Auto-fixing all code quality issues..."

# Python files
echo "🐍 Formatting Python files..."
black --line-length=88 .
autopep8 --in-place --recursive --max-line-length=88 --aggressive --aggressive .
isort --profile=black --line-length=88 .

# Remove unused imports and fix basic issues
echo "🧹 Cleaning up Python files..."
# Use autoflake to remove unused imports
pip install autoflake
autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .

# Markdown files
echo "📝 Formatting Markdown files..."
prettier --write "**/*.md" --prose-wrap=always
markdownlint --fix .

# JSON files
echo "📄 Formatting JSON files..."
prettier --write "**/*.json"

# YAML files
echo "📋 Formatting YAML files..."
prettier --write "**/*.yml" "**/*.yaml"

# Fix common issues
echo "🔧 Fixing common issues..."

# Fix trailing whitespace
find . -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" | xargs sed -i '' 's/[[:space:]]*$//'

# Ensure files end with newline
find . -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" | while read file; do
    if [ -s "$file" ] && [ "$(tail -c1 "$file" | wc -l)" -eq 0 ]; then
        echo "" >> "$file"
    fi
done

echo "✅ Auto-fix complete!"
echo ""
echo "To check for remaining issues:"
echo "  flake8 --max-line-length=88 ."
echo "  markdownlint ." 