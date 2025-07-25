#!/bin/bash

# Script to run slow tests
# These tests are excluded from CI due to their long runtime

echo "Running slow tests..."
echo "These tests may take several minutes to complete."
echo ""

# Run slow tests with longer timeout
python -m pytest tests/slow/ -v --tb=short --timeout=600

echo ""
echo "Slow tests completed!"
