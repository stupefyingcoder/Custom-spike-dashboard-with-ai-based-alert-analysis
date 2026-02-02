# 🚨 Spike Dashboard with AI-Based Alert Analysis

A powerful Streamlit web dashboard that fetches incident alerts from Spike.sh API and provides AI-powered categorization and summarization using Claude AI.

## 🎯 Features

- **Real-time Incident Monitoring**: Fetch triggered, acknowledged, or resolved incidents from Spike.sh
- **AI-Powered Analysis**: 
  - Automatic alert categorization by type, severity, and patterns
  - Executive incident summaries with actionable insights
- **Interactive Dashboard**: Clean, modern UI with real-time metrics
- **Test Incident Creation**: Built-in testing capability
- **Secure**: All credentials managed via environment variables

## 📋 Prerequisites

- Python 3.8+
- Spike.sh account with API access
- Anthropic API key (for Claude AI)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd spike-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example env file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
SPIKE_API_KEY=your_spike_api_key_here
SPIKE_TEAM_ID=your_team_id_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Where to get these:**

- **Spike API Key & Team ID**: 
  1. Go to [Spike.sh Settings](https://app.spike.sh/settings/api)
  2. Generate an API key
  3. Find your Team ID in the same section

- **Anthropic API Key**:
  1. Visit [Anthropic Console](https://console.anthropic.com/)
  2. Create an account or sign in
  3. Generate an API key

### 4. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 🎨 Dashboard Features

### Main Dashboard View
- **Metrics Panel**: Total incidents, critical alerts (P1), high priority (P2), and severity 1 counts
- **Status Filter**: View triggered, acknowledged, or resolved incidents
- **Auto-refresh**: Optional 30-second auto-refresh

### Three Main Tabs

1. **📊 Incidents Tab**
   - View all current incidents
   - Color-coded priority indicators
   - Priority and severity metrics for each incident

2. **🤖 AI Categorization Tab**
   - Click "Analyze & Categorize Incidents"
   - AI categorizes by issue type, severity, and patterns
   - Identifies recurring problems

3. **📝 AI Summary Tab**
   - Click "Generate Summary"
   - Executive summary of all incidents
   - Key incidents requiring attention
   - Trend analysis and recommendations

### Test Features
- **Create Test Incident**: Generate sample incidents for testing
- Built-in error handling for API failures

## 📁 Project Structure

```
spike-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your actual credentials (not committed)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SPIKE_API_KEY` | ✅ | Your Spike.sh API key |
| `SPIKE_TEAM_ID` | ✅ | Your Spike.sh Team ID |
| `ANTHROPIC_API_KEY` | ✅ | Your Anthropic API key for Claude |

### Spike API Endpoints Used

- `GET /incidents/{status}` - Fetch incidents (triggered/acknowledged/resolved)
- `POST /incidents/create` - Create test incidents

## 🧪 Testing

### Create Test Incidents

1. Click "Create Test Incident" in the sidebar
2. Refresh the dashboard to see the new incident
3. Use AI analysis features to categorize/summarize

### Manual API Testing

```python
import requests

headers = {
    "x-api-key": "your_api_key",
    "x-team-id": "your_team_id"
}

response = requests.get(
    "https://api.spike.sh/incidents/triggered",
    headers=headers
)
print(response.json())
```

## 🐛 Troubleshooting

### "Missing environment variables" error
- Ensure `.env` file exists in project root
- Verify all three variables are set correctly
- Don't add quotes around values in `.env`

### "Error fetching incidents" 
- Verify your Spike API key is valid
- Check your Team ID is correct
- Ensure you have incidents in your Spike account

### "AI analysis error"
- Verify Anthropic API key is valid
- Check you have API credits available
- Network connectivity to Anthropic API

## 📊 Sample Output

When running successfully, you'll see:

```
Total Incidents: 5
Critical (P1): 1
High (P2): 2
Severity 1: 1

Incidents displayed with priority indicators:
🔴 Critical database outage - Priority: P1, Severity: SEV1
🟠 API response time degradation - Priority: P2, Severity: SEV2
...
```

AI Categorization example:
```
Issue Type Distribution:
- Infrastructure: 2 incidents
- Application: 2 incidents
- Database: 1 incident

Severity Analysis:
- SEV1: 1 critical issue requiring immediate attention
- SEV2: 3 high-priority issues
...
```

## 🔒 Security Best Practices

- ✅ Never commit `.env` file to Git
- ✅ Use environment variables for all secrets
- ✅ Keep API keys secure and rotate regularly
- ✅ Use minimum required API permissions

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use and modify

## 🆘 Support

- **Spike.sh Docs**: https://docs.spike.sh
- **Anthropic Docs**: https://docs.anthropic.com
- **Issues**: Open an issue in this repository

## 🎉 Demo

Run the dashboard and create test incidents to see it in action:

```bash
# Start the dashboard
streamlit run app.py

# In the UI:
# 1. Click "Create Test Incident" in sidebar
# 2. Refresh the dashboard
# 3. Click "Analyze & Categorize Incidents"
# 4. See AI-powered insights!
```

---

Built with ❤️ using Streamlit, Spike.sh API, and Claude AI
