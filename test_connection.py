"""
Test script to validate Spike API and Anthropic API connections
Run this before starting the dashboard to ensure everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_env_vars():
    """Test if environment variables are set"""
    print("=" * 60)
    print("Testing Environment Variables")
    print("=" * 60)
    
    required_vars = {
        "SPIKE_API_KEY": os.getenv("SPIKE_API_KEY"),
        "SPIKE_TEAM_ID": os.getenv("SPIKE_TEAM_ID"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY")
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        if not var_value or "your_" in var_value.lower():
            print(f"❌ {var_name}: NOT SET or using placeholder")
            all_set = False
        else:
            # Show masked value
            masked = var_value[:8] + "..." + var_value[-4:] if len(var_value) > 12 else "***"
            print(f"✅ {var_name}: {masked}")
    
    print()
    return all_set


def test_spike_api():
    """Test Spike API connection"""
    print("=" * 60)
    print("Testing Spike API Connection")
    print("=" * 60)
    
    api_key = os.getenv("SPIKE_API_KEY")
    team_id = os.getenv("SPIKE_TEAM_ID")
    
    if not api_key or not team_id:
        print("❌ Cannot test - credentials not set")
        print()
        return False
    
    try:
        headers = {
            "x-api-key": api_key,
            "x-team-id": team_id,
            "Accept": "application/json"
        }
        
        url = "https://api.spike.sh/incidents/triggered"
        
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            incident_count = len(data.get("incidents", []))
            print(f"✅ Connection successful!")
            print(f"   Found {incident_count} triggered incidents")
            print()
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Spike API: {str(e)}")
        print()
        return False


def test_anthropic_api():
    """Test Anthropic API connection"""
    print("=" * 60)
    print("Testing Anthropic API Connection")
    print("=" * 60)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ Cannot test - API key not set")
        print()
        return False
    
    try:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 50,
            "messages": [
                {"role": "user", "content": "Say 'API connection test successful' and nothing else."}
            ]
        }
        
        print("Sending test request to Anthropic API...")
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["content"][0]["text"]
            print(f"✅ Connection successful!")
            print(f"   Response: {message}")
            print()
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Anthropic API: {str(e)}")
        print()
        return False


def main():
    """Run all tests"""
    print()
    print("🧪 Spike Dashboard - Connection Test")
    print()
    
    # Test environment variables
    env_ok = test_env_vars()
    
    if not env_ok:
        print("=" * 60)
        print("⚠️  Please configure your .env file first:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your API credentials")
        print("   3. Run this test again")
        print("=" * 60)
        print()
        sys.exit(1)
    
    # Test APIs
    spike_ok = test_spike_api()
    anthropic_ok = test_anthropic_api()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Spike API:            {'✅ PASS' if spike_ok else '❌ FAIL'}")
    print(f"Anthropic API:        {'✅ PASS' if anthropic_ok else '❌ FAIL'}")
    print()
    
    if env_ok and spike_ok and anthropic_ok:
        print("🎉 All tests passed! You're ready to run the dashboard:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("   See README.md for setup instructions")
    
    print()


if __name__ == "__main__":
    main()
