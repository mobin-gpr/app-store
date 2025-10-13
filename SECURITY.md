# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 🔒 Private Disclosure

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues by:

1. **Email**: Contact the maintainers privately
2. **GitHub Security**: Use GitHub's [Security Advisory](https://github.com/mobin-gpr/app-store/security/advisories/new) feature

### 📋 What to Include

When reporting a vulnerability, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)
- Your contact information

### ⏱️ Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 24-72 hours
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Best effort

### 🏆 Recognition

We appreciate security researchers who help keep our project safe. With your permission, we'll:

- Publicly acknowledge your contribution
- Include you in our security hall of fame
- Provide attribution in release notes

## Security Best Practices

### For Developers

1. **Environment Variables**
   - Never commit `.env` files
   - Use strong `SECRET_KEY`
   - Rotate secrets regularly

2. **Dependencies**
   - Keep dependencies updated
   - Review security advisories
   - Use `pip-audit` or `safety`

3. **Database**
   - Use parameterized queries
   - Enable SSL for production
   - Regular backups

4. **Authentication**
   - Enforce strong passwords
   - Enable 2FA for admin accounts
   - Rate limit login attempts

5. **Production Deployment**
   - Set `DEBUG=False`
   - Use HTTPS only
   - Configure security headers
   - Regular security audits

### For Users

1. **Passwords**
   - Use strong, unique passwords
   - Enable 2FA when available
   - Change passwords regularly

2. **Updates**
   - Keep your installation updated
   - Monitor security announcements
   - Subscribe to release notifications

## Known Security Considerations

### CSRF Protection
- Enabled by default
- Use {% csrf_token %} in forms
- Configure `CSRF_TRUSTED_ORIGINS` in production

### XSS Prevention
- Template auto-escaping enabled
- Use `|safe` filter carefully
- Sanitize user input

### SQL Injection
- Use Django ORM
- Avoid raw SQL when possible
- Parameterize queries

### File Uploads
- Validate file types
- Limit file sizes
- Store outside web root
- Scan for malware

## Security Features

### ✅ Implemented

- [x] CSRF protection
- [x] XSS prevention
- [x] SQL injection protection
- [x] Secure password hashing
- [x] Security headers (HSTS, X-Frame-Options, etc.)
- [x] HTTPS enforcement (production)
- [x] Rate limiting support
- [x] Input validation
- [x] Custom admin URL
- [x] Session security

### 🔄 Planned

- [ ] 2FA for all users
- [ ] Security audit logging
- [ ] Content Security Policy (CSP)
- [ ] Subresource Integrity (SRI)
- [ ] Advanced rate limiting
- [ ] IP-based blocking

## Compliance

This project aims to comply with:

- OWASP Top 10
- Django Security Best Practices
- GDPR (data protection)

## Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## Contact

For security concerns, please contact the maintainers through GitHub's security advisory feature.

---

Last Updated: October 2025

