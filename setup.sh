#!/bin/bash
export TERM=xterm-256color

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
BLUE=$(tput setaf 4)
PURPLE=$(tput setaf 5)
CYAN=$(tput setaf 6)
YELLOW=$(tput setaf 3)
BOLD=$(tput bold)
NC=$(tput sgr0)

print_loading() {
    local phrase=$1
    printf "%s%s%s" "${CYAN}${BOLD}" "$phrase" "${NC}"
    for i in {1..3}; do
        printf "%s.%s" "${YELLOW}" "${NC}"
        sleep 0.5
    done
    echo
}

print_success() {
    local text=$1
    printf "%s%s✓ %s%s\n" "${GREEN}" "${BOLD}" "$text" "${NC}"
    sleep 0.5
}

animate_progress() {
    local duration=$1
    local phrase=$2
    printf "%s%s%s " "${BLUE}" "${phrase}" "${NC}"
    local chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for (( i=0; i<duration; i++ )); do
        local char="${chars:i%10:1}"
        printf "%s%s%s" "${PURPLE}" "${char}" "${NC}"
        sleep 0.1
        printf "\b"
    done
    echo
}

print_banner() {
    echo "${CYAN}${BOLD}"
    cat << "EOF"
 ____       _        __           ____  _           
/ ___| ___ (_)_ __  / _|_ __ ___ |  _ \| |_   _ ___ 
| |  _ / _ \| | '_ \| |_| '__/ _ \| |_) | | | | / __|
| |_| | (_) | | | | |  _| | |  __/|  __/| | |_| \__ \
 \____|\___/|_|_| |_|_| |_|  \___||_|   |_|\__,_|___/
EOF
    echo "${NC}"
}

setup_goinfre_plus() {
    clear
    print_banner
    echo "${YELLOW}${BOLD}Initializing Goinfre Plus Setup...${NC}"
    echo

    print_loading "Creating Goinfre Plus directory"
    mkdir -p "$HOME/.goinfre-plus"
    print_success "Directory created at $HOME/.goinfre-plus"

    print_loading "Copying files to Goinfre Plus directory"
    cp -R ./* "$HOME/.goinfre-plus/" 2>/dev/null || true
    cd "$HOME/.goinfre-plus"
    print_success "Files copied successfully"

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
    if ! grep -q "alias goinfre=" "$HOME/.zshrc"; then
        echo 'alias goinfre="python3 ~/.goinfre-plus/start.py"' >> "$HOME/.zshrc"
    fi
    print_success "Alias added to .zshrc"

    echo
    echo "${GREEN}${BOLD}✨ Goinfre Plus setup completed successfully! ✨${NC}"
    echo "${CYAN}Please restart your terminal or run 'source ~/.zshrc' to use the 'goinfre' command.${NC}"
}

setup_goinfre_plus