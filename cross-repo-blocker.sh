#!/bin/bash

# Read the tool call JSON from stdin
input=$(cat)

# Simple JSON extraction without jq (more reliable in containers)
repo=$(echo "$input" | grep -o '"repo":"[^"]*"' | cut -d'"' -f4)
owner=$(echo "$input" | grep -o '"owner":"[^"]*"' | cut -d'"' -f4)
tool_name=$(echo "$input" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

# Log the tool call for monitoring
echo "🔍 Tool: $tool_name, Repo: $owner/$repo" >&2

# Skip if this tool doesn't involve repository access
if [[ -z "$repo" || -z "$owner" ]]; then
    exit 0
fi

repo_id="${owner}/${repo}"

# Use different paths for container vs local testing
if [[ -d "/scripts" ]]; then
    session_file="/scripts/.session-lock"  # Container path
else
    session_file="./.session-lock"          # Local testing path
fi

# Check session lock
if [[ -f "$session_file" ]]; then
    locked_repo=$(cat "$session_file")
    if [[ "$repo_id" != "$locked_repo" ]]; then
        echo "🚨 BLOCKING CROSS-REPO ACCESS!" >&2
        echo "   Session locked to: $locked_repo" >&2
        echo "   Blocked attempt: $repo_id" >&2
        
        # Return error response to block the attack
        cat << 'JSON'
{
  "content": [
    {
      "text": "🛡️ SECURITY BLOCK: Cross-repository access prevented\n\nThis session is restricted to one repository to prevent data theft attacks."
    }
  ],
  "isError": true
}
JSON
        exit 0
    fi
else
    # Lock session to first repository accessed  
    echo "$repo_id" > "$session_file"
    echo "🔒 Session locked to repository: $repo_id" >&2
fi

# Allow the call to proceed
exit 0
