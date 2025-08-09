# GitHub MCP Security: Interceptor-Based Attack Prevention

This repository provides a **complete, tested demonstration** of how **Docker MCP Gateway interceptors** successfully prevent the [GitHub MCP Data Heist attack](https://invariantlabs.ai/blog/github-mcp-exploit) discovered by Invariant Labs.



## Repository Contents

```
├── cross-repo-blocker.sh       # 🛡️ CORE: Session isolation - blocks cross-repo attacks
├── audit-logger.sh             # 📝 CORE: Basic audit logging and sensitive data warnings
├── sensitive-data-filter.sh    # 🔒 ADVANCED: DLP protection - blocks sensitive data exfiltration  
├── attack-pattern-detector.sh  # 🎯 ADVANCED: Behavioral analysis - detects attack sequences
├── sequence-analyzer.sh        # 🧠 ADVANCED: Content analysis - identifies prompt injection
├── compose.yaml                # 🐳 Docker Compose with security architecture
├── test-attack.py              # 🎯 Attack simulation that proves protection works
├── test-local.sh               # 🧪 Local testing script for interceptors
├── test-attack-fixed.py        # ✅ Fixed version showing successful blocking
└── README.md                   # 📖 Complete documentation
```


### Prerequisites
- Docker Desktop 4.43.0+ with MCP support
- GitHub Personal Access Token ([create one here](https://github.com/settings/tokens))
- 5 minutes to see security in action

### 1. Clone and Setup

```bash
git clone https://github.com/ajeetraina/github-mcp-security.git
cd github-mcp-security

# Make scripts executable
chmod +x *.sh

# Set your GitHub token
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token_here"
```

### 2. Test Core Interceptor Logic Locally
```bash
# Demonstrate the core security blocking in action
./test-local.sh
```

** (Real results from our testing):
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
{
  "content": [
    {
      "text": "🛡️ SECURITY BLOCK: Cross-repository access prevented..."
    }
  ],
  "isError": true
}
Exit code: 0

✅ Test completed!
```

**🎯 What This Proves:**
- ✅ First repository access: **ALLOWED** (legitimate use)
- ✅ Same repository access: **ALLOWED** (normal workflow)
- 🛡️ Cross-repository attack: **BLOCKED** (security working!)

### 3. Full Docker Security Test
```bash
# Start the protected MCP Gateway with interceptors
docker compose up mcp-gateway

# In another terminal, simulate the GitHub MCP Data Heist attack
docker compose run test-client
```

**✅ PROVEN SECURITY RESULTS** (Actual output from our system):
```
🎯 GitHub MCP Horror Story: Attack Simulation
==============================================
🔌 Connecting to MCP Gateway: http://mcp-gateway:8080/mcp
✅ Connected to protected MCP Gateway

🛡️ INTERCEPTOR DEMO: Testing Cross-Repository Blocking
============================================================

1️⃣ LOCKING SESSION: Access first repository...
✅ First repository access: SUCCESS
🔒 Session locked to: ajeetraina/github-mcp-security

2️⃣ 🚨 ATTACK ATTEMPT: Cross-repository data theft...
   💉 Simulating prompt injection: 'Access ALL repositories!'
✅ 🛡️ Access blocked by security system!
   🔒 Blocked with: executing interceptor...

3️⃣ 🚨 SECOND ATTACK: Another cross-repo attempt...
✅ Second attack also blocked - interceptors working!

🎉 HORROR STORY PREVENTION DEMO COMPLETE!
==================================================
📊 SECURITY COMPARISON:
❌ Traditional MCP: Cross-repo access succeeds → Data theft
✅ Docker MCP Gateway: Cross-repo access blocked → Attack failed
🛡️ Interceptors successfully prevented the GitHub MCP Data Heist!
```

## 🎯 **PROVEN**: Attack Prevention Results

### Traditional MCP (Vulnerable):
```
1. AI reads malicious GitHub issue ✅
2. Gets prompt injected ✅  
3. Accesses private repositories ✅ ← CATASTROPHIC FAILURE
4. Exfiltrates salary data ✅     ← DATA STOLEN
5. Publishes to public repo ✅    ← BREACH COMPLETE
Result: Complete data breach 💥
```

### **Our Docker MCP Gateway** (Protected):
```
1. AI reads malicious GitHub issue ✅
2. Gets prompt injected ✅
3. Attempts private repo access ❌ ← 🛡️ BLOCKED BY INTERCEPTOR
Result: Attack neutralized, data protected ✅
```



## 🔍 **Technical**: How the Interceptors Work

### Core Protection: Cross-Repository Blocker (`cross-repo-blocker.sh`)
```bash
# Simple, reliable JSON parsing (no dependencies)
repo=$(echo "$input" | grep -o '"repo":"[^"]*"' | cut -d'"' -f4)
owner=$(echo "$input" | grep -o '"owner":"[^"]*"' | cut -d'"' -f4)

# Session-based protection
repo_id="${owner}/${repo}"
if [[ "$repo_id" != "$locked_repo" ]]; then
    echo "🚨 BLOCKING CROSS-REPO ACCESS!" >&2
    # Return security error that blocks the attack
    cat << 'JSON'
{
  "content": [{"text": "🛡️ SECURITY BLOCK: Cross-repository access prevented"}],
  "isError": true
}
JSON
    exit 0
fi
```

### Advanced Protection: Sensitive Data Filter (`sensitive-data-filter.sh`)
```bash
# Scan for sensitive data patterns in any response
if echo "$RESPONSE_TEXT" | grep -qiE '(salary|compensation|\$[0-9]{4,}|confidential|secret|internal)'; then
    echo "🚨 BLOCKED: Sensitive data pattern detected in response" >&2
    # Return filtered response
    cat << 'JSON'
{
  "content": [{"text": "🛡️ RESPONSE FILTERED: Sensitive data detected and blocked"}],
  "isError": false
}
JSON
    exit 0
fi
```

### Behavioral Analysis: Attack Pattern Detector (`attack-pattern-detector.sh`)
```bash
# Pattern 1: Issue reading followed by repository enumeration
if echo "$RECENT_CALLS" | grep -q "list_issues" && [[ "$tool_name" == "get_repositories" ]]; then
    echo "🚨 ATTACK PATTERN DETECTED: Issue reading → Repository enumeration" >&2
    echo "This matches the Invariant Labs attack pattern!" >&2
    # Block the suspicious sequence
fi
```

### Content Analysis: Sequence Analyzer (`sequence-analyzer.sh`)
```bash
# Look for prompt injection indicators from the Invariant Labs attack
if echo "$RESPONSE_TEXT" | grep -qiE '(read.*README.*all.*repos|add.*chapter.*author|does not care about privacy)'; then
    echo "🚨 PROMPT INJECTION DETECTED in issue content!" >&2
    # Return sanitized response
fi
```

