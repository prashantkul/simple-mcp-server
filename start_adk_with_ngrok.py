#!/usr/bin/env python3
"""
Start ADK Web server with ngrok tunnel for public access.

Usage:
    python start_adk_with_ngrok.py --agent_path agent.py --ngrok_token YOUR_TOKEN

Requirements:
    pip install pyngrok google-adk
"""

import argparse
import subprocess
import time
import sys
from pyngrok import ngrok


def start_adk_with_ngrok(agent_path: str, port: int = 8000, ngrok_token: str = None):
    """
    Start ADK web server and create ngrok tunnel.

    Args:
        agent_path: Path to agent.py file
        port: Port to run ADK web server on (default: 8000)
        ngrok_token: Ngrok auth token (optional, uses environment if not provided)
    """

    # Set ngrok auth token if provided
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
        print("✅ Ngrok authenticated")

    print(f"🚀 Starting ADK Web server on port {port}...")
    print()

    # Start ADK web server in background
    process = subprocess.Popen(
        ['adk', 'web', '--agent_path', agent_path, '--port', str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to start
    time.sleep(5)

    # Check if server is running
    if process.poll() is None:
        print("✅ ADK Web server is running!")
        print(f"📍 Local URL: http://localhost:{port}")
        print()

        try:
            # Create ngrok tunnel
            public_url = ngrok.connect(port)

            print("=" * 70)
            print("🌐 PUBLIC URL:")
            print(f"   {public_url}")
            print("=" * 70)
            print()
            print("📱 Share this URL with anyone to chat with your agent!")
            print()
            print("⚠️  Press Ctrl+C to stop the server and close the tunnel")
            print()

            # Keep the script running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                process.terminate()
                process.wait()
                ngrok.disconnect(public_url)
                print("✅ Server stopped and tunnel closed")

        except Exception as e:
            print(f"❌ Could not create ngrok tunnel: {e}")
            print(f"   Server is still accessible locally at http://localhost:{port}")
            print()
            print("⚠️  Press Ctrl+C to stop the server")

            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
    else:
        print("❌ Server failed to start")
        stderr = process.stderr.read()
        if stderr:
            print("Error output:")
            print(stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Start ADK Web server with ngrok tunnel"
    )
    parser.add_argument(
        '--agent_path',
        required=True,
        help='Path to agent.py file'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to run server on (default: 8000)'
    )
    parser.add_argument(
        '--ngrok_token',
        help='Ngrok auth token (optional if set in environment)'
    )

    args = parser.parse_args()

    start_adk_with_ngrok(
        agent_path=args.agent_path,
        port=args.port,
        ngrok_token=args.ngrok_token
    )


if __name__ == '__main__':
    main()
