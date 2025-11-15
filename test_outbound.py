#!/usr/bin/env python3
"""
Test script for making outbound calls
"""
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("SERVER_URL", "http://localhost:8000")


def make_outbound_call(phone_number: str):
    """Make an outbound call to the specified phone number"""
    url = f"{API_URL}/api/calls/outbound"
    
    payload = {
        "phone_number": phone_number
    }
    
    print(f"Making outbound call to {phone_number}...")
    print(f"POST {url}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("\n✅ Success!")
        print(f"Call SID: {result.get('call_sid')}")
        print(f"Status: {result.get('status')}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def check_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        health = response.json()
        print("API Health Check:")
        print(f"  Status: {health.get('status')}")
        print(f"  Services:")
        for service, status in health.get('services', {}).items():
            status_icon = "✅" if status else "❌"
            print(f"    {status_icon} {service}: {status}")
        return health.get('status') == 'healthy'
    except Exception as e:
        print(f"❌ API not reachable: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_outbound.py <phone_number>")
        print("Example: python test_outbound.py +1234567890")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    
    # Validate phone number format (basic check)
    if not phone_number.startswith('+'):
        print("⚠️  Warning: Phone number should be in E.164 format (e.g., +1234567890)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Check health first
    print("Checking API health...\n")
    if not check_health():
        print("\n⚠️  API health check failed. Make sure the server is running.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print()
    make_outbound_call(phone_number)

