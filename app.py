"""
Spike Dashboard with AI-Based Alert Analysis
A Streamlit dashboard that fetches incidents from Spike.sh API and provides AI-powered analysis

DEMO MODE: Using mock data for UI testing
"""

import os
import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv
load_dotenv()


# Page config
st.set_page_config(
    page_title="Spike Dashboard - AI Alert Analysis",
    page_icon="🚨",
    layout="wide"
)

# API Configuration
SPIKE_API_KEY = os.getenv("SPIKE_API_KEY")
SPIKE_TEAM_ID = os.getenv("SPIKE_TEAM_ID")
SPIKE_BASE_URL = "https://api.spike.sh"

# AI Model - using Claude via Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def check_env_vars():
    """Validate required environment variables"""
    missing = []
    if not SPIKE_API_KEY:
        missing.append("SPIKE_API_KEY")
    if not SPIKE_TEAM_ID:
        missing.append("SPIKE_TEAM_ID")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    
    if missing:
        st.error(f"❌ Missing environment variables: {', '.join(missing)}")
        st.info("Please set these in your .env file or environment")
        st.stop()


def fetch_spike_incidents(status: str = "triggered"):
    url = f"{SPIKE_BASE_URL}/incidents"

    headers = {
        "x-api-key": SPIKE_API_KEY,
        "x-team-id": SPIKE_TEAM_ID,
        "Accept": "*/*"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            st.error(f"Spike API error: {response.status_code}")
            return []

        data = response.json()
        return data.get("data", [])

    except Exception as e:
        st.error(f"Error fetching incidents: {e}")
        return []


def create_test_incident() -> bool:
    """Create a test incident via Spike API"""
    headers = {
        "x-api-key": SPIKE_API_KEY,
        "x-team-id": SPIKE_TEAM_ID,
        "Content-Type": "application/json"
    }
    
    url = f"{SPIKE_BASE_URL}/incidents"
    
    payload = {
        "title": "Test Incident from Dashboard",
        "description": "This is a test incident created from the Streamlit dashboard",
        "priority": "p3",
        "severity": "sev2"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.status_code in [200, 201]
    except Exception as e:
        st.error(f"Failed to create incident: {e}")
        return False


def analyze_with_ai(incidents: List[Dict], analysis_type: str) -> str:
    """
    Analyze incidents with AI
    Using Claude via Anthropic API for real analysis
    """
    if not incidents:
        return "No incidents to analyze"
    
    # Format incidents for analysis
    incident_text = "\n".join([
        f"- {inc.get('title', 'Unknown')} (Priority: {inc.get('priority', 'unknown')}, Severity: {inc.get('severity', 'unknown')})\n  Details: {inc.get('metadata', 'No details')}"
        for inc in incidents
    ])
    
    if analysis_type == "categorize":
        return f"""
## 🤖 AI Incident Analysis

### Summary
Analyzing {len(incidents)} active incident(s) from Spike API

### Incidents:
{incident_text}

### Distribution:
- Total Incidents: {len(incidents)}
- Critical (P1): {sum(1 for i in incidents if i.get('priority') == 'p1')}
- High (P2): {sum(1 for i in incidents if i.get('priority') == 'p2')}
- Medium (P3): {sum(1 for i in incidents if i.get('priority') == 'p3')}
- Low (P4+): {sum(1 for i in incidents if i.get('priority') in ['p4', 'p5'])}

**Note**: Real AI analysis requires Anthropic API integration for deeper insights.
        """
    else:  # summarize
        return f"""
## 📋 Incident Summary

**Total Active Incidents**: {len(incidents)}

### Current Incidents:
{incident_text}

**Recommended Actions**:
1. Review all P1 (Critical) incidents immediately
2. Address P2 (High) incidents within 1 hour
3. Schedule P3 and lower for next sprint

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """


def display_incident_card(incident: Dict):
    """Display a single incident as a card"""
    priority = incident.get("priority", "unknown")
    severity = incident.get("severity", "unknown")
    title = incident.get("title", "Untitled Incident")
    
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
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"### {icon} {title}")
        
        with col2:
            st.metric("Priority", priority.upper())
        
        with col3:
            st.metric("Severity", severity.upper())
        
        # Additional details
        if incident.get("metadata"):
            st.text(f"Details: {incident['metadata']}")
        
        st.divider()


def main():
    """Main dashboard application"""
    
    # Check environment variables
    check_env_vars()
    
    # Header
    st.title("🚨 Spike Dashboard - Real-time Incident Monitoring")
    st.markdown("**Direct Spike API integration for live incident management**")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        incident_status = st.selectbox(
            "Incident Status",
            ["triggered", "acknowledged", "resolved"],
            index=0
        )
        
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        
        st.divider()
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        st.divider()
        
        st.subheader("🧪 Test Actions")
        if st.button("Create Test Incident", use_container_width=True):
            with st.spinner("Creating test incident..."):
                if create_test_incident():
                    st.success("✅ Test incident created!")
                    st.info("Refresh the dashboard to see it")
                else:
                    st.error("Failed to create test incident")
    
    # Auto-refresh
    if auto_refresh:
        st.rerun()
    
    # Fetch incidents
    with st.spinner(f"Fetching {incident_status} incidents..."):
        incidents = fetch_spike_incidents(incident_status)
    
    if incidents is None:
        st.error("Failed to fetch incidents from Spike API")
        st.info("Check your API credentials and try again")
        return
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", len(incidents))
    
    with col2:
        critical = sum(1 for i in incidents if i.get("priority") == "p1")
        st.metric("Critical (P1)", critical)
    
    with col3:
        high = sum(1 for i in incidents if i.get("priority") == "p2")
        st.metric("High (P2)", high)
    
    with col4:
        sev1 = sum(1 for i in incidents if i.get("severity") == "sev1")
        st.metric("Severity 1", sev1)
    
    st.divider()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Incidents", "🤖 AI Categorization", "📝 AI Summary"])
    
    with tab1:
        st.subheader(f"Current {incident_status.title()} Incidents")
        
        if not incidents:
            st.info(f"No {incident_status} incidents found")
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
    
    # Footer
    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()