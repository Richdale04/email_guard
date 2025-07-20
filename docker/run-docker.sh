#!/bin/bash

echo "🐳 Email Guard - Docker Setup"
echo "=============================="

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed or not in PATH"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running"
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
    echo "🚀 Starting services..."
    run_docker_compose up -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo "🔧 Configuring APISIX routes..."
    ./setup-apisix.sh
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🌐 Access your application:"
    echo "   API Gateway: http://localhost:9080"
    echo "   APISIX Admin: http://localhost:9180"
    echo "   Backend Direct: http://localhost:8000"
    echo ""
    echo "🔑 Test tokens:"
    echo "   - sample_token_1 (User)"
    echo "   - sample_token_2 (Admin)"
    echo "   - sample_token_3 (User)"
    echo "   - sample_token_4 (User)"
    echo ""
    echo "📖 See DEPLOYMENT_GUIDE.md for frontend deployment to Vercel"
}

# Main script logic
case "${1:-}" in
    "up")
        echo "🚀 Starting Email Guard services..."
        run_docker_compose up -d
        echo "✅ Services started!"
        ;;
    "down")
        echo "🛑 Stopping Email Guard services..."
        run_docker_compose down
        echo "✅ Services stopped!"
        ;;
    "restart")
        echo "🔄 Restarting Email Guard services..."
        run_docker_compose restart
        echo "✅ Services restarted!"
        ;;
    "logs")
        echo "📋 Showing logs..."
        run_docker_compose logs -f
        ;;
    "setup")
        setup_apisix
        ;;
    "clean")
        echo "🧹 Cleaning up Email Guard services..."
        run_docker_compose down -v
        echo "✅ Services and volumes cleaned!"
        ;;
    "status")
        echo "📊 Service status:"
        run_docker_compose ps
        ;;
    "build")
        echo "🔨 Building Email Guard services..."
        run_docker_compose build
        echo "✅ Services built!"
        ;;
    *)
        show_usage
        ;;
esac 