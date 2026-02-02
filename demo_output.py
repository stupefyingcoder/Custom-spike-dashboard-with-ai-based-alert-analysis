"""
Demo Output Example
This file shows what the dashboard looks like when running
"""

DEMO_OUTPUT = """
================================================================================
🚨 SPIKE DASHBOARD - AI ALERT ANALYSIS
================================================================================

Dashboard URL: http://localhost:8501

================================================================================
METRICS PANEL
================================================================================
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Total Incidents │  Critical (P1)  │   High (P2)     │   Severity 1    │
│       5         │        1        │        2        │        1        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

================================================================================
INCIDENTS TAB - Current Triggered Incidents
================================================================================

🔴 Database Connection Pool Exhausted
   Priority: P1  |  Severity: SEV1
   Details: Production database unable to accept new connections
   ───────────────────────────────────────────────────────────────

🟠 API Response Time Degradation  
   Priority: P2  |  Severity: SEV2
   Details: Average response time increased from 200ms to 2s
   ───────────────────────────────────────────────────────────────

🟠 Memory Usage High on App Server
   Priority: P2  |  Severity: SEV2
   Details: Memory usage at 87%, approaching threshold
   ───────────────────────────────────────────────────────────────

🟡 Disk Space Low on Backup Server
   Priority: P3  |  Severity: SEV3
   Details: 15% free space remaining on /backup volume
   ───────────────────────────────────────────────────────────────

🟢 Certificate Expiring Soon
   Priority: P4  |  Severity: SEV3
   Details: SSL certificate expires in 25 days
   ───────────────────────────────────────────────────────────────

================================================================================
AI CATEGORIZATION TAB
================================================================================

Button: [🧠 Analyze & Categorize Incidents]

After clicking:

AI Analysis Results:
────────────────────

INCIDENT CATEGORIZATION

1. Issue Type Distribution:
   • Database Issues: 1 incident (20%)
     - Connection pool exhaustion
   
   • Performance Issues: 2 incidents (40%)
     - API response degradation
     - Memory usage warnings
   
   • Infrastructure: 2 incidents (40%)
     - Disk space concerns
     - Certificate management

2. Severity Distribution:
   • SEV1 (Critical): 1 incident - requires immediate action
   • SEV2 (High): 2 incidents - needs attention within hours
   • SEV3 (Medium): 2 incidents - can be scheduled

3. Common Patterns Identified:
   • Resource exhaustion theme across 3 incidents
   • All production-related systems affected
   • No network-layer issues detected
   
4. Actionable Insights:
   ⚠️  URGENT: Database connection pool needs immediate scaling
   📊 Monitor memory usage trends to prevent cascading failures
   🔧 Implement automated disk cleanup on backup server
   📅 Schedule certificate renewal process

================================================================================
AI SUMMARY TAB
================================================================================

Button: [📋 Generate Summary]

After clicking:

Executive Incident Summary:
──────────────────────────

OVERVIEW
Currently tracking 5 active incidents across production infrastructure,
with 1 critical issue requiring immediate attention and 2 high-priority
issues needing resolution within the next few hours.

KEY INCIDENTS REQUIRING IMMEDIATE ATTENTION

1. 🔴 Database Connection Pool Exhausted (P1/SEV1)
   Status: Critical - Production database at capacity
   Impact: New user connections failing, service degradation
   Action: Scale connection pool immediately, investigate leak

2. 🟠 API Response Time Degradation (P2/SEV2)
   Status: High priority - Performance impact
   Impact: User experience degraded, potential timeout cascade
   Action: Profile application, identify bottleneck

TRENDS AND PATTERNS

• Resource Pressure: 60% of incidents relate to resource exhaustion
  (database connections, memory, disk space)
  
• Proactive Alerts: 2 incidents are preventive (disk space, cert expiry)
  showing good monitoring coverage

• No Security Incidents: All issues are operational/performance related

RECOMMENDED ACTIONS

Immediate (Next 1 hour):
  1. Scale database connection pool
  2. Investigate API performance regression
  
Short-term (Next 24 hours):
  3. Review and adjust memory limits on app servers
  4. Implement disk space auto-cleanup
  
Preventive:
  5. Set up automated certificate renewal
  6. Review resource allocation across infrastructure

OVERALL HEALTH: ⚠️ DEGRADED
Recommendation: Address P1 issue immediately to prevent service outage

================================================================================
API RESPONSE EXAMPLE
================================================================================

GET https://api.spike.sh/incidents/triggered

Response (200 OK):
{
  "incidents": [
    {
      "id": "inc_abc123",
      "title": "Database Connection Pool Exhausted",
      "priority": "p1",
      "severity": "sev1",
      "status": "triggered",
      "created_at": "2025-01-31T10:30:00Z",
      "metadata": "Production database unable to accept new connections"
    },
    {
      "id": "inc_def456",
      "title": "API Response Time Degradation",
      "priority": "p2",
      "severity": "sev2",
      "status": "triggered",
      "created_at": "2025-01-31T11:15:00Z",
      "metadata": "Average response time increased from 200ms to 2s"
    }
  ],
  "total": 5
}

================================================================================
TEST INCIDENT CREATION
================================================================================

Click: [Create Test Incident]

Response:
✅ Test incident created!
ℹ️  Refresh the dashboard to see it

New incident appears:
🟡 Test Alert - Dashboard Demo - 2025-01-31 15:45:32
   Priority: P3  |  Severity: SEV2
   Details: This is a test incident created from the Spike Dashboard demo

================================================================================
"""

if __name__ == "__main__":
    print(DEMO_OUTPUT)
