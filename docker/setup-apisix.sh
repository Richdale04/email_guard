#!/bin/bash

echo "ðŸš€ Setting up APISIX routes for Email Guard..."

# Wait for APISIX to be ready
echo "â³ Waiting for APISIX to be ready..."
sleep 30

# Function to check if APISIX is ready
check_apisix() {
    curl -s -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' http://localhost:9180/apisix/admin/services > /dev/null
    return $?
}

# Wait for APISIX admin API
while ! check_apisix; do
    echo "â³ APISIX not ready yet, waiting..."
    sleep 5
done

echo "âœ… APISIX is ready!"

# Create routes using APISIX Admin API
echo "ðŸ”§ Configuring APISIX routes..."

# Authentication route
curl -X PUT http://localhost:9180/apisix/admin/routes/1 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uri": "/auth/*",
    "name": "email-guard-auth",
    "desc": "Email Guard Authentication Endpoints",
    "methods": ["POST", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "rate-limit": {
        "rate": 5,
        "burst": 10,
        "time_window": 420,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 5 authentication requests per 7 minutes.",
        "key_type": "var",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "*",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "*",
        "expose_headers": "*",
        "allow_credentials": true,
        "max_age": 3600
      }
    }
  }'

# Scan route
curl -X PUT http://localhost:9180/apisix/admin/routes/2 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uri": "/scan/*",
    "name": "email-guard-scan",
    "desc": "Email Guard Scanning Endpoints",
    "methods": ["POST", "GET", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "rate-limit": {
        "rate": 20,
        "burst": 30,
        "time_window": 60,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 20 scan requests per minute.",
        "key_type": "var",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "*",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "*",
        "expose_headers": "*",
        "allow_credentials": true,
        "max_age": 3600
      }
    }
  }'

# Health route
curl -X PUT http://localhost:9180/apisix/admin/routes/3 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uri": "/health",
    "name": "email-guard-health",
    "desc": "Email Guard Health Check",
    "methods": ["GET", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "cors": {
        "allow_origins": "*",
        "allow_methods": "GET,OPTIONS",
        "allow_headers": "*",
        "expose_headers": "*",
        "allow_credentials": true,
        "max_age": 3600
      }
    }
  }'

# History route
curl -X PUT http://localhost:9180/apisix/admin/routes/4 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uri": "/history",
    "name": "email-guard-history",
    "desc": "Email Guard History Endpoints",
    "methods": ["GET", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "rate-limit": {
        "rate": 30,
        "burst": 50,
        "time_window": 60,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 30 history requests per minute.",
        "key_type": "var",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "*",
        "allow_methods": "GET,OPTIONS",
        "allow_headers": "*",
        "expose_headers": "*",
        "allow_credentials": true,
        "max_age": 3600
      }
    }
  }'

echo "âœ… APISIX routes configured successfully!"
echo ""
echo "ðŸŒ Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   API Gateway: http://localhost:9080"
echo "   APISIX Admin: http://localhost:9180"
echo ""
echo "ðŸ”‘ Test tokens:"
echo "   - sample_token_1 (User)"
echo "   - sample_token_2 (Admin)"
echo "   - sample_token_3 (User)"
echo "   - sample_token_4 (User)" 