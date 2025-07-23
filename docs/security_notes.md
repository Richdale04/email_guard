# Security Notes - Email Guard

## Security Overview

This document outlines the comprehensive security measures implemented in the Email Guard application and provides guidance for secure deployment and operation. The application implements multiple layers of security from the frontend to the backend, including authentication, rate limiting, input validation, and container security.

## Authentication Security

### JWT Implementation
- **Algorithm**: HS256 (HMAC with SHA-256) for symmetric key signing
- **Token Structure**: Standard JWT with header, payload, and signature
- **Token Expiration**: 60 minutes (configurable via environment variables)
- **Secret Key**: Configurable via `JWT_SECRET_KEY` environment variable
- **Claims**: Includes user ID (`sub`), role, and expiration time (`exp`)
- **Validation**: Server-side verification on every protected endpoint

### HTTP-Only Cookies
- **XSS Protection**: Tokens stored in HTTP-only cookies prevent JavaScript access
- **Security Attributes**:
  - `httponly=True`: Prevents client-side script access
  - `secure=True`: HTTPS-only transmission (production)
  - `samesite="lax"`: CSRF protection
  - `max_age=3600`: 1-hour expiration
- **Automatic Handling**: Browsers automatically include cookies in requests
- **Logout Security**: Secure cookie deletion on logout

### Token-Based Authentication
- **Token Storage**: CSV file for development (database recommended for production)
- **Token Validation**: Pre-shared tokens with expiration dates
- **Role-Based Access**: User and admin roles with different permissions
- **Sample Tokens**: Development tokens for testing purposes

## Rate Limiting Security

### APISIX Gateway Rate Limiting
- **Implementation**: APISIX plugin-based rate limiting
- **Storage**: In-memory for development, Redis recommended for production
- **Granularity**: Per IP address to prevent abuse from single sources

#### Authentication Endpoints (`/auth/*`)
- **Rate**: 5 requests per 7 minutes per IP address
- **Burst**: 10 requests maximum
- **Time Window**: 420 seconds (7 minutes)
- **Purpose**: Prevents brute force authentication attacks

#### Scan Endpoints (`/scan/*`)
- **Rate**: 20 requests per minute per IP address
- **Burst**: 30 requests maximum
- **Time Window**: 60 seconds
- **Timeout**: 300 seconds (5 minutes for model cold start)

#### History Endpoints (`/history`)
- **Rate**: 30 requests per minute per IP address
- **Burst**: 50 requests maximum
- **Time Window**: 60 seconds

#### Models Status Endpoints (`/models/*`)
- **Rate**: No limit (frequent status checks needed)
- **Timeout**: 60 seconds
- **Purpose**: Real-time model status monitoring

## Input Validation and Sanitization

### Email Content Validation
- **Length Limits**: Maximum 10,000 characters to prevent resource exhaustion
- **Content Detection**: Basic email structure validation
- **Character Filtering**: Removal of control characters and dangerous unicode
- **Unicode Normalization**: NFKC normalization for consistent processing
- **HTML Entity Handling**: Proper decoding and sanitization

### Pydantic Model Validation
- **Schema Validation**: All API inputs validated with Pydantic models
- **Type Checking**: Strict type validation for all request parameters
- **Automatic Sanitization**: Built-in data cleaning and validation
- **Error Handling**: Structured error responses without information leakage

### Suspicious Pattern Detection
- **URL Analysis**: Detection of suspicious domains and shortened URLs
- **Keyword Detection**: Financial terms, urgency indicators, personal info requests
- **Pattern Matching**: Regular expressions for common phishing patterns
- **Risk Scoring**: Weighted scoring system for threat assessment

## API Security

### CORS Configuration
- **Allowed Origins**: Explicitly configured allowed origins
- **Development**: `http://localhost:5173` for local development
- **Production**: Specific domain restrictions
- **Credentials**: Enabled for cookie-based authentication
- **Methods**: Only necessary HTTP methods allowed

### Request Validation
- **Schema Enforcement**: All requests validated against predefined schemas
- **Content-Type Validation**: Proper JSON content type enforcement
- **Size Limits**: Request size limitations to prevent DoS attacks
- **Header Validation**: Security-relevant header checking

### Response Security
- **Information Hiding**: No sensitive data in error responses
- **Consistent Formatting**: Standardized response structure
- **Security Headers**: Appropriate HTTP security headers
- **Content-Type Protection**: Proper MIME type setting

## Container Security

### Docker Implementation
- **Base Images**: Official Python slim images for minimal attack surface
- **Multi-stage Builds**: Reduced final image size and attack surface
- **Non-root Execution**: Application runs as non-root user where possible
- **Dependency Management**: Minimal required packages only
- **Layer Optimization**: Efficient layer caching and minimal rebuilds

### Container Isolation
- **Network Isolation**: Docker networks for service isolation
- **Resource Limits**: Memory and CPU constraints
- **Read-only Filesystems**: Where applicable
- **Health Checks**: Application health monitoring
- **Secret Management**: Environment variable-based secrets

### APISIX Container Security
- **Official Images**: Apache APISIX official Docker images
- **Configuration Security**: Secure default configurations
- **Admin API Protection**: Admin key-based authentication
- **TLS Configuration**: HTTPS/TLS support for production

## Data Protection

### Sensitive Data Handling
- **Email Content**: Temporary storage during analysis only
- **User Tokens**: Secure storage with expiration
- **Analysis History**: Local file storage with access controls
- **No Persistent PII**: No long-term personal data storage
- **Memory Management**: Secure memory cleanup after processing

### Privacy Considerations
- **Data Minimization**: Only necessary data collected and stored
- **Retention Policies**: Automatic cleanup of temporary data
- **User Control**: Users control their analysis history
- **No Data Sharing**: No third-party data sharing
- **Anonymization**: Results stored without personal identifiers

### Encryption
- **Transmission**: HTTPS encryption for all production traffic
- **Storage**: Encrypted storage recommended for production
- **JWT Signing**: Cryptographic signing of authentication tokens
- **Password Hashing**: Secure hashing for any stored credentials

## Model Security

### AI Model Safety
- **Input Validation**: All inputs sanitized before model processing
- **Resource Limits**: Memory and processing time constraints
- **Error Handling**: Graceful degradation on model failures
- **Model Isolation**: Sandboxed model execution environment
- **Timeout Protection**: Prevents hanging model operations

### Model Output Validation
- **Result Formatting**: Standardized and validated output format
- **Confidence Bounds**: Validated confidence scores (0.0-1.0)
- **Decision Mapping**: Consistent decision categories
- **Sanitized Responses**: No raw model output exposed to users
- **Error Masking**: Generic error messages for model failures

## Network Security

### API Gateway Security
- **Request Routing**: Secure routing through APISIX gateway
- **Load Balancing**: Distribution of requests across backend instances
- **SSL Termination**: TLS encryption handling at gateway level
- **Request Filtering**: Malicious request detection and blocking
- **IP Filtering**: Geographic and known bad IP blocking capabilities

### Backend Protection
- **Internal Networks**: Backend services on isolated Docker networks
- **Port Restrictions**: Only necessary ports exposed
- **Service Discovery**: Secure inter-service communication
- **Health Monitoring**: Continuous service health checking

## Security Headers

### HTTP Security Headers
- **X-Content-Type-Options**: `nosniff` to prevent MIME type sniffing
- **X-Frame-Options**: `DENY` to prevent clickjacking
- **X-XSS-Protection**: Browser XSS protection enabled
- **Strict-Transport-Security**: HTTPS enforcement in production
- **Content-Security-Policy**: Strict CSP for XSS prevention

### Custom Security Headers
- **API Versioning**: Version information in headers
- **Request Tracking**: Unique request IDs for audit trails
- **Rate Limit Information**: Current rate limit status in responses

## Error Handling Security

### Information Disclosure Prevention
- **Generic Error Messages**: No system information in user-facing errors
- **Log Segregation**: Detailed errors in logs, generic errors to users
- **Stack Trace Hiding**: No technical details exposed to clients
- **Consistent Error Format**: Standardized error response structure

### Audit and Logging
- **Security Events**: Authentication attempts, rate limit violations
- **Access Logging**: All API access logged with timestamps
- **Error Logging**: System errors logged for monitoring
- **No Sensitive Data**: Personal information excluded from logs
- **Structured Logging**: Machine-readable log format

## Deployment Security

### Environment Configuration
- **Secret Management**: All secrets via environment variables
- **Configuration Validation**: Startup configuration checking
- **Default Security**: Secure defaults for all settings
- **Environment Separation**: Different configs for dev/staging/production

### Production Hardening
- **HTTPS Enforcement**: All traffic over TLS
- **Security Headers**: Full security header implementation
- **Rate Limiting**: Production-grade rate limiting with Redis
- **Monitoring**: Comprehensive security monitoring and alerting
- **Backup Security**: Encrypted backups with access controls

## Security Best Practices

### Development Security
1. **Secure Coding**: Follow secure development practices
2. **Code Review**: Security-focused code reviews
3. **Dependency Management**: Regular security updates
4. **Testing**: Comprehensive security testing
5. **Documentation**: Security requirement documentation

### Operational Security
1. **Access Control**: Principle of least privilege
2. **Regular Updates**: Timely security patches
3. **Monitoring**: Continuous security monitoring
4. **Backup**: Regular secure backups
5. **Training**: Security awareness training

### Production Security
1. **HTTPS Only**: Enforce HTTPS for all traffic
2. **Strong Secrets**: Cryptographically secure secrets
3. **Database Security**: Encrypted database storage
4. **Network Security**: Proper network segmentation
5. **Audit Logging**: Comprehensive audit trails

## Security Checklist

### Pre-Deployment
- [ ] JWT secret key configured
- [ ] HTTPS certificates installed
- [ ] Rate limiting configured
- [ ] Input validation implemented
- [ ] Error handling reviewed
- [ ] Security headers configured
- [ ] Container security hardened
- [ ] Network isolation implemented

### Post-Deployment
- [ ] Security monitoring active
- [ ] Logging configured
- [ ] Backup strategy implemented
- [ ] Access controls verified
- [ ] Performance monitoring active
- [ ] Incident response plan ready

### Ongoing Security
- [ ] Regular security updates
- [ ] Log analysis and monitoring
- [ ] Access review and audit
- [ ] Security testing and assessment
- [ ] Incident response drills
- [ ] Security training updates

## Incident Response

### Security Incident Process
1. **Detection**: Automated monitoring and manual reporting
2. **Assessment**: Impact and scope evaluation
3. **Containment**: Immediate threat isolation
4. **Eradication**: Threat removal and vulnerability patching
5. **Recovery**: Service restoration and monitoring
6. **Lessons Learned**: Post-incident security improvements

### Contact Information
- **Security Team**: security@emailguard.com
- **Emergency Response**: Immediate escalation procedures
- **Documentation**: Incident documentation and reporting

## Compliance Considerations

### Data Protection
- **GDPR**: Data minimization and user rights
- **CCPA**: Privacy and data handling
- **SOC 2**: Security controls and monitoring

### Industry Standards
- **OWASP Top 10**: Address common vulnerabilities
- **NIST Framework**: Cybersecurity best practices
- **ISO 27001**: Information security management

## Security Testing

### Automated Testing
- **Unit Tests**: Security-focused test cases
- **Integration Tests**: API security testing
- **Static Analysis**: Code security scanning

### Manual Testing
- **Penetration Testing**: Regular security assessments
- **Code Review**: Security-focused code reviews
- **Configuration Review**: Security configuration audits

## Future Security Enhancements

### Planned Improvements
1. **Multi-Factor Authentication**: Additional authentication factors
2. **Advanced Rate Limiting**: More sophisticated rate limiting
3. **Threat Intelligence**: Integration with threat feeds
4. **Behavioral Analysis**: User behavior monitoring
5. **Encryption**: End-to-end encryption for sensitive data

### Security Roadmap
- **Phase 1**: Basic security measures (implemented)
- **Phase 2**: Advanced authentication and monitoring
- **Phase 3**: Threat intelligence and behavioral analysis
- **Phase 4**: Advanced encryption and compliance features

## Conclusion

The Email Guard application implements comprehensive security measures across all layers of the application stack. From secure authentication and authorization to input validation, rate limiting, and container security, the application follows industry best practices and security standards.
