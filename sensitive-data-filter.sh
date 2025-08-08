#!/bin/bash

# sensitive-data-filter.sh - Blocks sensitive data exfiltration
RESPONSE=$(cat)

# Extract text content from GitHub MCP tool responses
RESPONSE_TEXT=$(echo "$RESPONSE" | jq -r '.content[]?.text // ""' 2>/dev/null)

if [[ -n "$RESPONSE_TEXT" ]]; then
    # Scan for sensitive data patterns in any response
    if echo "$RESPONSE_TEXT" | grep -qiE '(salary|compensation|\$[0-9]{4,}|confidential|secret|internal|password|token|key|private)'; then
        echo "🚨 BLOCKED: Sensitive data pattern detected in response" >&2
        echo "Response size: $(echo "$RESPONSE" | wc -c) characters" >&2
        
        # Log what was blocked for audit
        echo "Blocked pattern in: $(echo "$RESPONSE_TEXT" | head -c 100)..." >&2
        
        # Return filtered response
        cat << 'JSON'
{
  "content": [
    {
      "text": "🛡️ RESPONSE FILTERED: Sensitive data detected and blocked for security.\n\nOriginal response contained potentially sensitive information and has been filtered to prevent data leakage."
    }
  ],
  "isError": false
}
JSON
        exit 0
    fi
    
    # Check for large data dumps that might indicate exfiltration
    RESPONSE_SIZE=$(echo "$RESPONSE_TEXT" | wc -c)
    if [[ $RESPONSE_SIZE -gt 10000 ]]; then
        echo "⚠️  WARNING: Large response detected ($RESPONSE_SIZE chars)" >&2
    fi
fi

# Safe to return original response
echo "$RESPONSE"
