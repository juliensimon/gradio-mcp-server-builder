#!/bin/bash

# Serve the Gradio MCP Server Builder documentation
echo "🚀 Starting Gradio MCP Server Builder documentation server..."
echo "📖 Documentation will be available at: http://127.0.0.1:8001"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

mkdocs serve --dev-addr 127.0.0.1:8001
