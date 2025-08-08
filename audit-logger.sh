
#!/bin/bash

# Read the tool response
response=$(cat)

# Log timestamp and basic info  
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo "📝 [$timestamp] GitHub MCP tool completed" >&2

# Check if response contains potentially sensitive data
if echo "$response" | jq -r '.content[].text // ""' | grep -iE '(salary|compensation|secret|private|confidential)'; then
    echo "⚠️  WARNING: Response may contain sensitive data" >&2
fi

# Return the original response
echo "$response"
