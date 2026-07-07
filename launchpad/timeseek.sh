#!/bin/bash
# Timeseek Lifecycle Script (Linux Debian)
# Philosophy: Offline, Portable, 1-Click

function check_prereqs() {
    echo "Checking prerequisites..."
    if ! command -v python3 &> /dev/null; then
        echo "Error: python3 is not installed."
        return 1
    fi
    echo "Prerequisites met."
}

function install() {
    check_prereqs || return 1
    echo "Installing Timeseek..."
    python3 -m pip install .
}

function start() {
    echo "Starting Timeseek..."
    python3 -m timeseek.app
}

function stop() {
    echo "Stopping Timeseek..."
    pkill -f "timeseek.app" || echo "Timeseek was not running."
}

function uninstall() {
    echo "Uninstalling Timeseek..."
    python3 -m pip uninstall timeseek -y
}

function show_help() {
    echo "Usage: ./timeseek.sh [command]"
    echo "Commands:"
    echo "  check-prereqs : Verify system dependencies"
    echo "  install       : Install the application"
    echo "  start         : Start the application"
    echo "  stop          : Stop the running application"
    echo "  uninstall     : Remove the application"
    echo "  help          : Show this help menu"
}

case "$1" in
    check-prereqs) check_prereqs ;;
    install)       install ;;
    start)         start ;;
    stop)          stop ;;
    uninstall)     uninstall ;;
    help|*)        show_help ;;
esac
