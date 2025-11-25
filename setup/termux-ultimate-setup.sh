#!/data/data/com.termux/files/usr/bin/bash

################################################################################
# TermForum Ultimate - Termux Setup Script
#
# Installs and configures:
# - ZSH + Oh-My-Zsh + Powerlevel10k
# - Terminal effects (cmatrix, pipes.sh, neofetch)
# - TStyle for theme/font switching
# - System monitoring tools (btop, glances)
# - ASCII art and animations
# - Custom TermForum branding
#
# Author: Yossi (analist0)
# Version: 1.0.0
################################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Emojis
CHECK="✅"
ROCKET="🚀"
GEAR="⚙️"
FIRE="🔥"
STAR="⭐"
LOCK="🔐"
PAINT="🎨"

# Banner
show_banner() {
    clear
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                                ║
║  ████████╗███████╗██████╗ ███╗   ███╗███████╗ ██████╗ ██████╗ ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝██╔═══██╗██╔══██╗║
║     ██║   █████╗  ██████╔╝██╔████╔██║█████╗  ██║   ██║██████╔╝║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██╗║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝║
║                                                                  ║
║             🔥 ULTIMATE TERMUX SETUP SCRIPT 🔥                  ║
║               Underground Terminal Experience                   ║
║                                                                  ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo ""
}

# Progress indicator
progress() {
    local msg="$1"
    echo -e "${BLUE}${GEAR}${NC} ${WHITE}${msg}...${NC}"
}

# Success message
success() {
    local msg="$1"
    echo -e "${GREEN}${CHECK} ${msg}${NC}"
}

# Error message
error() {
    local msg="$1"
    echo -e "${RED}❌ Error: ${msg}${NC}"
    exit 1
}

# Step header
step() {
    local num="$1"
    local msg="$2"
    echo ""
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}${ROCKET} Step ${num}: ${msg}${NC}"
    echo -e "${MAGENTA}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check if running in Termux
check_termux() {
    if [ ! -d "/data/data/com.termux" ]; then
        error "This script must be run in Termux!"
    fi
}

# Update and upgrade packages
update_system() {
    step 1 "Updating Termux packages"
    progress "Running apt update"
    apt update -y || error "Failed to update packages"

    progress "Running apt upgrade"
    apt upgrade -y || error "Failed to upgrade packages"

    success "System updated successfully"
}

# Install essential packages
install_essentials() {
    step 2 "Installing essential packages"

    local packages=(
        "git"
        "curl"
        "wget"
        "vim"
        "python"
        "nodejs"
        "ncurses-utils"
        "termux-api"
        "figlet"
        "toilet"
        "cowsay"
        "fortune"
        "lolcat"
    )

    for pkg in "${packages[@]}"; do
        progress "Installing ${pkg}"
        pkg install -y "$pkg" 2>/dev/null || echo "  ⚠️  ${pkg} already installed or unavailable"
    done

    success "Essential packages installed"
}

# Install ZSH + Oh-My-Zsh + Powerlevel10k
install_zsh() {
    step 3 "Installing ZSH + Oh-My-Zsh + Powerlevel10k"

    # Install ZSH
    if ! command -v zsh &> /dev/null; then
        progress "Installing ZSH"
        pkg install -y zsh || error "Failed to install ZSH"
    else
        success "ZSH already installed"
    fi

    # Install Oh-My-Zsh
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        progress "Installing Oh-My-Zsh"
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || error "Failed to install Oh-My-Zsh"
        success "Oh-My-Zsh installed"
    else
        success "Oh-My-Zsh already installed"
    fi

    # Install Powerlevel10k
    if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
        progress "Installing Powerlevel10k theme"
        git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
            ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k || error "Failed to install Powerlevel10k"
        success "Powerlevel10k installed"
    else
        success "Powerlevel10k already installed"
    fi

    # Update .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        progress "Configuring .zshrc"

        # Backup original
        cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%s)"

        # Set Powerlevel10k theme
        sed -i 's/ZSH_THEME=".*"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' "$HOME/.zshrc"

        # Add plugins
        sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' "$HOME/.zshrc"

        success ".zshrc configured"
    fi

    # Install useful plugins
    progress "Installing ZSH plugins"

    # zsh-autosuggestions
    if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
        git clone https://github.com/zsh-users/zsh-autosuggestions \
            ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions 2>/dev/null || true
    fi

    # zsh-syntax-highlighting
    if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" ]; then
        git clone https://github.com/zsh-users/zsh-syntax-highlighting \
            ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting 2>/dev/null || true
    fi

    success "ZSH setup complete"
}

# Install TStyle
install_tstyle() {
    step 4 "Installing TStyle (Theme & Font Manager)"

    if [ ! -d "$HOME/tstyle" ]; then
        progress "Cloning TStyle repository"
        cd "$HOME"
        git clone https://github.com/termuxprof/tstyle.git || error "Failed to clone TStyle"

        cd tstyle
        progress "Running TStyle setup"
        bash setup.sh || error "Failed to setup TStyle"

        success "TStyle installed (run 'tstyle' to use it)"
    else
        success "TStyle already installed"
    fi
}

# Install visual effects
install_effects() {
    step 5 "Installing terminal effects & animations"

    # cmatrix
    progress "Installing cmatrix"
    pkg install -y cmatrix 2>/dev/null || echo "  ⚠️  cmatrix unavailable"

    # pipes.sh
    if [ ! -d "$HOME/pipes.sh" ]; then
        progress "Installing pipes.sh"
        cd "$HOME"
        git clone https://github.com/pipeseroni/pipes.sh.git
        chmod +x pipes.sh/pipes.sh
        ln -sf "$HOME/pipes.sh/pipes.sh" "$PREFIX/bin/pipes.sh" 2>/dev/null || true
        success "pipes.sh installed"
    else
        success "pipes.sh already installed"
    fi

    # neofetch
    progress "Installing neofetch"
    pkg install -y neofetch 2>/dev/null || {
        # Fallback: install from source
        cd "$HOME"
        git clone https://github.com/dylanaraps/neofetch
        cd neofetch
        make install PREFIX="$PREFIX" || true
    }

    success "Visual effects installed"
}

# Install monitoring tools
install_monitoring() {
    step 6 "Installing system monitoring tools"

    # btop
    progress "Installing btop"
    pkg install -y btop 2>/dev/null || echo "  ⚠️  btop unavailable, trying alternative"

    # If btop fails, try bpytop
    if ! command -v btop &> /dev/null; then
        progress "Installing bpytop"
        pip install bpytop 2>/dev/null || echo "  ⚠️  bpytop unavailable"
    fi

    # glances
    progress "Installing glances"
    pip install glances 2>/dev/null || echo "  ⚠️  glances unavailable"

    success "Monitoring tools installed"
}

# Create custom neofetch config for TermForum
create_neofetch_config() {
    step 7 "Creating custom neofetch config"

    mkdir -p "$HOME/.config/neofetch"

    cat > "$HOME/.config/neofetch/config.conf" << 'NEOFETCH_EOF'
# TermForum Ultimate Neofetch Config

print_info() {
    info "╔═══════════════════════════════════════╗" title
    info "║       TERMFORUM UNDERGROUND           ║" title
    info "╚═══════════════════════════════════════╝" title
    info ""
    info "🔥 OS" distro
    info "💻 Host" model
    info "🎨 Theme" theme
    info "⚡ CPU" cpu
    info "💾 Memory" memory
    info "📦 Packages" packages
    info "🐚 Shell" shell
    info "📟 Terminal" term
    info "🎯 Uptime" uptime
    info ""
    info "🚀 Status" cols
}

# ASCII art
image_source="$HOME/.config/neofetch/termforum.txt"

# Display settings
ascii_distro="arch_small"
ascii_colors=(2 7)  # Green & White
ascii_bold="on"

# Colors
colors=(2 7 2 2 7 7)  # Matrix green theme

# Info settings
os_arch="on"
cpu_brand="on"
cpu_speed="on"
cpu_cores="logical"
memory_percent="on"
memory_unit="gib"
shell_version="on"
disk_show=('/')
disk_subtitle="dir"
uptime_shorthand="on"

# Text colors
bold="on"
underline_enabled="on"
separator=" →"

# Backend
image_backend="ascii"
NEOFETCH_EOF

    # Create custom ASCII art
    cat > "$HOME/.config/neofetch/termforum.txt" << 'ASCII_EOF'
   ███████╗ ██████╗ ██████╗ ██╗   ██╗███╗   ███╗
   ██╔════╝██╔═══██╗██╔══██╗██║   ██║████╗ ████║
   █████╗  ██║   ██║██████╔╝██║   ██║██╔████╔██║
   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██║╚██╔╝██║
   ██║     ╚██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║
   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝
ASCII_EOF

    success "Custom neofetch config created"
}

# Create welcome script
create_welcome_script() {
    step 8 "Creating TermForum welcome script"

    cat > "$HOME/.termforum_welcome.sh" << 'WELCOME_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# TermForum Welcome Animation

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Clear screen
clear

# Matrix effect (1 second)
if command -v cmatrix &> /dev/null; then
    timeout 1 cmatrix -C green -u 9 2>/dev/null || true
    clear
fi

# Show neofetch
if command -v neofetch &> /dev/null; then
    neofetch
fi

# Show fortune + cowsay (if available)
if command -v fortune &> /dev/null && command -v cowsay &> /dev/null; then
    echo ""
    fortune | cowsay -f tux | lolcat 2>/dev/null || fortune | cowsay -f tux
fi

# Welcome message
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ${CYAN}Welcome to TermForum Ultimate${GREEN}                           ║${NC}"
echo -e "${GREEN}║  ${MAGENTA}Type 'termforum' to enter the underground${GREEN}              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

WELCOME_EOF

    chmod +x "$HOME/.termforum_welcome.sh"

    # Add to .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        if ! grep -q "termforum_welcome" "$HOME/.zshrc"; then
            echo "" >> "$HOME/.zshrc"
            echo "# TermForum welcome screen" >> "$HOME/.zshrc"
            echo "bash ~/.termforum_welcome.sh" >> "$HOME/.zshrc"
        fi
    fi

    success "Welcome script created"
}

# Create useful aliases
create_aliases() {
    step 9 "Creating useful aliases"

    cat >> "$HOME/.zshrc" << 'ALIAS_EOF'

# TermForum Ultimate Aliases
alias matrix='cmatrix -C green'
alias pipes='pipes.sh'
alias neo='neofetch'
alias btop='btop --utf-force'
alias ll='ls -lah --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias termforum='cd ~/termforum && python -m termforum.main run'

# Quick theme switch
alias theme-dark='export TERMFORUM_THEME=dark_hacker'
alias theme-kali='export TERMFORUM_THEME=kali_red'
alias theme-cyber='export TERMFORUM_THEME=neon_cyber'
alias theme-light='export TERMFORUM_THEME=light_pro'

# System
alias sysinfo='neofetch && echo "" && btop'
alias ports='netstat -tuln'
alias myip='curl -s https://api.ipify.org && echo'

ALIAS_EOF

    success "Aliases created"
}

# Final setup
final_setup() {
    step 10 "Final configuration"

    # Set ZSH as default shell
    progress "Setting ZSH as default shell"
    chsh -s zsh 2>/dev/null || echo "  ⚠️  Could not set default shell automatically"

    # Create .termux directory
    mkdir -p "$HOME/.termux"

    # Success banner
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                                ║
║                  🎉 INSTALLATION COMPLETE! 🎉                  ║
║                                                                ║
║  Your Termux is now transformed into an underground terminal   ║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    echo -e "${CYAN}${STAR} What's installed:${NC}"
    echo "  • ZSH + Oh-My-Zsh + Powerlevel10k"
    echo "  • TStyle (theme & font manager)"
    echo "  • cmatrix, pipes.sh, neofetch"
    echo "  • btop/bpytop, glances"
    echo "  • Custom TermForum branding"
    echo "  • Useful aliases and tools"
    echo ""

    echo -e "${YELLOW}${ROCKET} Next steps:${NC}"
    echo "  1. Restart Termux or run: exec zsh"
    echo "  2. Configure Powerlevel10k: p10k configure"
    echo "  3. Try TStyle: tstyle"
    echo "  4. Run: termforum"
    echo ""

    echo -e "${MAGENTA}${FIRE} Useful commands:${NC}"
    echo "  • matrix      - Matrix rain effect"
    echo "  • pipes       - Animated pipes"
    echo "  • neo         - System info"
    echo "  • btop        - System monitor"
    echo "  • termforum   - Launch the forum"
    echo ""

    echo -e "${GREEN}Enjoy your underground terminal experience! 🔥${NC}"
    echo ""
}

# Main installation flow
main() {
    show_banner

    # Confirmation
    echo -e "${YELLOW}This script will install:${NC}"
    echo "  • ZSH + Oh-My-Zsh + Powerlevel10k"
    echo "  • TStyle"
    echo "  • Terminal effects (cmatrix, pipes.sh, neofetch)"
    echo "  • System monitoring (btop, glances)"
    echo "  • Custom TermForum configuration"
    echo ""
    echo -e "${YELLOW}Continue? (y/n)${NC}"
    read -r response

    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi

    # Run installation steps
    check_termux
    update_system
    install_essentials
    install_zsh
    install_tstyle
    install_effects
    install_monitoring
    create_neofetch_config
    create_welcome_script
    create_aliases
    final_setup
}

# Run main
main "$@"
