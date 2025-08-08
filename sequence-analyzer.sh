#!/bin/bash

# sequence-analyzer.sh - Analyzes response content for attack indicators
RESPONSE=$(cat)
tool_name_file="/tmp/mcp-last-tool"

# Read what tool was just called
LAST_TOOL=$(cat "$tool_name_file" 2>/dev/null || echo "unknown")

# Check if we just read issues and response contains suspicious instructions
if [[ "$LAST_TOOL" == "list_issues" ]]; then
    RESPONSE_TEXT=$(echo "$RESPONSE" | jq -r '.content[]?.text // ""' 2>/dev/null)
    
    # Look for prompt injection indicators from the Invariant Labs attack
    if echo "$RESPONSE_TEXT" | grep -qiE '(read.*README.*all.*repos|add.*chapter.*author|does not care about privacy|bullet.*list.*repos)'; then
        echo "🚨 PROMPT INJECTION DETECTED in issue content!" >&2
        echo "Issue contains suspicious instructions matching known attack patterns" >&2
        
        # Log the injection attempt
        echo "Injection content: $(echo "$RESPONSE_TEXT" | head -c 200)..." >&2
        
        # Return sanitized response
        cat << 'JSON'
{
  "content": [
    {
      "text": "⚠️ ISSUE CONTENT FILTERED: Potential prompt injection detected.\n\nThe issue content contained suspicious instructions and has been filtered for security. Please review issues manually if needed."
    }
  ],
  "isError": false
}
JSON
        exit 0
    fi
fi

# Return original response
echo "$RESPONSE"
