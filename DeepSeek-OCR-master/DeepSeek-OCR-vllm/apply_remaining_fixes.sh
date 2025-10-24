#!/bin/bash

# Simple script to apply the remaining fixes to gradio_app.py

echo "Applying fixes to gradio_app.py..."

# Fix max_tokens from 8192 to 1536
sed -i 's/max_tokens=8192,/max_tokens=1536,  # Reduced for PDF processing to prevent timeouts/g' gradio_app.py

echo "✓ Applied max_tokens fixes"

# Verify the changes
echo "Verifying changes..."
grep -n "max_tokens=1536" gradio_app.py | head -5

echo "✓ Fixes applied successfully"