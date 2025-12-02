#!/bin/bash

# ========================================
# CertifyTrack: Automatic Event Status Updates Setup
# ========================================
#
# This script helps set up automatic event status updates that run periodically
# to update event statuses based on date and time.
#
# The management command updates event statuses as follows:
# - Draft events become "scheduled" when event date arrives
# - Scheduled events become "ongoing" when start time is reached
# - Ongoing/Scheduled events become "completed" when end time is reached
#

# Configuration
VIRTUAL_ENV_PATH="/home/lazypanda69/Projects/Web_Dev/CertifyTrack/BackEnd/.venv"
PROJECT_PATH="/home/lazypanda69/Projects/Web_Dev/CertifyTrack/BackEnd"
MANAGEMENT_COMMAND="python manage.py update_event_statuses"
LOG_FILE="/var/log/certifytrack/event_updates.log"

# Create log directory if it doesn't exist
sudo mkdir -p /var/log/certifytrack
sudo chown $(whoami):$(whoami) /var/log/certifytrack

echo "Setting up automatic event status updates..."
echo "Run frequency: Every 15 minutes"
echo "Log file: $LOG_FILE"
echo ""

# Test the command first
echo "Testing the management command..."
cd $PROJECT_PATH
source $VIRTUAL_ENV_PATH/bin/activate
python manage.py update_event_statuses --dry-run

if [ $? -eq 0 ]; then
    echo "✅ Management command test successful"
else
    echo "❌ Management command test failed"
    exit 1
fi

echo ""
echo "To set up the cron job manually, add the following line to your crontab:"
echo "Run 'crontab -e' and add this line:"
echo ""
echo "# Automatic event status updates every 15 minutes"
echo "*/15 * * * * source $VIRTUAL_ENV_PATH/bin/activate && cd $PROJECT_PATH && $MANAGEMENT_COMMAND >> $LOG_FILE 2>&1"
echo ""

# Offer to set up the cron job automatically
echo "Would you like me to set up the cron job automatically? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Setting up cron job..."

    # Backup current crontab
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null

    # Add the new cron job
    (crontab -l 2>/dev/null; echo "# Automatic event status updates every 15 minutes"; echo "*/15 * * * * source $VIRTUAL_ENV_PATH/bin/activate && cd $PROJECT_PATH && $MANAGEMENT_COMMAND >> $LOG_FILE 2>&1") | crontab -

    if [ $? -eq 0 ]; then
        echo "✅ Cron job set up successfully!"
        echo "The command will run every 15 minutes to update event statuses."
        echo ""
        echo "To view recent logs:"
        echo "tail -f $LOG_FILE"
        echo ""
        echo "To view your crontab:"
        echo "crontab -l"
        echo ""
        echo "To remove the automatic updates:"
        echo "crontab -e # and remove the event status update line"
    else
        echo "❌ Failed to set up cron job. Please set it up manually."
    fi
else
    echo "Cron job setup skipped. You can set it up manually using:"
    echo "crontab -e"
fi

echo ""
echo "Setup complete!"
echo ""
echo "For production deployment, consider these alternatives:"
echo "1. Docker cron container"
echo "2. Kubernetes CronJob"
echo "3. AWS Lambda scheduled event"
echo "4. Django-Q or Celery periodic tasks"
echo ""
echo "Manual test commands:"
echo "cd $PROJECT_PATH && source $VIRTUAL_ENV_PATH/bin/activate"
echo "python manage.py update_event_statuses --dry-run    # Test without changes"
echo "python manage.py update_event_statuses             # Apply changes"
