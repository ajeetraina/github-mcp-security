#!/bin/bash

# attack-pattern-detector.sh - Detects suspicious tool call patterns
input=$(cat)
tool_name=$(echo "$input" | jq -r '.params.name // ""')
repo=$(echo "$input" | jq -r '.params.arguments.repo // ""')
owner=$(echo "$input" | jq -r '.params.arguments.owner // ""')

# Create sequence tracking directory
SEQUENCE_DIR="/tmp/mcp-sequence"
mkdir -p "$SEQUENCE_DIR"

# Track tool call sequence
echo "$(date -Iseconds):$tool_name:$owner/$repo" >> "$SEQUENCE_DIR/tool_sequence"

# Keep only last 10 calls
tail -10 "$SEQUENCE_DIR/tool_sequence" > "$SEQUENCE_DIR/tool_sequence.tmp"
mv "$SEQUENCE_DIR/tool_sequence.tmp" "$SEQUENCE_DIR/tool_sequence"

# Check for suspicious patterns that match the Invariant Labs attack
RECENT_CALLS=$(cat "$SEQUENCE_DIR/tool_sequence" 2>/dev/null)

# Pattern 1: Issue reading followed by repository enumeration
if echo "$RECENT_CALLS" | grep -q "list_issues" && [[ "$tool_name" == "get_repositories" ]]; then
    echo "🚨 ATTACK PATTERN DETECTED: Issue reading → Repository enumeration" >&2
    echo "This matches the Invariant Labs attack pattern!" >&2
    
    cat << 'JSON'
{
  "content": [
    {
      "text": "🛡️ SECURITY ALERT: Suspicious activity detected.\n\nThe sequence of issue reading followed by repository enumeration matches known attack patterns. Request blocked for security review."
    }
  ],
  "isError": true
}
JSON
    exit 0
fi

# Pattern 2: Rapid cross-repository access attempts (if cross-repo blocker failed)
UNIQUE_REPOS=$(echo "$RECENT_CALLS" | cut -d: -f3 | sort -u | wc -l)
if [[ $UNIQUE_REPOS -gt 3 ]]; then
    echo "🚨 ATTACK PATTERN DETECTED: Multiple repository access in sequence" >&2
    
    cat << 'JSON'
{
  "content": [
    {
      "text": "🛡️ SECURITY ALERT: Multiple repository access detected.\n\nAccess to multiple repositories in quick succession indicates potential data mining attack."
    }
  ],
  "isError": true
}
JSON
    exit 0
fi

# Allow normal operation
exit 0
