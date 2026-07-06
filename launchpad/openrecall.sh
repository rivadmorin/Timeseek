#!/bin/bash
# OpenRecall Lifecycle Script (Linux Debian)
# Philosophy: Offline, Portable, 1-Click

function install() {
    echo "Installing OpenRecall..."
    python3 -m pip install .
}

function run() {
    echo "Starting OpenRecall..."
    python3 -m openrecall.app
}

function stop() {
    echo "Stopping OpenRecall..."
    pkill -f "openrecall.app"
}

function uninstall() {
    echo "Uninstalling OpenRecall..."
    python3 -m pip uninstall openrecall -y
}

case "$1" in
    install) install ;;
    run) run ;;
    stop) stop ;;
    uninstall) uninstall ;;
    *) echo "Usage: $0 {install|run|stop|uninstall}" ;;
esac
