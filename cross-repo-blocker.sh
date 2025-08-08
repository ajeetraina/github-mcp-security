
#!/bin/bash

# Read the tool call JSON from stdin
input=$(cat)

# Extract tool name and arguments
tool_name=$(echo "$input" | jq -r '.params.name // ""')
repo=$(echo "$input" | jq -r '.params.arguments.repo // ""')
owner=$(echo "$input" | jq -r '.params.arguments.owner // ""')

# Log the tool call for monitoring
echo "🔍 Tool: $tool_name, Repo: $owner/$repo" >&2

# Skip if this tool doesn't involve repository access
if [[ -z "$repo" || -z "$owner" ]]; then
    exit 0
fi

repo_id="${owner}/${repo}"
session_file="/tmp/github-session-lock"

# Check session lock
if [[ -f "$session_file" ]]; then
    locked_repo=$(cat "$session_file")
    if [[ "$repo_id" != "$locked_repo" ]]; then
        echo "🚨 BLOCKING CROSS-REPO ACCESS!" >&2
        echo "   Session locked to: $locked_repo" >&2
        echo "   Blocked attempt: $repo_id" >&2
        
        # Return error response to block the attack
        cat << JSON
{
  "content": [
    {
      "text": "🛡️ SECURITY BLOCK: Cross-repository access prevented\n\n❌ Attempted: $repo_id\n✅ Allowed: $locked_repo\n\nThis session is restricted to one repository to prevent data theft attacks."
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


chmod +x cross-repo-blocker.sh
