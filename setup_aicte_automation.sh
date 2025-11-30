#!/bin/bash

# CertifyTrack AICTE Automation Setup Script
# This script sets up automated AICTE tasks including 7-day auto-approval and reporting

echo "🔧 Setting up CertifyTrack AICTE Automation..."

# Check if we're in the project directory
if [ ! -f "BackEnd/manage.py" ]; then
    echo "❌ Error: Please run this script from the CertifyTrack project root directory"
    exit 1
fi

# Navigate to Django directory
cd BackEnd

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Warning: No virtual environment found. Please activate one manually if needed."
fi

# Setup cron jobs for automation
echo "⏰ Setting up cron jobs..."

# Create cron job for daily AICTE auto-approval (runs at 9 AM daily)
CRON_APPROVE="0 9 * * * cd $(pwd)/BackEnd && $(which python) manage.py auto_approve_aicte_points"

# Create cron job for weekly compliance report (runs every Monday at 10 AM)
CRON_REPORT="0 10 * * 1 cd $(pwd)/BackEnd && $(which python) manage.py aicte_compliance_report --output aicte_weekly_report_$(date +\%Y\%m\%d).csv"

# Check if cron jobs already exist
if crontab -l | grep -q "auto_approve_aicte_points"; then
    echo "⚠️  AICTE approval cron job already exists"
else
    # Add approval job to crontab
    (crontab -l ; echo "$CRON_APPROVE") | crontab -
    echo "✅ Added daily AICTE auto-approval job (9 AM daily)"
fi

if crontab -l | grep -q "aicte_compliance_report"; then
    echo "⚠️  AICTE compliance report cron job already exists"
else
    # Add reporting job to crontab
    (crontab -l ; echo "$CRON_REPORT") | crontab -
    echo "✅ Added weekly AICTE compliance report job (Monday 10 AM)"
fi

# Test the management commands
echo "🧪 Testing management commands..."

echo "Testing auto-approve command..."
python manage.py auto_approve_aicte_points

echo "Testing compliance report command..."
python manage.py aicte_compliance_report --output test_report.csv

if [ -f "test_report.csv" ]; then
    echo "✅ Compliance report generated successfully"
    rm test_report.csv
else
    echo "⚠️  Compliance report might not have generated (could be due to no data)"
fi

echo ""
echo "🎉 AICTE Automation Setup Complete!"
echo ""
echo "📋 Scheduled Tasks:"
echo "   • Daily AICTE auto-approval: Every day at 9:00 AM"
echo "   • Weekly compliance report: Every Monday at 10:00 AM"
echo ""
echo "📁 Report files will be saved in BackEnd/ directory"
echo ""
echo "🔍 To manually run tasks:"
echo "   cd BackEnd"
echo "   python manage.py auto_approve_aicte_points"
echo "   python manage.py aicte_compliance_report"
echo ""
echo "📊 To check cron jobs: crontab -l"
echo "🛑 To remove cron jobs: crontab -r"
echo ""
