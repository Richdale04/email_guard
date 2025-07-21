#!/bin/bash

echo "ðŸ³ Email Guard - Docker Setup"
echo "=============================="

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "âŒ Error: docker-compose is not installed or not in PATH"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "âŒ Error: Docker is not running"
    exit 1
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  up          - Start all services"
    echo "  down        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  logs        - Show logs from all services"
    echo "  setup       - Start services and configure APISIX routes"
    echo "  clean       - Stop services and remove volumes"
    echo "  status      - Show status of all services"
    echo "  build       - Build all services"
    echo ""
    echo "Examples:"
    echo "  $0 up       - Start the application"
    echo "  $0 setup    - Start and configure everything"
    echo "  $0 logs     - View logs"
    echo ""
}

# Function to run docker-compose commands
run_docker_compose() {
    docker-compose "$@"
}

# Function to setup APISIX routes
setup_apisix() {
    echo "ðŸš€ Starting services..."
    run_docker_compose up -d
    
    echo "â³ Waiting for services to be ready..."
    sleep 10
    
    echo "ðŸ”§ Configuring APISIX routes..."
    ./setup-apisix.sh
    
    echo ""
    echo "âœ… Setup complete!"
    echo ""
    echo "ðŸŒ Access your application:"
    echo "   API Gateway: http://localhost:9080"
    echo "   APISIX Admin: http://localhost:9180"
    echo "   Backend Direct: http://localhost:8000"
    echo ""
    echo "ðŸ”‘ Test tokens:"
    echo "   - sample_token_1 (User)"
    echo "   - sample_token_2 (Admin)"
    echo "   - sample_token_3 (User)"
    echo "   - sample_token_4 (User)"
    echo ""
    echo "ðŸ“– See DEPLOYMENT_GUIDE.md for frontend deployment to Vercel"
}

# Main script logic
case "${1:-}" in
    "up")
        echo "ðŸš€ Starting Email Guard services..."
        run_docker_compose up -d
        echo "âœ… Services started!"
        ;;
    "down")
        echo "ðŸ›‘ Stopping Email Guard services..."
        run_docker_compose down
        echo "âœ… Services stopped!"
        ;;
    "restart")
        echo "ðŸ”„ Restarting Email Guard services..."
        run_docker_compose restart
        echo "âœ… Services restarted!"
        ;;
    "logs")
        echo "ðŸ“‹ Showing logs..."
        run_docker_compose logs -f
        ;;
    "setup")
        setup_apisix
        ;;
    "clean")
        echo "ðŸ§¹ Cleaning up Email Guard services..."
        run_docker_compose down -v
        echo "âœ… Services and volumes cleaned!"
        ;;
    "status")
        echo "ðŸ“Š Service status:"
        run_docker_compose ps
        ;;
    "build")
        echo "ðŸ”¨ Building Email Guard services..."
        run_docker_compose build
        echo "âœ… Services built!"
        ;;
    *)
        show_usage
        ;;
esac 