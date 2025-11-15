#!/usr/bin/env python3
"""
Test script for API endpoints
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("SERVER_URL", "http://localhost:8000")


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_root():
    """Test root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_conversations():
    """Test conversations endpoint"""
    print("Testing /api/conversations endpoint...")
    response = requests.get(f"{API_URL}/api/conversations")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_outbound_call(phone_number: str):
    """Test outbound call endpoint"""
    print(f"Testing /api/calls/outbound with {phone_number}...")
    payload = {"phone_number": phone_number}
    response = requests.post(f"{API_URL}/api/calls/outbound", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code in [200, 201]


if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("Rap Beat Call Bot API Tests")
    print("=" * 50)
    print()
    
    # Test basic endpoints
    test_root()
    test_health()
    test_conversations()
    
    # Test outbound call if phone number provided
    if len(sys.argv) > 1:
        phone_number = sys.argv[1]
        test_outbound_call(phone_number)
    else:
        print("Skipping outbound call test (no phone number provided)")
        print("Usage: python test_api.py [phone_number]")
    
    print("=" * 50)
    print("Tests completed!")

