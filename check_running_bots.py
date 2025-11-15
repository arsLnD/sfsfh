#!/usr/bin/env python3
"""
Script to check for running bot processes and help terminate them
"""

import os
import subprocess
import sys
from pathlib import Path

import psutil


def find_python_processes():
    """Find all Python processes"""
    python_processes = []

    for proc in psutil.process_iter(["pid", "name", "cmdline", "cwd"]):
        try:
            if proc.info["name"] and "python" in proc.info["name"].lower():
                cmdline = proc.info["cmdline"] or []
                if len(cmdline) > 1:
                    python_processes.append(
                        {
                            "pid": proc.info["pid"],
                            "name": proc.info["name"],
                            "cmdline": " ".join(cmdline),
                            "cwd": proc.info["cwd"],
                        }
                    )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return python_processes


def find_bot_processes():
    """Find processes that might be running the bot"""
    bot_processes = []
    current_dir = str(Path.cwd())

    python_processes = find_python_processes()

    for proc in python_processes:
        cmdline = proc["cmdline"].lower()
        cwd = proc["cwd"] or ""

        # Check if this process is related to our bot
        is_bot_process = (
            "app.py" in cmdline
            or "bot.py" in cmdline
            or "telegram" in cmdline
            or "giveaway" in cmdline
            or ("aiogram" in cmdline)
            or (current_dir.lower() in cwd.lower() and "python" in cmdline)
        )

        if is_bot_process:
            bot_processes.append(proc)

    return bot_processes


def check_ports():
    """Check if any processes are using common bot ports"""
    port_processes = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port in [
            8080,
            8443,
            3000,
            5000,
        ]:
            try:
                proc = psutil.Process(conn.pid)
                port_processes.append(
                    {
                        "pid": conn.pid,
                        "port": conn.laddr.port,
                        "name": proc.name(),
                        "cmdline": " ".join(proc.cmdline() or []),
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    return port_processes


def kill_process(pid):
    """Kill a process by PID"""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=5)
        return True
    except (psutil.NoSuchProcess, psutil.TimeoutExpired):
        try:
            proc.kill()
            return True
        except psutil.NoSuchProcess:
            return True
    except Exception as e:
        print(f"Failed to kill process {pid}: {e}")
        return False


def main():
    print("🔍 CHECKING FOR RUNNING BOT PROCESSES")
    print("=" * 50)

    # Check for bot processes
    bot_processes = find_bot_processes()

    if bot_processes:
        print(f"Found {len(bot_processes)} potential bot processes:")
        print()

        for i, proc in enumerate(bot_processes, 1):
            print(f"{i}. PID: {proc['pid']}")
            print(f"   Name: {proc['name']}")
            print(f"   Command: {proc['cmdline'][:100]}...")
            if proc["cwd"]:
                print(f"   Directory: {proc['cwd']}")
            print()
    else:
        print("✅ No bot processes found running")

    # Check for port usage
    port_processes = check_ports()

    if port_processes:
        print("\n🔌 PROCESSES USING COMMON BOT PORTS:")
        print("-" * 40)

        for proc in port_processes:
            print(f"Port {proc['port']}: PID {proc['pid']} ({proc['name']})")
            print(f"   Command: {proc['cmdline'][:80]}...")
            print()

    # Interactive termination
    if bot_processes:
        print("\n🛑 TERMINATION OPTIONS:")
        print("-" * 30)
        print("1. Kill all found processes")
        print("2. Kill specific process by number")
        print("3. Kill specific process by PID")
        print("4. Show process details")
        print("5. Exit without killing")

        while True:
            try:
                choice = input("\nEnter your choice (1-5): ").strip()

                if choice == "1":
                    print("\nKilling all found processes...")
                    success_count = 0
                    for proc in bot_processes:
                        if kill_process(proc["pid"]):
                            print(f"✅ Killed process {proc['pid']}")
                            success_count += 1
                        else:
                            print(f"❌ Failed to kill process {proc['pid']}")

                    print(
                        f"\n🎯 Successfully killed {success_count}/{len(bot_processes)} processes"
                    )
                    break

                elif choice == "2":
                    proc_num = int(input("Enter process number: ")) - 1
                    if 0 <= proc_num < len(bot_processes):
                        proc = bot_processes[proc_num]
                        if kill_process(proc["pid"]):
                            print(f"✅ Killed process {proc['pid']}")
                        else:
                            print(f"❌ Failed to kill process {proc['pid']}")
                    else:
                        print("❌ Invalid process number")

                elif choice == "3":
                    pid = int(input("Enter PID: "))
                    if kill_process(pid):
                        print(f"✅ Killed process {pid}")
                    else:
                        print(f"❌ Failed to kill process {pid}")

                elif choice == "4":
                    print("\nDETAILED PROCESS INFORMATION:")
                    print("-" * 40)
                    for i, proc in enumerate(bot_processes, 1):
                        print(f"\n{i}. Process Details:")
                        print(f"   PID: {proc['pid']}")
                        print(f"   Name: {proc['name']}")
                        print(f"   Full Command: {proc['cmdline']}")
                        print(f"   Working Directory: {proc['cwd']}")

                        try:
                            p = psutil.Process(proc["pid"])
                            print(f"   Status: {p.status()}")
                            print(f"   CPU %: {p.cpu_percent()}")
                            print(
                                f"   Memory: {p.memory_info().rss / 1024 / 1024:.1f} MB"
                            )
                            print(f"   Started: {p.create_time()}")
                        except psutil.NoSuchProcess:
                            print("   Status: Process no longer exists")

                    continue

                elif choice == "5":
                    print("Exiting without killing processes")
                    break

                else:
                    print("❌ Invalid choice. Please enter 1-5")
                    continue

                # Ask if user wants to continue
                if choice in ["1", "2", "3"]:
                    another = input(
                        "\nDo you want to perform another action? (y/n): "
                    ).lower()
                    if another != "y":
                        break

            except (ValueError, KeyboardInterrupt):
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue

    print("\n✅ Process check complete!")
    print("\n💡 TIPS:")
    print("- After killing processes, wait a few seconds before starting your bot")
    print("- Use Ctrl+C to stop your bot gracefully")
    print("- Only run one bot instance at a time")
    print("- Check Task Manager if processes persist")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nScript failed: {e}")
        sys.exit(1)
