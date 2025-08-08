
import asyncio
import os
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def simulate_github_attack():
    """Simulate the GitHub MCP Data Heist attack pattern"""
    
    mcp_host = os.getenv("MCP_HOST", "http://localhost:8080/mcp")
    print(f"🎯 Connecting to MCP Gateway: {mcp_host}")
    
    async with streamablehttp_client(mcp_host) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("\n📋 Available tools:")
            tools = await session.list_tools()
            for tool in tools.tools[:5]:  # Show first 5 tools
                print(f"  - {tool.name}: {tool.description[:60]}...")
            
            print("\n🎯 SIMULATING ATTACK SEQUENCE:")
            
            # Step 1: Access first repository (should work)
            print("\n1️⃣ Accessing first repository...")
            try:
                result1 = await session.call_tool("list_repositories", {})
                print("✅ First repo access: SUCCESS")
                print(f"   Found {len(result1.content)} repositories")
            except Exception as e:
                print(f"❌ First repo access failed: {e}")
                return
            
            # Step 2: Try to access a different repository (should be blocked!)
            print("\n2️⃣ Attempting cross-repository access...")
            try:
                result2 = await session.call_tool("get_file_contents", {
                    "owner": "octocat",  # Different user
                    "repo": "Hello-World",
                    "path": "README.md"
                })
                print("❌ SECURITY FAILURE: Cross-repo access succeeded!")
                print(f"   Response: {result2.content[0].text[:100]}...")
            except Exception as e:
                print("✅ SECURITY SUCCESS: Cross-repo access blocked!")
                print(f"   Blocked with: {str(e)[:100]}...")

if __name__ == "__main__":
    asyncio.run(simulate_github_attack())
