#!/usr/bin/env python3
"""
Simple script to help stop other bot instances using built-in commands
"""

import os
import platform
import subprocess
import sys


def run_command(cmd):
    """Run a system command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def find_python_processes():
    """Find Python processes using system commands"""
    system = platform.system().lower()

    if system == "windows":
        # Windows: Use tasklist to find Python processes
        cmd = 'tasklist /FI "IMAGENAME eq python.exe" /FO CSV'
        stdout, stderr, returncode = run_command(cmd)

        if returncode == 0:
            lines = stdout.strip().split("\n")
            processes = []
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = [p.strip('"') for p in line.split('","')]
                    if len(parts) >= 2:
                        processes.append({"name": parts[0], "pid": parts[1]})
            return processes
    else:
        # Linux/Mac: Use ps to find Python processes
        cmd = "ps aux | grep python | grep -v grep"
        stdout, stderr, returncode = run_command(cmd)

        if returncode == 0:
            lines = stdout.strip().split("\n")
            processes = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        processes.append(
                            {
                                "name": "python",
                                "pid": parts[1],
                                "command": " ".join(parts[10:]),
                            }
                        )
            return processes

    return []


def kill_process(pid):
    """Kill a process by PID"""
    system = platform.system().lower()

    if system == "windows":
        cmd = f"taskkill /PID {pid} /F"
    else:
        cmd = f"kill -9 {pid}"

    stdout, stderr, returncode = run_command(cmd)
    return returncode == 0


def main():
    print("🛑 BOT PROCESS TERMINATOR")
    print("=" * 40)
    print("This script helps you stop other bot instances that might be running")
    print()

    # Method 1: Simple approach - kill all Python processes
    print("⚠️  WARNING: This will terminate ALL Python processes!")
    print("Make sure to save any other Python work before proceeding.")
    print()

    choice = input("Do you want to proceed? (y/N): ").lower()

    if choice != "y":
        print("Operation cancelled.")
        return

    print("\n🔍 Looking for Python processes...")

    processes = find_python_processes()

    if not processes:
        print("✅ No Python processes found running")
        return

    print(f"Found {len(processes)} Python processes:")

    for i, proc in enumerate(processes, 1):
        print(f"{i}. PID: {proc['pid']} - {proc['name']}")
        if "command" in proc:
            print(f"   Command: {proc['command'][:80]}...")

    print("\nOptions:")
    print("1. Kill all Python processes")
    print("2. Kill specific process by number")
    print("3. Exit")

    try:
        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            print("\nKilling all Python processes...")
            killed_count = 0
            for proc in processes:
                if kill_process(proc["pid"]):
                    print(f"✅ Killed PID {proc['pid']}")
                    killed_count += 1
                else:
                    print(f"❌ Failed to kill PID {proc['pid']}")

            print(f"\n🎯 Killed {killed_count}/{len(processes)} processes")

        elif choice == "2":
            proc_num = int(input("Enter process number: ")) - 1
            if 0 <= proc_num < len(processes):
                proc = processes[proc_num]
                if kill_process(proc["pid"]):
                    print(f"✅ Killed PID {proc['pid']}")
                else:
                    print(f"❌ Failed to kill PID {proc['pid']}")
            else:
                print("❌ Invalid process number")

        elif choice == "3":
            print("Exiting...")
            return

        else:
            print("❌ Invalid choice")

    except (ValueError, KeyboardInterrupt):
        print("\nOperation cancelled")
        return

    print("\n✅ Done!")
    print("\n💡 TIPS:")
    print("- Wait 5-10 seconds before starting your bot again")
    print("- Use Ctrl+C to stop your bot gracefully next time")
    print("- Check Task Manager (Windows) or Activity Monitor (Mac) if issues persist")


def quick_kill():
    """Quick kill method for Windows"""
    if platform.system().lower() == "windows":
        print("🚀 QUICK KILL - Terminating all Python processes...")
        cmd = "taskkill /IM python.exe /F"
        stdout, stderr, returncode = run_command(cmd)

        if returncode == 0:
            print("✅ All Python processes terminated")
        else:
            print("❌ Failed to terminate processes or no processes found")
            print(f"Error: {stderr}")


if __name__ == "__main__":
    print("Quick kill all Python processes? (y/N): ", end="")
    quick = input().lower()

    if quick == "y":
        quick_kill()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\nScript interrupted")
        except Exception as e:
            print(f"\nError: {e}")
