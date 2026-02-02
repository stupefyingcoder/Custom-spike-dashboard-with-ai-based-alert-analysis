"""
Spike Dashboard with AI-Based Alert Analysis
A Streamlit dashboard that displays incidents from FastAPI webhook receiver

ENHANCED: Now fetches real-time data from FastAPI backend
"""

import os
import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List, Optional
import json
import time

# Page config
st.set_page_config(
    page_title="Spike Dashboard - AI Alert Analysis",
    page_icon="🚨",
    layout="wide"
)

# API Configuration
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def fetch_incidents_from_api(status: str = None) -> Optional[List[Dict]]:
    """
    Fetch incidents from FastAPI backend
    
    Args:
        status: Filter by status (triggered, acknowledged, resolved)
    
    Returns:
        List of incidents or None on error
    """
    try:
        params = {}
        if status:
            params["status"] = status
        
        response = requests.get(f"{FASTAPI_URL}/incidents", params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return data.get("incidents", [])
        
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Cannot connect to FastAPI backend. Make sure it's running on port 8000")
        return None
    except Exception as e:
        st.error(f"Error fetching incidents: {str(e)}")
        return None


def fetch_incident_stats() -> Optional[Dict]:
    """Fetch incident statistics from FastAPI backend"""
    try:
        response = requests.get(f"{FASTAPI_URL}/incidents/stats", timeout=5)
        response.raise_for_status()
        return response.json()
    except:
        return None


def create_mock_incident_via_api() -> bool:
    """Create a mock incident via FastAPI"""
    try:
        response = requests.post(f"{FASTAPI_URL}/incidents/mock", timeout=5)
        return response.status_code == 200
    except:
        return False


def clear_all_incidents() -> bool:
    """Clear all incidents from FastAPI backend"""
    try:
        response = requests.delete(f"{FASTAPI_URL}/incidents", timeout=5)
        return response.status_code == 200
    except:
        return False


def analyze_with_ai(incidents: List[Dict], analysis_type: str) -> str:
    """
    Analyze incidents using Claude AI or return mock analysis
    
    Args:
        incidents: List of incident dictionaries
        analysis_type: Type of analysis (categorize or summarize)
    
    Returns:
        AI analysis result
    """
    # If no Anthropic key, return mock analysis
    if not ANTHROPIC_API_KEY:
        if analysis_type == "categorize":
            return """
## 🤖 AI Categorization (MOCK DATA - Add ANTHROPIC_API_KEY for real analysis)

### Issue Type Distribution:
- **Database Issues**: 20%
- **Performance Issues**: 40%
- **Infrastructure**: 40%

### Severity Distribution:
- **SEV1 (Critical)**: Requires immediate action
- **SEV2 (High)**: Needs attention within hours
- **SEV3 (Medium)**: Can be scheduled

### Actionable Insights:
⚠️ **URGENT**: Critical issues need immediate attention
📊 Monitor resource usage trends
🔧 Implement automated remediation
            """
        else:  # summarize
            return f"""
## 📋 Executive Summary (MOCK DATA - Add ANTHROPIC_API_KEY for real analysis)

### Overview
Currently tracking {len(incidents)} active incidents across infrastructure.

### Recommendations:
- Address critical issues within 1 hour
- Review resource allocation
- Set up automated monitoring
            """
    
    # Real AI analysis with Anthropic API
    try:
        if analysis_type == "categorize":
            prompt = f"""Analyze these {len(incidents)} incidents and categorize them by:
1. Type of issue (infrastructure, application, network, database, etc.)
2. Severity distribution
3. Common patterns or recurring issues

Incidents data:
{json.dumps(incidents[:10], indent=2)}

Provide a clear, concise categorization with actionable insights."""

        else:  # summarize
            prompt = f"""Summarize these {len(incidents)} incidents:
1. Overall incident summary
2. Key incidents requiring immediate attention
3. Trends and patterns
4. Recommended actions

Incidents data:
{json.dumps(incidents[:10], indent=2)}

Provide a brief executive summary suitable for incident review."""

        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result["content"][0]["text"]
        
    except Exception as e:
        return f"Error during AI analysis: {str(e)}"


def display_incident_card(incident: Dict):
    """Display a single incident as a card"""
    priority = incident.get("priority", "unknown")
    severity = incident.get("severity", "unknown")
    title = incident.get("title", "Untitled Incident")
    source = incident.get("source", "unknown")
    
    # Color coding based on priority
    priority_colors = {
        "p1": "🔴",
        "p2": "🟠",
        "p3": "🟡",
        "p4": "🟢",
        "p5": "⚪"
    }
    
    icon = priority_colors.get(priority, "⚫")
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"### {icon} {title}")
        
        with col2:
            st.metric("Priority", priority.upper())
        
        with col3:
            st.metric("Severity", severity.upper())
        
        with col4:
            st.caption(f"Source: {source}")
        
        # Additional details
        if incident.get("metadata"):
            st.text(f"Details: {incident['metadata']}")
        
        created = incident.get("created_at", "")
        if created:
            st.caption(f"Created: {created}")
        
        st.divider()


def main():
    """Main dashboard application"""
    
    # Header
    st.title("🚨 Spike Dashboard - AI Alert Analysis")
    st.markdown("**Real-time incident monitoring with FastAPI webhook integration**")
    
    # Check FastAPI connection
    try:
        health = requests.get(f"{FASTAPI_URL}/health", timeout=2)
        if health.status_code == 200:
            st.success(f"✅ Connected to FastAPI backend at {FASTAPI_URL}")
        else:
            st.error(f"❌ FastAPI backend health check failed")
    except:
        st.error(f"❌ Cannot connect to FastAPI backend at {FASTAPI_URL}")
        st.info("Start the FastAPI server with: `python api.py`")
        st.stop()
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        incident_status = st.selectbox(
            "Incident Status",
            ["all", "triggered", "acknowledged", "resolved"],
            index=0
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)
        refresh_interval = st.slider("Refresh interval (seconds)", 3, 30, 5)
        
        st.divider()
        
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        st.subheader("🧪 Test Actions")
        
        if st.button("📥 Create Mock Incident", use_container_width=True):
            with st.spinner("Creating mock incident..."):
                if create_mock_incident_via_api():
                    st.success("✅ Mock incident created!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to create mock incident")
        
        if st.button("🗑️ Clear All Incidents", use_container_width=True, type="secondary"):
            if clear_all_incidents():
                st.success("✅ All incidents cleared!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to clear incidents")
        
        st.divider()
        
        st.subheader("📡 Webhook Info")
        st.code(f"{FASTAPI_URL}/webhook/spike", language="text")
        st.caption("Send POST requests here to create incidents")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()
    
    # Fetch incidents
    status_filter = None if incident_status == "all" else incident_status
    
    with st.spinner(f"Fetching incidents..."):
        incidents = fetch_incidents_from_api(status_filter)
        stats = fetch_incident_stats()
    
    if incidents is None:
        st.error("Failed to fetch incidents from FastAPI backend")
        st.info("Make sure the FastAPI server is running: `python api.py`")
        return
    
    # Display metrics from stats
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Incidents", stats.get("total", 0))
        
        with col2:
            p1_count = stats.get("by_priority", {}).get("p1", 0)
            st.metric("Critical (P1)", p1_count)
        
        with col3:
            p2_count = stats.get("by_priority", {}).get("p2", 0)
            st.metric("High (P2)", p2_count)
        
        with col4:
            sev1_count = stats.get("by_severity", {}).get("sev1", 0)
            st.metric("Severity 1", sev1_count)
    
    st.divider()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Incidents", "🤖 AI Categorization", "📝 AI Summary", "📈 Statistics"])
    
    with tab1:
        st.subheader(f"Current Incidents ({len(incidents)})")
        
        if not incidents:
            st.info(f"No incidents found")
            st.markdown("""
            **To add incidents:**
            1. Click "Create Mock Incident" in sidebar
            2. Send POST request to webhook endpoint
            3. Use Spike.sh integration
            """)
        else:
            for incident in incidents:
                display_incident_card(incident)
    
    with tab2:
        st.subheader("🤖 AI-Powered Alert Categorization")
        
        if not incidents:
            st.info("No incidents to categorize")
        else:
            if st.button("🧠 Analyze & Categorize Incidents", use_container_width=True):
                with st.spinner("AI is analyzing incidents..."):
                    analysis = analyze_with_ai(incidents, "categorize")
                    st.markdown(analysis)
    
    with tab3:
        st.subheader("📝 AI-Powered Incident Summary")
        
        if not incidents:
            st.info("No incidents to summarize")
        else:
            if st.button("📋 Generate Summary", use_container_width=True):
                with st.spinner("AI is generating summary..."):
                    summary = analyze_with_ai(incidents, "summarize")
                    st.markdown(summary)
    
    with tab4:
        st.subheader("📈 Incident Statistics")
        
        if stats and stats.get("total", 0) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### By Priority")
                priority_data = stats.get("by_priority", {})
                for priority, count in sorted(priority_data.items()):
                    st.metric(priority.upper(), count)
            
            with col2:
                st.markdown("#### By Severity")
                severity_data = stats.get("by_severity", {})
                for severity, count in sorted(severity_data.items()):
                    st.metric(severity.upper(), count)
            
            st.divider()
            
            st.markdown("#### By Status")
            status_data = stats.get("by_status", {})
            for status, count in sorted(status_data.items()):
                st.metric(status.title(), count)
            
            if stats.get("latest_incident"):
                st.divider()
                st.markdown("#### Latest Incident")
                display_incident_card(stats["latest_incident"])
        else:
            st.info("No statistics available - add some incidents first!")
    
    # Footer
    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
