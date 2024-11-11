#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

print_loading() {
    local phrase=$1
    printf "${CYAN}${BOLD}$phrase${NC}"
    for i in {1..3}; do
        printf "${YELLOW}.${NC}"
        sleep 0.5
    done
    echo
}

print_success() {
    local text=$1
    printf "${GREEN}${BOLD}✓ %s${NC}\n" "$text"
    sleep 0.5
}

animate_progress() {
    local duration=$1
    local phrase=$2
    printf "${BLUE}${phrase}${NC} "
    local chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for (( i=0; i<duration; i++ )); do
        local char="${chars:i%10:1}"
        printf "${PURPLE}${char}${NC}"
        sleep 0.1
        printf "\b"
    done
    echo
}

print_banner() {
cat << "EOF"
${CYAN}
 ____       _        __           ____  _           
/ ___| ___ (_)_ __  / _|_ __ ___ |  _ \| |_   _ ___ 
| |  _ / _ \| | '_ \| |_| '__/ _ \| |_) | | | | / __|
| |_| | (_) | | | | |  _| | |  __/|  __/| | |_| \__ \
 \____|\___/|_|_| |_|_| |_|  \___||_|   |_|\__,_|___/
${NC}
EOF
}

setup_goinfre_plus() {
    clear
    print_banner
    echo "${YELLOW}${BOLD}Initializing Goinfre Plus Setup...${NC}"
    echo

    print_loading "Creating Goinfre Plus directory"
    mkdir -p "$HOME/.goinfre-plus"
    print_success "Directory created at $HOME/.goinfre-plus"

    print_loading "Moving files to Goinfre Plus directory"
    mv * "$HOME/.goinfre-plus/" 2>/dev/null || true
    cd "$HOME/.goinfre-plus"
    print_success "Files moved successfully"

    animate_progress 20 "Creating Python virtual environment"
    python3 -m venv env
    print_success "Virtual environment created"

    animate_progress 15 "Activating virtual environment"
    source env/bin/activate
    print_success "Virtual environment activated"

    animate_progress 30 "Installing Django"
    python3 -m pip install django
    print_success "Django installed successfully"

    deactivate
    print_success "Virtual environment deactivated"

    print_loading "Setting up Goinfre Plus command"
    echo 'alias goinfre="python3 ~/.goinfre-plus/start.py"' >> "$HOME/.zshrc"
    print_success "Alias added to .zshrc"

    echo
    echo "${GREEN}${BOLD}✨ Goinfre Plus setup completed successfully! ✨${NC}"
    echo "${CYAN}Please restart your terminal or run 'source ~/.zshrc' to use the 'goinfre' command.${NC}"
}

setup_goinfre_plus