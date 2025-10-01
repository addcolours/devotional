print("Starting Durga scraper test...")
print("This is a test to see if Python output works")

import sys
print(f"Python version: {sys.version}")

try:
    import requests
    print("requests module: OK")
except ImportError:
    print("requests module: NOT FOUND")

try:
    from bs4 import BeautifulSoup
    print("BeautifulSoup module: OK")
except ImportError:
    print("BeautifulSoup module: NOT FOUND")

print("Test completed!")
