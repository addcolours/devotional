#!/usr/bin/env python3
"""
Quick script to fix &nbsp; entities in shiva-stotras.php
"""

# Read the file
with open('output_pages/en/shiva-stotras.php', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace &nbsp; with regular spaces
content = content.replace('&nbsp;', ' ')

# Write back to file
with open('output_pages/en/shiva-stotras.php', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed &nbsp; entities in shiva-stotras.php")
