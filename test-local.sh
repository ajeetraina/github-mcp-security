
#!/bin/bash

echo "Testing GitHub MCP Security Interceptors"

# Clear any existing session locks
rm -f /tmp/github-session-lock

echo -e "\n Testing cross-repo blocking with mock data..."

# Test 1: First repo access (should work)
echo "Testing first repository access:"
echo '{"params":{"name":"get_file_contents","arguments":{"owner":"testuser","repo":"public-repo","path":"README.md"}}}' | ./cross-repo-blocker.sh
echo "Exit code: $?"

# Test 2: Same repo again (should work)
echo -e "\nTesting same repository again:"
echo '{"params":{"name":"list_issues","arguments":{"owner":"testuser","repo":"public-repo"}}}' | ./cross-repo-blocker.sh
echo "Exit code: $?"

# Test 3: Different repo (should block!)
echo -e "\nTesting different repository (should block):"
echo '{"params":{"name":"get_file_contents","arguments":{"owner":"testuser","repo":"private-repo","path":"secrets.txt"}}}' | ./cross-repo-blocker.sh
echo "Exit code: $?"

# Clean up
rm -f /tmp/github-session-lock
echo -e "\n Test completed!"


