#!/bin/bash

echo "Setting up APISIX routes for Email Guard..."

# Wait for APISIX to be ready
#echo "Waiting for APISIX to be ready..."
#sleep 10

# Function to check if APISIX is ready
#check_apisix() {
#    curl -s -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' http://localhost:9180/apisix/admin/services > /dev/null
#    return $?
#}

# Wait for APISIX admin API
#while ! check_apisix; do
#    echo "APISIX not ready yet, waiting..."
#    sleep 5
#done

#echo "APISIX is ready!"

# Create routes using APISIX Admin API
echo "Configuring APISIX routes..."

# Authentication route
curl -X PUT http://localhost:9180/apisix/admin/routes/1 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uris": ["/auth/token", "/auth/logout"],
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
      "limit-count": {
        "count": 5,
        "time_window": 420,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 5 authentication requests per 7 minutes.",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "http://localhost:5173",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "expose_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "allow_credential": true,
        "max_age": 3600
      }
    }
  }'


# Scan route
curl -X PUT http://localhost:9180/apisix/admin/routes/2 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uris": ["/scan/email"],
    "name": "email-guard-scan",
    "desc": "Email Guard Scanning Endpoint",
    "methods": ["POST", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "limit-count": {
        "count": 20,
        "time_window": 60,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 20 scan requests per minute.",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "http://localhost:5173",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "expose_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "allow_credential": true,
        "max_age": 3600
      }
    }
  }'

# Health route
curl -X PUT http://localhost:9180/apisix/admin/routes/3 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uris": ["/health"],
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
        "allow_origins": "http://localhost:5173",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "expose_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "allow_credential": true,
        "max_age": 3600
      }
    }
  }'

# History route
curl -X PUT http://localhost:9180/apisix/admin/routes/4 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{
    "uris": ["/history"],
    "name": "email-guard-history",
    "desc": "Email Guard History Endpoint",
    "methods": ["GET", "OPTIONS"],
    "upstream": {
      "type": "roundrobin",
      "nodes": {
        "backend:8000": 1
      }
    },
    "plugins": {
      "limit-count": {
        "count": 30,
        "time_window": 60,
        "rejected_code": 429,
        "rejected_msg": "Rate limit exceeded. Maximum 30 history requests per minute.",
        "key": "remote_addr"
      },
      "cors": {
        "allow_origins": "http://localhost:5173",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "expose_headers": "Authorization,Content-Type,Accept,Origin,X-Requested-With",
        "allow_credential": true,
        "max_age": 3600
      }
    }
  }'


echo "APISIX routes configured!"
curl http://localhost:9180/apisix/admin/routes -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'

echo "Access your application:"
echo "   Frontend: http://localhost:5173"
echo "   API Gateway: http://localhost:9080"
echo "   APISIX Admin: http://localhost:9180"
echo ""
echo "Test tokens:"
echo "   - sample_token_1 (User)"
echo "   - sample_token_2 (Admin)"