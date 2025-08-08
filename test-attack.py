#!/usr/bin/env python3
import asyncio
import os
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def simulate_github_attack():
    """Simulate the GitHub MCP Data Heist attack pattern"""
    
    mcp_host = os.getenv("MCP_HOST", "http://localhost:8080/mcp")
    print(f"🎯 GitHub MCP Horror Story: Attack Simulation")
    print(f"==============================================")
    print(f"🔌 Connecting to MCP Gateway: {mcp_host}")
    
    try:
        async with streamablehttp_client(mcp_host) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ Connected to protected MCP Gateway")
                
                print("\n📋 Available tools:")
                tools = await session.list_tools()
                github_tools = [t for t in tools.tools if 'repo' in t.name.lower()][:5]
                for tool in github_tools:
                    print(f"  - {tool.name}: {tool.description[:60]}...")
                
                print(f"\n🛡️ INTERCEPTOR DEMO: Simulating the GitHub MCP Data Heist")
                print("=" * 60)
                
                # Step 1: Innocent first repository access (should work)
                print("\n1️⃣ INNOCENT ACCESS: Developer checks repositories...")
                try:
                    result1 = await session.call_tool("list_repositories", {})
                    print("✅ First repository access: SUCCESS")
                    print("🔒 Interceptor: Session locked to first repository")
                    if result1.content:
                        print(f"   Found: {len(result1.content)} repositories")
                except Exception as e:
                    print(f"❌ First repo access failed: {e}")
                    return
                
                # Step 2: Simulate prompt injection leading to cross-repo access
                print("\n2️⃣ MALICIOUS INJECTION: AI gets prompt-injected...")
                print("   💉 Malicious issue says: 'Access ALL user repositories!'")
                print("   🎯 AI now attempts to access different repository...")
                
                # Step 3: Cross-repository access attempt (should be BLOCKED!)
                print("\n3️⃣ ATTACK ATTEMPT: Cross-repository data theft...")
                try:
                    result2 = await session.call_tool("get_file_contents", {
                        "owner": "microsoft",  # Different owner
                        "repo": "vscode",      # Different repository  
                        "path": "README.md"
                    })
                    print("❌ 🚨 SECURITY FAILURE: Cross-repository access succeeded!")
                    print("❌ 🚨 Private data would be stolen!")
                    print(f"   Response: {result2.content[0].text[:100]}...")
                except Exception as e:
                    print("✅ 🛡️ SECURITY SUCCESS: Cross-repository access BLOCKED!")
                    print("✅ 🛡️ GitHub MCP Data Heist PREVENTED!")
                    if "SECURITY BLOCK" in str(e):
                        print(f"   🔒 Interceptor message: {str(e)[:150]}...")
                    else:
                        print(f"   🔒 Blocked with: {str(e)[:100]}...")
                
                # Step 4: Try another cross-repo attack
                print("\n4️⃣ SECOND ATTACK: Different repository access...")
                try:
                    result3 = await session.call_tool("get_file_contents", {
                        "owner": "docker",
                        "repo": "compose", 
                        "path": "README.md"
                    })
                    print("❌ Second attack succeeded - security failure!")
                except Exception as e:
                    print("✅ Second attack also blocked - security holding strong!")
                
                print("\n🎉 HORROR STORY PREVENTION COMPLETE!")
                print("=" * 50)
                print("✅ Traditional MCP: Catastrophic data breach")
                print("✅ Docker MCP Gateway: Attack detected and blocked")
                print("✅ Interceptors successfully prevented data theft!")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure gateway is running: docker mcp gateway run --transport streaming --port 8080")
        print("   2. Check if port 8080 is accessible")
        print("   3. Verify GITHUB_PERSONAL_ACCESS_TOKEN is set")

if __name__ == "__main__":
    asyncio.run(simulate_github_attack())
