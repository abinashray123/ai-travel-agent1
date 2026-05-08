#!/usr/bin/env python
"""Diagnostic script for AI Travel Agent connectivity issues"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

print("=" * 60)
print("AI TRAVEL AGENT - CONNECTIVITY DIAGNOSTIC")
print("=" * 60)

# 1. SSL Certificate Check
print("\n1️⃣ SSL Certificate Check:")
ca_bundle = Path(__file__).parent / "certs" / "cacert.pem"
if ca_bundle.exists():
    print(f"   ✅ CA Bundle exists: {ca_bundle}")
    print(f"   📊 Size: {ca_bundle.stat().st_size} bytes")
else:
    print(f"   ❌ CA Bundle NOT found: {ca_bundle}")

# 2. Environment Variables
print("\n2️⃣ Environment Variables:")
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY", "NOT SET")
tavily_key = os.getenv("TAVILY_API_KEY", "NOT SET")
serper_key = os.getenv("SERPER_API_KEY", "NOT SET")

print(f"   GROQ_API_KEY: {'✅ SET' if groq_key != 'NOT SET' else '❌ NOT SET'}")
print(f"   TAVILY_API_KEY: {'✅ SET' if tavily_key != 'NOT SET' else '❌ NOT SET'}")
print(f"   SERPER_API_KEY: {'✅ SET' if serper_key != 'NOT SET' else '❌ NOT SET'}")

# 3. Network Connectivity
print("\n3️⃣ Network Connectivity Test:")
try:
    import socket
    
    hosts_to_test = [
        ("google.com", "General Internet"),
        ("api.groq.com", "Groq API"),
        ("api.tavily.com", "Tavily API"),
    ]
    
    for host, desc in hosts_to_test:
        try:
            result = socket.getaddrinfo(host, 443, socket.AF_INET, socket.SOCK_STREAM)
            print(f"   ✅ {desc}: {host} - REACHABLE")
        except socket.gaierror as e:
            print(f"   ❌ {desc}: {host} - FAILED ({e})")
except Exception as e:
    print(f"   ❌ Network test error: {e}")

# 4. Agent Initialization
print("\n4️⃣ Agent & Model Initialization:")
try:
    from src.config.config import GROQ_API_KEY
    from src.agents.travel_agent import model, agent
    print(f"   ✅ Agent initialized successfully")
    print(f"   🤖 Model: llama-3.1-8b-instant")
    print(f"   🔌 Tools: 2 (Tavily Search, Serper Search)")
except Exception as e:
    print(f"   ❌ Agent initialization failed: {e}")

# 5. Python Environment
print("\n5️⃣ Python Environment:")
print(f"   📌 Python: {sys.version.split()[0]}")
print(f"   📦 Virtual Env: {sys.prefix}")

print("\n" + "=" * 60)
print("📋 TROUBLESHOOTING STEPS:")
print("=" * 60)
print("""
If Groq API is unreachable (❌):
  1. Check your internet connection: ping google.com
  2. Check firewall/proxy settings
  3. Try: ipconfig /flushdns (clear DNS cache)
  4. Check if Groq is down: https://status.groq.com

If API keys are missing (❌):
  1. Create .env file with the keys
  2. Restart your terminal/IDE
  3. Verify: python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('GROQ_API_KEY:', os.getenv('GROQ_API_KEY'))"

If SSL issues occur (❌):
  1. The cacert.pem is already configured
  2. If still failing, update: pip install --upgrade certifi
  3. Run again and check certificate paths

Then restart: streamlit run app.py
""")
