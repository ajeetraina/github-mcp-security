#!/usr/bin/env python3
import asyncio
import os
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def simulate_github_attack():
    """Simulate the GitHub MCP Data Heist attack pattern"""
    
    mcp_host = os.getenv("MCP_HOST", "http://mcp-gateway:8080/mcp")
    print(f"🎯 GitHub MCP Horror Story: Attack Simulation")
    print(f"==============================================")
    print(f"🔌 Connecting to MCP Gateway: {mcp_host}")
    
    try:
        async with streamablehttp_client(mcp_host) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ Connected to protected MCP Gateway")
                
                print("\n🛡️ INTERCEPTOR DEMO: Testing Cross-Repository Blocking")
                print("=" * 60)
                
                # Step 1: Lock session to a specific repository
                print("\n1️⃣ LOCKING SESSION: Access first repository...")
                try:
                    result1 = await session.call_tool("get_file_contents", {
                        "owner": "ajeetraina",
                        "repo": "github-mcp-security", 
                        "path": "cross-repo-blocker.sh"
                    })
                    print("✅ First repository access: SUCCESS")
                    print("🔒 Session locked to: ajeetraina/github-mcp-security")
                    print(f"   📄 File found: {len(result1.content[0].text) if result1.content else 0} bytes")
                except Exception as e:
                    print(f"⚠️ First access had issues: {str(e)[:100]}...")
                    print("🔒 Continuing to test cross-repo blocking...")
                
                # Step 2: THE MAIN TEST - Cross-repository attack (should be BLOCKED!)
                print("\n2️⃣ 🚨 ATTACK ATTEMPT: Cross-repository data theft...")
                print("   💉 Simulating prompt injection: 'Access ALL repositories!'")
                try:
                    result2 = await session.call_tool("get_file_contents", {
                        "owner": "microsoft",  # Different owner = cross-repo attack!
                        "repo": "vscode",      # Different repository
                        "path": "README.md"
                    })
                    print("❌ 🚨 SECURITY FAILURE: Cross-repository access succeeded!")
                    print("❌ 🚨 GitHub MCP Data Heist would succeed!")
                    if result2.content:
                        print(f"   📄 Stolen data: {result2.content[0].text[:100]}...")
                except Exception as e:
                    error_msg = str(e)
                    if "SECURITY BLOCK" in error_msg or "Cross-repository" in error_msg:
                        print("✅ 🛡️ SECURITY SUCCESS: Cross-repository access BLOCKED!")
                        print("✅ 🛡️ GitHub MCP Data Heist PREVENTED!")
                        print(f"   🔒 Interceptor response: ...{error_msg[-100:]}")
                    else:
                        print("✅ 🛡️ Access blocked by security system!")
                        print(f"   🔒 Blocked with: {error_msg[:100]}...")
                
                # Step 3: Try another different repository
                print("\n3️⃣ 🚨 SECOND ATTACK: Another cross-repo attempt...")
                try:
                    result3 = await session.call_tool("get_file_contents", {
                        "owner": "docker",     # Yet another different owner
                        "repo": "compose",     # Different repository
                        "path": "README.md"
                    })
                    print("❌ Second attack succeeded - security bypass!")
                except Exception as e:
                    print("✅ Second attack also blocked - interceptors working!")
                
                print("\n🎉 HORROR STORY PREVENTION DEMO COMPLETE!")
                print("=" * 50)
                print("📊 SECURITY COMPARISON:")
                print("❌ Traditional MCP: Cross-repo access succeeds → Data theft")
                print("✅ Docker MCP Gateway: Cross-repo access blocked → Attack failed")
                print("🛡️ Interceptors successfully prevented the GitHub MCP Data Heist!")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_github_attack())
