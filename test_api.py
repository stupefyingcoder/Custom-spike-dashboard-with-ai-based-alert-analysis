"""
Test script for FastAPI webhook integration
Tests all endpoints and webhook functionality
"""

import requests
import time
import json

FASTAPI_URL = "http://localhost:8000"

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_health():
    """Test health endpoint"""
    print_header("Testing Health Endpoint")
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to FastAPI: {str(e)}")
        print("   Make sure to start FastAPI: python api.py")
        return False

def test_create_mock_incident():
    """Test creating mock incident"""
    print_header("Testing Mock Incident Creation")
    try:
        response = requests.post(f"{FASTAPI_URL}/incidents/mock", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Mock incident created")
            print(f"   Incident: {data['incident']['title']}")
            print(f"   ID: {data['incident']['id']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_webhook_spike():
    """Test Spike webhook endpoint"""
    print_header("Testing Spike Webhook Endpoint")
    
    incident = {
        "title": "Test Alert from Test Script",
        "priority": "p2",
        "severity": "sev2",
        "metadata": "This is a test incident created by test_api.py",
        "status": "triggered"
    }
    
    try:
        response = requests.post(
            f"{FASTAPI_URL}/webhook/spike",
            json=incident,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Webhook accepted")
            print(f"   Incident ID: {data['incident_id']}")
            print(f"   Total incidents: {data['total_incidents']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_incidents():
    """Test getting incidents"""
    print_header("Testing Get Incidents Endpoint")
    try:
        response = requests.get(f"{FASTAPI_URL}/incidents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['total']} incidents")
            
            if data['incidents']:
                print("\n   Latest incident:")
                latest = data['incidents'][0]
                print(f"   Title: {latest['title']}")
                print(f"   Priority: {latest['priority']}")
                print(f"   Severity: {latest['severity']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_stats():
    """Test statistics endpoint"""
    print_header("Testing Statistics Endpoint")
    try:
        response = requests.get(f"{FASTAPI_URL}/incidents/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics retrieved")
            print(f"   Total incidents: {stats['total']}")
            print(f"   By priority: {stats['by_priority']}")
            print(f"   By severity: {stats['by_severity']}")
            print(f"   By status: {stats['by_status']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_filtered_incidents():
    """Test filtered incident retrieval"""
    print_header("Testing Filtered Incidents")
    try:
        # Test status filter
        response = requests.get(
            f"{FASTAPI_URL}/incidents",
            params={"status": "triggered", "limit": 5},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['total']} triggered incidents")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_custom_webhook():
    """Test custom webhook with validation"""
    print_header("Testing Custom Webhook (Validated)")
    
    incident = {
        "title": "Custom Webhook Test",
        "priority": "p3",
        "severity": "sev3",
        "metadata": "Testing custom webhook with Pydantic validation"
    }
    
    try:
        response = requests.post(
            f"{FASTAPI_URL}/webhook/custom",
            json=incident,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Custom webhook accepted")
            print(f"   Incident ID: {data['incident_id']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SPIKE DASHBOARD API TEST SUITE" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {}
    
    # Run tests
    results['Health Check'] = test_health()
    
    if not results['Health Check']:
        print("\n❌ FastAPI is not running. Please start it with: python api.py")
        return
    
    time.sleep(0.5)
    results['Mock Incident'] = test_create_mock_incident()
    
    time.sleep(0.5)
    results['Spike Webhook'] = test_webhook_spike()
    
    time.sleep(0.5)
    results['Custom Webhook'] = test_custom_webhook()
    
    time.sleep(0.5)
    results['Get Incidents'] = test_get_incidents()
    
    time.sleep(0.5)
    results['Statistics'] = test_get_stats()
    
    time.sleep(0.5)
    results['Filtered Query'] = test_filtered_incidents()
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your FastAPI integration is working!")
        print("\nNext steps:")
        print("1. Start Streamlit: streamlit run app_with_api.py")
        print("2. Open: http://localhost:8501")
        print("3. Test the dashboard with the created incidents")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n")

if __name__ == "__main__":
    main()
