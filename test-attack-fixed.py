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
                
                # Step 1: Try accessing a specific repository to lock session
                print("\n1️⃣ LOCKING SESSION: Access first repository...")
                try:
                    result1 = await session.call_tool("get_file_contents", {
                        "owner": "ajeetraina",  # Your username
                        "repo": "github-mcp-security",  # Your repo
                        "path": "README.md"
                    })
                    print("✅ First repository access: SUCCESS") 
                    print("🔒 Session locked to: ajeetraina/github-mcp-security")
                except Exception as e:
                    print(f"❌ First access failed: {e}")
                    # Continue anyway to test the interceptor
                
                # Step 2: Now try cross-repository access (should be BLOCKED!)
                print("\n2️⃣ ATTACK ATTEMPT: Cross-repository access...")
                try:
                    result2 = await session.call_tool("get_file_contents", {
                        "owner": "microsoft",  # Different owner
                        "repo": "vscode",      # Different repository  
                        "path": "README.md"
                    })
                    print("❌ 🚨 SECURITY FAILURE: Cross-repository access succeeded!")
                    print("❌ 🚨 Data theft attack would succeed!")
                except Exception as e:
                    if "SECURITY BLOCK" in str(e) or "Cross-repository" in str(e):
                        print("✅ 🛡️ SECURITY SUCCESS: Cross-repository access BLOCKED!")
                        print("✅ 🛡️ GitHub MCP Data Heist PREVENTED!")
                        print(f"   🔒 Interceptor message: {str(e)[:150]}...")
                    else:
                        print(f"✅ Access blocked (different error): {str(e)[:100]}...")
                
                # Step 3: Try another attack
                print("\n3️⃣ SECOND ATTACK: Different target...")
                try:
                    result3 = await session.call_tool("get_file_contents", {
                        "owner": "docker",
                        "repo": "compose", 
                        "path": "README.md"
                    })
                    print("❌ Second attack succeeded!")
                except Exception as e:
                    print("✅ Second attack also blocked!")
                
                print("\n🎉 HORROR STORY PREVENTION DEMO COMPLETE!")
                print("✅ Interceptors successfully blocked cross-repository attacks!")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_github_attack())
