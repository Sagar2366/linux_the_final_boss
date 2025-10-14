# Day 22: Certificate Management (SSL/TLS, OpenSSL, Certbot)

## Table of Contents

- [Day 22: Certificate Management (SSL/TLS, OpenSSL, Certbot)](#day-22-certificate-management-ssltls-openssl-certbot)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
  - [Why Certificate Management Matters](#why-certificate-management-matters)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary](#key-commands-summary)
- [Certificate generation](#certificate-generation)
- [Let's Encrypt](#let's-encrypt)
- [Certificate inspection](#certificate-inspection)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 22, you will:
- Understand SSL/TLS fundamentals and PKI
- Generate and manage certificates with OpenSSL
- Automate certificate management with Certbot
- Configure HTTPS on web servers
- Monitor and renew certificates

**Estimated Time:** 3-4 hours

## Notes

## Why Certificate Management Matters
- Secures data in transit, enables HTTPS, and builds trust for users.
- Essential for web servers, APIs, and secure communications.

```mermaid
flowchart TD
    A[Certificate Management] --> B[Certificate Types]
    A --> C[Certificate Lifecycle]
    A --> D[Tools & Automation]
    A --> E[Security Practices]
    
    B --> B1[Self-signed<br/>Testing/Internal]
    B --> B2[CA-signed<br/>Production/Public]
    B --> B3[Wildcard<br/>*.domain.com]
    B --> B4[Multi-domain<br/>SAN certificates]
    
    C --> C1[Generation<br/>Private key + CSR]
    C --> C2[Signing<br/>CA validation]
    C --> C3[Installation<br/>Web server config]
    C --> C4[Renewal<br/>Before expiration]
    C --> C5[Revocation<br/>Compromise/replacement]
    
    D --> D1[OpenSSL<br/>Manual management]
    D --> D2[Certbot<br/>Let's Encrypt automation]
    D --> D3[ACME clients<br/>Automated renewal]
    D --> D4[Certificate stores<br/>System trust]
    
    E --> E1[Key Security<br/>Protect private keys]
    E --> E2[Regular Renewal<br/>Avoid expiration]
    E --> E3[Monitoring<br/>Certificate health]
    E --> E4[Backup & Recovery<br/>Certificate copies]
    
    F[Certificate Chain] --> F1[Root CA]
    F1 --> F2[Intermediate CA]
    F2 --> F3[Server Certificate]
    
    G[SSL/TLS Process] --> G1[Client Hello]
    G1 --> G2[Server Certificate]
    G2 --> G3[Key Exchange]
    G3 --> G4[Encrypted Communication]
    
    style A fill:#f96
    style C fill:#9f6
    style E fill:#69f
```

- **SSL/TLS Fundamentals:**
  - **Encryption:** Protects data in transit
  - **Authentication:** Verifies server identity
  - **Certificate Authority (CA):** Trusted third party
  - **Chain of Trust:** Root CA → Intermediate CA → Server Certificate
  - **Common Names (CN):** Domain name in certificate
  - **Subject Alternative Names (SAN):** Multiple domains

- **Certificate Types:**
  - **Self-signed:** Generated locally, not trusted by browsers
  - **CA-signed:** Issued by trusted Certificate Authority
  - **Domain Validated (DV):** Basic domain ownership verification
  - **Organization Validated (OV):** Company verification
  - **Extended Validation (EV):** Highest level of validation

- **Key Commands:**
  ```bash
  # OpenSSL certificate operations
  openssl genrsa -out private.key 2048
  openssl req -new -key private.key -out request.csr
  openssl x509 -req -in request.csr -signkey private.key -out certificate.crt
  
  # Certificate inspection
  openssl x509 -in cert.crt -text -noout
  openssl s_client -connect domain.com:443
  
  # Let's Encrypt with Certbot
  certbot --nginx -d domain.com
  certbot renew --dry-run
  ```

## Sample Exercises
1. Generate a self-signed certificate for a test domain.
2. Set up HTTPS on a local Nginx server using Certbot.
3. View and explain the details of a certificate file.
4. Automate certificate renewal and test expiry alerts.
5. Create a Certificate Signing Request (CSR).
6. Configure certificate chain validation.
7. Set up certificate monitoring and alerting.

## Solutions
1. **Self-signed certificate:**
   ```bash
   # Generate private key and certificate in one command
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout mysite.key -out mysite.crt \
     -subj "/C=US/ST=State/L=City/O=Org/CN=mysite.local"
   
   # Set proper permissions
   chmod 600 mysite.key
   chmod 644 mysite.crt
   ```

2. **Certbot HTTPS setup:**
   ```bash
   # Install Certbot
   sudo apt update
   sudo apt install certbot python3-certbot-nginx
   
   # Get certificate and configure Nginx
   sudo certbot --nginx -d example.com -d www.example.com
   
   # Verify configuration
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. **Certificate inspection:**
   ```bash
   # View certificate details
   openssl x509 -in mysite.crt -text -noout
   
   # Check specific fields
   openssl x509 -in mysite.crt -noout -subject
   openssl x509 -in mysite.crt -noout -dates
   openssl x509 -in mysite.crt -noout -fingerprint
   ```

4. **Automated renewal:**
   ```bash
   # Test renewal
   sudo certbot renew --dry-run
   
   # Add to crontab
   echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
   
   # Systemd timer (alternative)
   sudo systemctl enable certbot.timer
   sudo systemctl start certbot.timer
   ```

5. **Certificate Signing Request:**
   ```bash
   # Generate private key
   openssl genrsa -out private.key 2048
   
   # Create CSR
   openssl req -new -key private.key -out request.csr \
     -subj "/C=US/ST=State/L=City/O=Organization/CN=domain.com"
   
   # Verify CSR
   openssl req -in request.csr -text -noout
   ```

6. **Certificate chain validation:**
   ```bash
   # Download certificate chain
   openssl s_client -connect domain.com:443 -showcerts
   
   # Verify chain
   openssl verify -CAfile ca-bundle.crt certificate.crt
   ```

7. **Certificate monitoring:**
   ```bash
   #!/bin/bash
   # cert-monitor.sh
   CERT_FILE="/etc/ssl/certs/mysite.crt"
   DAYS_WARNING=30
   
   EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_FILE" | cut -d= -f2)
   EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
   NOW_EPOCH=$(date +%s)
   DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
   
   if [ $DAYS_LEFT -lt $DAYS_WARNING ]; then
       echo "WARNING: Certificate expires in $DAYS_LEFT days"
   fi
   ```

## Sample Interview Questions
1. What is the difference between SSL and TLS?
2. How do you generate a CSR and private key?
3. How do you automate certificate renewal?
4. How do you check certificate expiry?
5. What is a certificate chain and why is it important?
6. How do you troubleshoot SSL/TLS issues?
7. What are the different types of SSL certificates?
8. How do you secure private keys?
9. What is certificate pinning?
10. How do you handle certificate revocation?

## Interview Question Answers
1. **SSL vs TLS:** TLS is the modern, more secure successor to SSL; SSL is deprecated
2. **CSR Generation:** `openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out req.csr`
3. **Automated Renewal:** Use Certbot with cron jobs or systemd timers for Let's Encrypt
4. **Expiry Check:** `openssl x509 -enddate -noout -in cert.crt` or monitoring scripts
5. **Certificate Chain:** Sequence from server cert to root CA, establishes trust path
6. **SSL Troubleshooting:** Check certificate validity, chain completeness, cipher compatibility
7. **Certificate Types:** DV (domain validated), OV (organization), EV (extended validation)
8. **Key Security:** Restrict file permissions (600), use hardware security modules, rotate regularly
9. **Certificate Pinning:** Hardcode expected certificate/key in application for security
10. **Revocation:** Use CRL (Certificate Revocation List) or OCSP (Online Certificate Status Protocol)

## Completion Checklist
- [ ] Understand SSL/TLS fundamentals
- [ ] Can generate certificates with OpenSSL
- [ ] Know how to use Certbot for Let's Encrypt
- [ ] Can configure HTTPS on web servers
- [ ] Familiar with certificate monitoring
- [ ] Understand certificate troubleshooting

## Key Commands Summary
```bash
# Certificate generation
openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out csr.pem
openssl x509 -req -in csr.pem -signkey key.pem -out cert.pem

# Let's Encrypt
certbot --nginx -d domain.com
certbot renew
certbot certificates

# Certificate inspection
openssl x509 -in cert.pem -text -noout
openssl s_client -connect domain.com:443
```

## Best Practices
- Use strong encryption (RSA 2048+ or ECDSA 256+)
- Automate certificate renewal
- Monitor certificate expiry
- Protect private keys (permissions, storage)
- Use HTTPS everywhere
- Implement proper certificate validation

## Next Steps
Proceed to [Day 23: Linux Interview Questions & Real-World Scenarios](../Day_23/notes_and_exercises.md) for interview preparation.
