#!/bin/bash

# Startup script for Spike Dashboard with FastAPI webhook receiver
# This starts both the FastAPI backend and Streamlit frontend

echo "========================================"
echo "Starting Spike Dashboard"
echo "========================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo ""
echo "[1/2] Starting FastAPI webhook receiver on port 8000..."
python api.py &
FASTAPI_PID=$!

sleep 3

echo ""
echo "[2/2] Starting Streamlit dashboard on port 8501..."
streamlit run app_with_api.py &
STREAMLIT_PID=$!

echo ""
echo "========================================"
echo "Dashboard Started!"
echo "========================================"
echo ""
echo "FastAPI Docs:   http://localhost:8000/docs"
echo "Streamlit UI:   http://localhost:8501"
echo ""
echo "Webhook URL:    http://localhost:8000/webhook/spike"
echo ""
echo "PIDs: FastAPI=$FASTAPI_PID, Streamlit=$STREAMLIT_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================"

# Trap Ctrl+C and kill both processes
trap "kill $FASTAPI_PID $STREAMLIT_PID; exit" INT

# Wait for both processes
wait
