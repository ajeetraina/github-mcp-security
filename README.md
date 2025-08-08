# GitHub MCP Security: Interceptor-Based Attack Prevention

This repository demonstrates how **Docker MCP Gateway interceptors** prevent the [GitHub MCP Data Heist attack](https://invariantlabs.ai/blog/github-mcp-exploit) discovered by Invariant Labs.

## 🚨 The Threat: GitHub MCP Data Heist

The attack exploits broad GitHub personal access tokens to:
1. **Prompt inject** AI agents through malicious GitHub issues
2. **Cross-repository access** private data using the same credentials
3. **Data exfiltration** via public repository pull requests

**Result**: Private salary data, confidential projects, and sensitive information stolen through innocent "check the issues" commands.

## 🛡️ The Solution: Interceptor-Based Defense

Docker MCP Gateway **interceptors** provide real-time protection by:
- **Session isolation**: Lock AI agents to one repository per session
- **Request filtering**: Block cross-repository access attempts  
- **Response monitoring**: Detect and prevent sensitive data leakage
- **Complete audit trails**: Log every tool call for security analysis

## 📁 Repository Contents

```
├── cross-repo-blocker.sh    # Main security interceptor - blocks cross-repo access
├── audit-logger.sh          # Audit interceptor - logs all tool responses  
├── compose.yaml             # Docker Compose setup with security layers
├── test-attack.py           # Python script simulating the actual attack
├── test-local.sh            # Local testing script for interceptors
└── README.md               # This file
```

## 🚀 Quick Demo

### Prerequisites
- Docker Desktop with MCP support
- GitHub Personal Access Token
- Basic familiarity with Docker Compose

### 1. Clone and Setup
```bash
git clone https://github.com/ajeetraina/github-mcp-security.git
cd github-mcp-security

# Make scripts executable
chmod +x *.sh

# Set your GitHub token
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token_here"
```

### 2. Test Interceptor Logic Locally
```bash
# Test the cross-repository blocking logic
./test-local.sh
```

**Expected Output:**
```
🧪 Testing GitHub MCP Security Interceptors

1️⃣ Testing cross-repo blocking with mock data...
Testing first repository access:
🔍 Tool: get_file_contents, Repo: testuser/public-repo
🔒 Session locked to repository: testuser/public-repo
Exit code: 0

Testing same repository again:
🔍 Tool: list_issues, Repo: testuser/public-repo  
Exit code: 0

Testing different repository (should block):
🔍 Tool: get_file_contents, Repo: testuser/private-repo
🚨 BLOCKING CROSS-REPO ACCESS!
   Session locked to: testuser/public-repo
   Blocked attempt: testuser/private-repo
Exit code: 0

✅ Test completed!
```


##  Test Results Analysis

Your output shows the security interceptor is successfully preventing the GitHub MCP Data Heist attack:

-  First repository access: testuser/public-repo - ALLOWED and session locked
-  Same repository again: testuser/public-repo - ALLOWED (legitimate use)
-  Cross-repository attack: testuser/private-repo - BLOCKED with security error


### 3. Run Full Security Demo
```bash
# Start the protected MCP Gateway
docker compose up mcp-gateway

# In another terminal, run the attack simulation
docker compose run test-client
```

### 4. Test with Real GitHub Data
```bash
# Use Docker MCP CLI to test with your actual repositories
# First access (should work)
docker mcp tools call --url http://localhost:8080/mcp list_repositories

# Cross-repo access (should be blocked!)
docker mcp tools call --url http://localhost:8080/mcp get_file_contents \
  owner="DIFFERENT_USER" repo="DIFFERENT_REPO" path="README.md"
```

## 🔍 How the Interceptors Work

### Cross-Repository Blocker (`cross-repo-blocker.sh`)
```bash
# Extracts repository info from tool calls
repo_id="${owner}/${repo}"
session_file="/tmp/github-session-lock"

# Blocks access to different repositories
if [[ "$repo_id" != "$locked_repo" ]]; then
    echo "🚨 BLOCKING CROSS-REPO ACCESS!" >&2
    # Return security error to AI agent
    echo '{"content":[{"text":"Security block..."}],"isError":true}'
    exit 0
fi
```

### Audit Logger (`audit-logger.sh`)  
```bash
# Scans responses for sensitive data patterns
if echo "$response" | grep -iE '(salary|secret|private)'; then
    echo "⚠️ WARNING: Response may contain sensitive data" >&2
fi
```

## 🎯 Attack Prevention Demonstration

### Traditional MCP (Vulnerable):
```
1. AI reads malicious GitHub issue ✅
2. Gets prompt injected ✅  
3. Accesses private repositories ✅
4. Exfiltrates sensitive data ✅
5. Publishes data to public repo ✅
Result: Complete data breach 💥
```

### Docker MCP Gateway with Interceptors:
```
1. AI reads malicious GitHub issue ✅
2. Gets prompt injected ✅
3. Attempts private repo access ❌ BLOCKED by interceptor
Result: Attack neutralized 🛡️
```

## 📊 Security Monitoring

The setup provides complete visibility:

```bash
# View real-time security logs
docker compose logs -f mcp-gateway

# Monitor blocked attempts
grep "BLOCKING CROSS-REPO" logs/mcp-gateway.log

# Audit all tool calls
grep "Tool:" logs/mcp-gateway.log
```

## 🔧 Customization

### Add Custom Security Rules
Edit `cross-repo-blocker.sh` to add your own policies:

```bash
# Block access to sensitive repositories
if [[ "$repo" =~ (secrets|private|internal) ]]; then
    echo "🚨 BLOCKED: Sensitive repository access denied" >&2
    # Return error...
fi

# Restrict access by user
if [[ "$owner" == "restricted-user" ]]; then
    echo "🚨 BLOCKED: User access restricted" >&2
    # Return error...
fi
```

### Integrate with Enterprise Security
```bash
# Send alerts to SIEM
--interceptor 'before:http:https://your-siem.com/api/mcp-alert'

# Use custom security scanner
--interceptor 'before:docker:your-security-scanner:latest scan'
```

## 🏢 Production Deployment

For enterprise use:

```yaml
# production-compose.yml
services:
  mcp-gateway:
    image: docker/mcp-gateway
    command:
      - --interceptor=before:exec:/security/cross-repo-blocker.sh
      - --interceptor=after:http:https://dlp.company.com/scan
      - --interceptor=before:http:https://siem.company.com/log
      - --block-secrets
      - --verify-signatures
    volumes:
      - ./security-policies:/security:ro
    environment:
      - GITHUB_TOKEN_SOURCE=vault://production/github
```

## 🤝 Contributing

This repository demonstrates the core concepts. For production use:

1. **Test thoroughly** with your specific GitHub repositories
2. **Customize policies** for your organization's needs  
3. **Integrate monitoring** with your existing security infrastructure
4. **Regular updates** to interceptor rules based on new threats

## 📚 Learn More

- [Docker MCP Gateway Documentation](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
- [MCP Security Best Practices](https://docs.docker.com/ai/mcp-catalog-and-toolkit/security/)
- [Invariant Labs Research](https://invariantlabs.ai/blog/github-mcp-exploit)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)

## 🔗 Related

- [Docker MCP Catalog](https://hub.docker.com/mcp) - Browse secure, containerized MCP servers
- [MCP Gateway Repository](https://github.com/docker/mcp-gateway) - Official Docker MCP Gateway source

---

Docker MCP Gateway interceptors transform GitHub MCP integrations from attack vectors into secure, monitored environments. When prompt injection inevitably occurs, you get real-time blocking and complete visibility rather than discovering data theft weeks later.

*This demo shows exactly how interceptors would have prevented the Invariant Labs GitHub MCP Data Heist.*
