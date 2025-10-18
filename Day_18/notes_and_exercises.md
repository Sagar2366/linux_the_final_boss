# Day 18: Web Servers (Apache, Nginx, Reverse Proxy)

## Table of Contents

- [Day 18: Web Servers (Apache, Nginx, Reverse Proxy)](#day-18-web-servers-apache-nginx-reverse-proxy)
  - [Learning Objectives](#learning-objectives)
  - [Notes](#notes)
  - [Sample Exercises](#sample-exercises)
  - [Solutions](#solutions)
  - [Sample Interview Questions](#sample-interview-questions)
  - [Interview Question Answers](#interview-question-answers)
  - [Completion Checklist](#completion-checklist)
  - [Key Commands Summary](#key-commands-summary)
- [Apache](#apache)
- [Nginx](#nginx)
- [SSL/TLS](#ssltls)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)


## Learning Objectives
By the end of Day 18, you will:
- Install and configure Apache and Nginx web servers
- Set up virtual hosts and server blocks
- Configure reverse proxy setups
- Implement SSL/TLS certificates
- Monitor and troubleshoot web servers

**Estimated Time:** 4-5 hours

## Notes
- **Why Web Servers Matter:**
  - Serve web content, APIs, and enable application delivery.
  - Core skill for DevOps, SRE, and cloud engineers.

```mermaid
flowchart TD
    A[Web Server Architecture] --> B[Web Servers]
    A --> C[Reverse Proxy]
    A --> D[Load Balancing]
    A --> E[SSL/TLS]
    
    B --> B1[Apache<br/>Process-based]
    B --> B2[Nginx<br/>Event-driven]
    B --> B3[Lighttpd<br/>Lightweight]
    B --> B4[Caddy<br/>Auto HTTPS]
    
    C --> C1[Backend Routing]
    C --> C2[SSL Termination]
    C --> C3[Caching]
    C --> C4[Header Modification]
    
    D --> D1[Round Robin]
    D --> D2[Least Connections]
    D --> D3[IP Hash]
    D --> D4[Health Checks]
    
    E --> E1[Let's Encrypt]
    E --> E2[SSL Certificates]
    E --> E3[Security Headers]
    E --> E4[HTTPS Redirect]
    
    F[Request Flow] --> F1[Client]
    F1 --> F2[Web Server]
    F2 --> F3[Application]
    F3 --> F4[Database]
    
    G[Configuration] --> G1[Virtual Hosts]
    G --> G2[Server Blocks]
    G --> G3[Modules/Plugins]
    G --> G4[Log Management]
    
    style A fill:#f96
    style B fill:#9f6
    style F fill:#69f
```

- **Apache HTTP Server:**
  - Install: `apt install apache2` or `yum install httpd`
  - Start/stop: `systemctl start|stop apache2` or `httpd`
  - Config: `/etc/apache2/` (Debian), `/etc/httpd/` (RHEL)
  - Main config: `apache2.conf` or `httpd.conf`
  - Virtual hosts: `/etc/apache2/sites-available/`
  - Enable site: `a2ensite site.conf`; reload: `systemctl reload apache2`
  - Logs: `/var/log/apache2/`

- **Nginx:**
  - Install: `apt install nginx` or `yum install nginx`
  - Start/stop: `systemctl start|stop nginx`
  - Config: `/etc/nginx/`, main: `nginx.conf`
  - Server blocks: `/etc/nginx/sites-available/`
  - Test config: `nginx -t`; reload: `systemctl reload nginx`
  - Logs: `/var/log/nginx/`

- **Reverse Proxy:**
  - Nginx/Apache can proxy requests to backend servers
  - Example Nginx block:
    ```
    location /api/ {
      proxy_pass http://localhost:5000/;
    }
    ```
  - Use for load balancing, SSL termination, caching

- **Best Practices:**
  - Use least privilege for web server user
  - Keep software updated
  - Use HTTPS (Let's Encrypt, Certbot)
  - Restrict access to admin interfaces
  - Monitor logs for suspicious activity



- **Advanced Configuration:**
  ```bash
  # Nginx reverse proxy example
  server {
      listen 80;
      server_name example.com;
      
      location / {
          proxy_pass http://localhost:3000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
      }
  }
  
  # Apache virtual host example
  <VirtualHost *:80>
      ServerName example.com
      DocumentRoot /var/www/example
      ErrorLog ${APACHE_LOG_DIR}/example_error.log
      CustomLog ${APACHE_LOG_DIR}/example_access.log combined
  </VirtualHost>
  ```

- **SSL/TLS Configuration:**
  ```bash
  # Install Let's Encrypt certificate
  certbot --nginx -d example.com
  
  # Manual SSL configuration (Nginx)
  server {
      listen 443 ssl;
      ssl_certificate /path/to/cert.pem;
      ssl_certificate_key /path/to/key.pem;
  }
  ```

## Sample Exercises
1. Install and start Apache and Nginx on your system.
2. Configure a virtual host in Apache and a server block in Nginx.
3. Set up Nginx as a reverse proxy for a backend service.
4. Enable HTTPS using Let's Encrypt.
5. Analyze web server logs for errors and suspicious activity.

## Solutions
1. **Install web servers:**
   ```bash
   # Ubuntu/Debian
   apt update && apt install apache2 nginx
   systemctl start apache2 nginx
   systemctl enable apache2 nginx
   ```

2. **Configure virtual hosts:**
   ```bash
   # Apache
   sudo nano /etc/apache2/sites-available/mysite.conf
   sudo a2ensite mysite.conf
   sudo systemctl reload apache2
   
   # Nginx
   sudo nano /etc/nginx/sites-available/mysite
   sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

3. **Reverse proxy setup:**
   ```bash
   # Nginx reverse proxy config
   location /api/ {
       proxy_pass http://localhost:5000/;
       proxy_set_header Host $host;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   }
   ```

4. **Enable HTTPS:**
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   ```

5. **Log analysis:**
   ```bash
   tail -f /var/log/nginx/error.log
   grep "404" /var/log/apache2/access.log | tail -10
   ```

## Sample Interview Questions
1. What is the difference between Apache and Nginx?
2. How do you configure a virtual host in Apache? A server block in Nginx?
3. What is a reverse proxy and why use it?
4. How do you enable HTTPS on a web server?
5. How do you troubleshoot a web server that won't start?
6. How do you restrict access to admin interfaces?
7. How do you monitor and analyze web server logs?
8. What are the security best practices for web servers?
9. How do you set up load balancing with Nginx?
10. How do you serve static and dynamic content?

## Interview Question Answers
1. **Apache vs Nginx:** Apache uses process/thread model; Nginx is event-driven, better for high concurrency
2. **Virtual Hosts:** Apache: edit sites-available, use a2ensite; Nginx: create server blocks, link to sites-enabled
3. **Reverse Proxy:** Forwards client requests to backend servers for load balancing, SSL termination, caching
4. **HTTPS Setup:** Use Certbot for Let's Encrypt or manually configure SSL certificates in server config
5. **Troubleshooting:** Check syntax (nginx -t), review logs, verify port availability, test configuration
6. **Access Restriction:** Use IP restrictions, HTTP auth, firewall rules, or application-level security
7. **Log Analysis:** Use grep, awk, tail -f for real-time monitoring, log rotation for management
8. **Security Practices:** Run as non-root, keep updated, use HTTPS, restrict file permissions, monitor logs
9. **Load Balancing:** Use upstream blocks in Nginx or mod_proxy_balancer in Apache
10. **Content Types:** Static files served directly; dynamic content via FastCGI, WSGI, or reverse proxy

## Completion Checklist
- [ ] Can install and configure Apache and Nginx
- [ ] Know how to set up virtual hosts/server blocks
- [ ] Understand reverse proxy configuration
- [ ] Can implement SSL/TLS certificates
- [ ] Know how to troubleshoot web server issues
- [ ] Familiar with log analysis and monitoring

## Key Commands Summary
```bash
# Apache
systemctl start/stop/reload apache2
a2ensite/a2dissite sitename
apachectl configtest

# Nginx
systemctl start/stop/reload nginx
nginx -t                         # Test configuration
nginx -s reload                  # Reload config

# SSL/TLS
certbot --nginx -d domain.com    # Let's Encrypt
openssl req -new -x509           # Self-signed cert
```

## Best Practices
- Use HTTPS for all production sites
- Implement proper logging and monitoring
- Regular security updates and patches
- Use reverse proxy for application isolation
- Configure proper file permissions
- Monitor performance and resource usage

## Next Steps
Proceed to [Day 19: Advanced Linux Storage & Filesystems](../Day_19/notes_and_exercises.md) to learn storage management.
