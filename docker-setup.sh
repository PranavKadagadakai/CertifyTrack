#!/bin/bash

# CertifyTrack Docker Startup Script
# This script handles common Docker setup tasks

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
    
    if ! command -v docker compose &> /dev/null && ! command -v docker &> /dev/null | head -1 | grep -q compose; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check if Docker daemon is running
    if ! docker ps &> /dev/null; then
        print_error "Docker daemon is not running"
        print_info "Please start Docker and try again"
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Setup environment files
setup_env_files() {
    print_info "Setting up environment files..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env from .env.example"
            print_warning "Please edit .env with your configuration"
        fi
    else
        print_success ".env file exists"
    fi
}

# Build images
build_images() {
    print_info "Building Docker images..."
    docker compose build
    print_success "Docker images built successfully"
}

# Start services
start_services() {
    print_info "Starting services..."
    docker compose up -d
    print_success "Services started"
    
    # Wait for database to be ready
    print_info "Waiting for database to be ready..."
    sleep 10
}

# Run migrations
run_migrations() {
    print_info "Running database migrations..."
    docker compose exec -T backend python manage.py migrate
    print_success "Migrations completed"
}

# Seed initial data
seed_data() {
    print_info "Seeding initial data..."
    docker compose exec -T backend python manage.py seed_halls
    print_success "Initial data seeded"
}

# Create superuser
create_superuser() {
    print_info "Creating superuser..."
    docker compose exec backend python manage.py createsuperuser
}

# Show service URLs
show_urls() {
    echo ""
    print_success "Services are running!"
    echo ""
    echo "  ${BLUE}Frontend:${NC}    http://localhost:3000"
    echo "  ${BLUE}API:${NC}         http://localhost:8000/api/"
    echo "  ${BLUE}Admin Panel:${NC}  http://localhost:8000/admin/"
    echo ""
}

# Stop services
stop_services() {
    print_info "Stopping services..."
    docker compose down
    print_success "Services stopped"
}

# Clean everything
clean_all() {
    print_warning "This will remove all containers, images, and volumes!"
    read -p "Are you sure? (yes/no) " -n 3 -r
    echo
    if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        docker compose down -v
        docker system prune -f
        print_success "All resources cleaned"
    fi
}

# View logs
view_logs() {
    service=$1
    if [ -z "$service" ]; then
        docker compose logs -f --tail=100
    else
        docker compose logs -f $service --tail=100
    fi
}

# Health check
health_check() {
    print_info "Checking service health..."
    
    echo ""
    echo "  ${BLUE}Docker Services:${NC}"
    docker compose ps
    
    echo ""
    echo "  ${BLUE}Database Connection:${NC}"
    if docker compose exec -T postgres pg_isready -U certifytrack_user -d certifytrack &> /dev/null; then
        print_success "PostgreSQL is responding"
    else
        print_error "PostgreSQL is not responding"
    fi
    
    echo ""
    echo "  ${BLUE}Redis Connection:${NC}"
    if docker compose exec -T redis redis-cli ping &> /dev/null; then
        print_success "Redis is responding"
    else
        print_error "Redis is not responding"
    fi
    
    echo ""
    echo "  ${BLUE}Backend API:${NC}"
    if curl -s http://localhost:8000/api/ &> /dev/null; then
        print_success "Backend API is responding"
    else
        print_error "Backend API is not responding"
    fi
    
    echo ""
    echo "  ${BLUE}Frontend:${NC}"
    if curl -s http://localhost:3000 &> /dev/null; then
        print_success "Frontend is responding"
    else
        print_error "Frontend is not responding"
    fi
    
    echo ""
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}CertifyTrack Docker Manager${NC}"
    echo "================================"
    echo ""
    echo "1. Setup (build and start)"
    echo "2. Start services"
    echo "3. Stop services"
    echo "4. View logs"
    echo "5. Health check"
    echo "6. Create superuser"
    echo "7. Run migrations"
    echo "8. Seed data"
    echo "9. Clean all"
    echo "0. Exit"
    echo ""
}

# Main script
main() {
    case "$1" in
        setup)
            check_prerequisites
            setup_env_files
            build_images
            start_services
            run_migrations
            seed_data
            show_urls
            ;;
        start)
            start_services
            show_urls
            ;;
        stop)
            stop_services
            ;;
        logs)
            view_logs $2
            ;;
        health)
            health_check
            ;;
        superuser)
            create_superuser
            ;;
        migrate)
            run_migrations
            ;;
        seed)
            seed_data
            ;;
        clean)
            clean_all
            ;;
        "")
            # Interactive mode
            check_prerequisites
            while true; do
                show_menu
                read -p "Select option: " choice
                case $choice in
                    1)
                        check_prerequisites
                        setup_env_files
                        build_images
                        start_services
                        run_migrations
                        seed_data
                        show_urls
                        ;;
                    2)
                        start_services
                        show_urls
                        ;;
                    3)
                        stop_services
                        ;;
                    4)
                        view_logs
                        ;;
                    5)
                        health_check
                        ;;
                    6)
                        create_superuser
                        ;;
                    7)
                        run_migrations
                        ;;
                    8)
                        seed_data
                        ;;
                    9)
                        clean_all
                        ;;
                    0)
                        print_info "Exiting..."
                        exit 0
                        ;;
                    *)
                        print_error "Invalid option"
                        ;;
                esac
            done
            ;;
        *)
            echo "Usage: $0 {setup|start|stop|logs|health|superuser|migrate|seed|clean}"
            echo ""
            echo "Examples:"
            echo "  $0 setup          # Setup and start all services"
            echo "  $0 start          # Start services"
            echo "  $0 stop           # Stop services"
            echo "  $0 logs [service] # View logs (optional service name)"
            echo "  $0 health         # Check service health"
            echo "  $0 superuser      # Create admin user"
            echo "  $0 migrate        # Run database migrations"
            echo "  $0 seed           # Seed initial data"
            echo "  $0 clean          # Remove all containers and volumes"
            echo ""
            echo "Run without arguments for interactive mode"
            exit 1
            ;;
    esac
}

main "$@"
