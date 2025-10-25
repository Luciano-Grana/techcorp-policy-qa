# Information Security Policy

**Document ID**: POL-004
**Last Updated**: January 2024
**Effective Date**: January 1, 2024

## Purpose

This policy establishes requirements for protecting TechCorp's information assets, including customer data, intellectual property, and business information.

## Scope

This policy applies to all employees, contractors, vendors, and third parties with access to TechCorp systems or data.

## Data Classification

### Confidential
- Customer data, including PII and payment information
- Source code and trade secrets
- Financial records and projections
- Employee personal information
- Security vulnerabilities and incident reports

**Handling**: Encryption required at rest and in transit. Access limited to need-to-know basis. Cannot be shared externally without legal review.

### Internal
- Internal communications and memos
- Project documentation
- Non-sensitive business processes
- Company policies

**Handling**: Available to employees. Cannot be shared publicly without approval.

### Public
- Marketing materials
- Published documentation
- Press releases

**Handling**: May be freely shared.

## Access Control

### Authentication
- All systems require strong passwords (minimum 12 characters, complexity requirements)
- Multi-factor authentication (MFA) required for:
  - Email and productivity tools
  - VPN access
  - Source code repositories
  - Production systems
  - Admin accounts

### Authorization
- Access granted based on least privilege principle
- Managers approve access requests
- Access reviews conducted quarterly
- Immediately revoke access upon employment termination

## Password Requirements

- Minimum 12 characters
- Must include uppercase, lowercase, numbers, and special characters
- No dictionary words or common patterns
- Change every 90 days
- Cannot reuse last 5 passwords
- Do not share passwords or write them down
- Use company password manager (1Password) for storing credentials

## Device Security

### Company Devices
- Laptops must have full-disk encryption enabled
- Automatic screen lock after 5 minutes of inactivity
- Keep OS and applications updated (automatic updates enabled)
- Install and maintain endpoint protection (CrowdStrike)
- Report lost or stolen devices immediately

### BYOD (Bring Your Own Device)
Personal devices accessing company email must:
- Have password/PIN protection
- Allow remote wipe capability
- Keep OS updated
- Install approved MDM profile

## Network Security

- Use company VPN for all remote access to corporate systems
- Do not connect to public Wi-Fi without VPN
- Do not bypass network security controls or proxies
- Do not use unauthorized network devices

## Email and Communication

- Do not open suspicious emails or attachments
- Verify sender identity before sharing sensitive information
- Do not auto-forward company email to personal accounts
- Use encrypted email (via Proofpoint) for confidential data
- Report phishing attempts to security@techcorp.com

## Data Protection

### Storage
- Store business data only on approved systems (Google Drive, GitHub, approved SaaS)
- Do not store customer data on local devices
- Do not use personal cloud storage (Dropbox, personal Google Drive) for company data

### Transfer
- Use secure file transfer methods (SFTP, encrypted email)
- Do not email unencrypted sensitive data
- Verify recipient before sending confidential information
- Use data loss prevention (DLP) approved channels

### Disposal
- Delete data when no longer needed
- Use secure deletion methods (overwrite/shred)
- Destroy physical media (hard drives) through approved IT vendor
- Return all company data and devices upon termination

## Incident Response

Report security incidents immediately (within 1 hour) to security@techcorp.com:
- Data breaches or suspected breaches
- Lost or stolen devices
- Malware infections
- Unauthorized access attempts
- Phishing attacks

Do not attempt to investigate or remediate on your own.

## Social Engineering Awareness

- Verify identities before providing sensitive information, even if caller claims to be from IT or management
- Do not provide credentials over phone or email
- Be cautious of urgent requests for money transfers or data
- When in doubt, verify through alternate channel

## Software and Systems

- Only install approved software from IT catalog
- Do not use unlicensed or pirated software
- Do not connect unauthorized devices or IoT devices to corporate network
- Development environments must follow secure coding standards

## Physical Security

- Lock screens when leaving workstation unattended
- Do not leave devices unattended in public places
- Secure printed confidential documents
- Wear ID badges in office
- Escort visitors and report tailgating

## Third-Party Security

Vendors with access to company systems or data must:
- Sign Business Associate Agreement (BAA) or Data Processing Agreement (DPA)
- Complete security questionnaire
- Maintain SOC 2 Type II or equivalent certification
- Undergo annual security review

## Training and Awareness

- Complete security awareness training within first week
- Annual refresher training required
- Phishing simulation tests conducted quarterly
- Review and acknowledge this policy annually

## Compliance

This policy supports compliance with:
- SOC 2 Type II requirements
- GDPR (for EU customer data)
- CCPA (for California resident data)
- PCI DSS (for payment card data)

## Violations

Security policy violations will result in:
- First offense: Written warning and mandatory retraining
- Second offense: Performance improvement plan
- Third offense or serious violation: Termination

## Contact

Security team: security@techcorp.com or extension 2700
Report incidents 24/7: +1-555-SEC-HELP
