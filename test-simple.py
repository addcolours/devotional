#!/usr/bin/env python3
print("Script is running!")
print("Testing basic functionality...")

import os
print(f"Current directory: {os.getcwd()}")

# Test file existence
test_file = "output_pages/en/sree-durga-sahasra-nama-stotram-english.php"
if os.path.exists(test_file):
    print(f"✅ File exists: {test_file}")
else:
    print(f"❌ File not found: {test_file}")

print("Script completed successfully!")
