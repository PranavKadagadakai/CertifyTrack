#!/bin/bash

# CertifyTrack Production Deployment Script
# This script deploys the application to a production server

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Configuration
DEPLOY_DIR="/opt/certifytrack"
REPO_URL="https://github.com/PranavKadagadakai/CertifyTrack.git"
BRANCH="main"

# Pre-deployment checks
pre_deployment_checks() {
    print_info "Running pre-deployment checks..."
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check available disk space (need at least 10GB)
    available=$(df /opt | awk 'NR==2 {print $4}')
    if [ $available -lt 10485760 ]; then
        print_warning "Low disk space available (< 10GB)"
    fi
}

# Clone or update repository
setup_repository() {
    print_info "Setting up repository..."
    
    if [ -d "$DEPLOY_DIR/.git" ]; then
        print_info "Repository exists, updating..."
        cd "$DEPLOY_DIR"
        git fetch origin
        git checkout $BRANCH
        git pull origin $BRANCH
    else
        print_info "Cloning repository..."
        mkdir -p "$DEPLOY_DIR"
        git clone -b $BRANCH "$REPO_URL" "$DEPLOY_DIR"
    fi
    
    print_success "Repository ready"
}

# Setup environment
setup_environment() {
    print_info "Setting up environment..."
    
    if [ ! -f "$DEPLOY_DIR/.env.prod" ]; then
        if [ -f "$DEPLOY_DIR/.env.prod.example" ]; then
            cp "$DEPLOY_DIR/.env.prod.example" "$DEPLOY_DIR/.env.prod"
            print_warning "Created .env.prod - please edit with production values"
            print_warning "Edit: $DEPLOY_DIR/.env.prod"
            exit 1
        fi
    fi
    
    print_success "Environment configured"
}

# Setup SSL certificates
setup_ssl() {
    print_info "Setting up SSL certificates..."
    
    mkdir -p "$DEPLOY_DIR/nginx/ssl"
    
    if [ ! -f "$DEPLOY_DIR/nginx/ssl/cert.pem" ]; then
        print_warning "SSL certificate not found"
        print_info "Using Let's Encrypt? Run certbot first:"
        echo "  certbot certonly --standalone -d yourdomain.com"
        echo "  sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem $DEPLOY_DIR/nginx/ssl/cert.pem"
        echo "  sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem $DEPLOY_DIR/nginx/ssl/key.pem"
        echo "  sudo chown nobody:nobody $DEPLOY_DIR/nginx/ssl/*"
        exit 1
    fi
    
    print_success "SSL certificates ready"
}

# Build and start services
deploy_services() {
    print_info "Building and starting services..."
    
    cd "$DEPLOY_DIR"
    
    # Build images
    print_info "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build
    
    # Start services
    print_info "Starting services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be ready
    sleep 20
    
    print_success "Services started"
}

# Initialize database
initialize_database() {
    print_info "Initializing database..."
    
    cd "$DEPLOY_DIR"
    
    # Run migrations
    print_info "Running migrations..."
    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
    
    # Collect static files
    print_info "Collecting static files..."
    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput
    
    # Seed initial data
    print_info "Seeding initial data..."
    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py seed_halls
    
    print_success "Database initialized"
}

# Setup backups
setup_backups() {
    print_info "Setting up backup scripts..."
    
    mkdir -p "$DEPLOY_DIR/backups"
    
    cat > "$DEPLOY_DIR/backup.sh" << 'BACKUP_EOF'
#!/bin/bash
BACKUP_DIR="/opt/certifytrack/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/database_$TIMESTAMP.sql.gz"

mkdir -p "$BACKUP_DIR"

# Backup database
cd /opt/certifytrack
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_FILE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "database_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
BACKUP_EOF
    
    chmod +x "$DEPLOY_DIR/backup.sh"
    
    # Add to crontab for daily backups at 2 AM
    (crontab -l 2>/dev/null | grep -v backup.sh; echo "0 2 * * * $DEPLOY_DIR/backup.sh") | crontab -
    
    print_success "Backup scripts configured (daily at 2 AM)"
}

# Setup SSL auto-renewal
setup_ssl_renewal() {
    print_info "Setting up SSL auto-renewal..."
    
    cat > "$DEPLOY_DIR/renew-ssl.sh" << 'RENEWAL_EOF'
#!/bin/bash
DEPLOY_DIR="/opt/certifytrack"

certbot renew --quiet
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem "$DEPLOY_DIR/nginx/ssl/cert.pem"
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem "$DEPLOY_DIR/nginx/ssl/key.pem"

cd "$DEPLOY_DIR"
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
RENEWAL_EOF
    
    chmod +x "$DEPLOY_DIR/renew-ssl.sh"
    
    # Add to crontab for monthly renewal
    (crontab -l 2>/dev/null | grep -v renew-ssl; echo "0 2 1 * * $DEPLOY_DIR/renew-ssl.sh") | crontab -
    
    print_success "SSL auto-renewal configured (1st of month at 2 AM)"
}

# Setup monitoring
setup_monitoring() {
    print_info "Setting up monitoring..."
    
    cat > "$DEPLOY_DIR/monitor.sh" << 'MONITOR_EOF'
#!/bin/bash
DEPLOY_DIR="/opt/certifytrack"

cd "$DEPLOY_DIR"

# Check if services are running
docker-compose -f docker-compose.prod.yml ps | grep "Up" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Services are down! Attempting restart..."
    docker-compose -f docker-compose.prod.yml up -d
fi

# Check disk space
available=$(df /opt | awk 'NR==2 {print $4}')
if [ $available -lt 5242880 ]; then
    echo "WARNING: Low disk space! Less than 5GB available"
fi

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs --tail=100 backend | grep -i "error" | head -5
MONITOR_EOF
    
    chmod +x "$DEPLOY_DIR/monitor.sh"
    
    # Add to crontab for hourly monitoring
    (crontab -l 2>/dev/null | grep -v monitor.sh; echo "0 * * * * $DEPLOY_DIR/monitor.sh") | crontab -
    
    print_success "Monitoring script configured (hourly checks)"
}

# Health check
health_check() {
    print_info "Running health checks..."
    
    cd "$DEPLOY_DIR"
    
    # Check services
    echo ""
    docker-compose -f docker-compose.prod.yml ps
    
    # Wait for services to be fully ready
    sleep 10
    
    # Test database
    echo ""
    print_info "Testing database connection..."
    if docker-compose -f docker-compose.prod.yml exec -T postgres pg_isready -U certifytrack_prod_user -d certifytrack_prod &> /dev/null; then
        print_success "PostgreSQL is responding"
    else
        print_error "PostgreSQL is not responding"
    fi
    
    # Test API
    echo ""
    print_info "Testing API..."
    if curl -s http://localhost:8000/api/ &> /dev/null; then
        print_success "Backend API is responding"
    else
        print_error "Backend API is not responding"
    fi
    
    # Test frontend
    echo ""
    print_info "Testing frontend..."
    if curl -s http://localhost/health &> /dev/null; then
        print_success "Frontend is responding"
    else
        print_error "Frontend is not responding"
    fi
}

# Post-deployment summary
deployment_summary() {
    echo ""
    echo "================================"
    print_success "Deployment completed!"
    echo "================================"
    echo ""
    echo "Next steps:"
    echo "1. Configure your domain DNS to point to this server"
    echo "2. Edit .env.prod with your production values"
    echo "3. Setup SSL certificates with Let's Encrypt"
    echo "4. Create admin user:"
    echo "   docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser"
    echo ""
    echo "Useful commands:"
    echo "  View logs:        docker-compose -f docker-compose.prod.yml logs -f"
    echo "  Stop services:    docker-compose -f docker-compose.prod.yml down"
    echo "  Backup database:  $DEPLOY_DIR/backup.sh"
    echo "  Monitor status:   $DEPLOY_DIR/monitor.sh"
    echo ""
    echo "Documentation: $DEPLOY_DIR/DOCKER_SETUP.md"
    echo ""
}

# Main deployment
main() {
    echo ""
    echo -e "${BLUE}CertifyTrack Production Deployment${NC}"
    echo "======================================"
    echo ""
    
    pre_deployment_checks
    setup_repository
    setup_environment
    setup_ssl
    deploy_services
    initialize_database
    setup_backups
    setup_ssl_renewal
    setup_monitoring
    health_check
    deployment_summary
}

# Run main function
main "$@"
