#!/usr/bin/env node

/**
 * TermForum Ultimate - Animated Splash Screen
 *
 * Matrix-style loading animation with ASCII art
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
};

// ASCII Art
const logo = `
╔═══════════════════════════════════════════════════════════════╗
║                                                                ║
║  ████████╗███████╗██████╗ ███╗   ███╗███████╗ ██████╗ ██████╗ ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝██╔═══██╗██╔══██╗║
║     ██║   █████╗  ██████╔╝██╔████╔██║█████╗  ██║   ██║██████╔╝║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██╗║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝║
║                                                                  ║
║          🔥 UNDERGROUND TERMINAL FORUM EXPERIENCE 🔥            ║
║                                                                  ║
╚═══════════════════════════════════════════════════════════════╝
`;

const matrixChars = 'ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ01';

// Helper functions
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function clearScreen() {
  process.stdout.write('\x1Bc');
}

function hideCursor() {
  process.stdout.write('\x1B[?25l');
}

function showCursor() {
  process.stdout.write('\x1B[?25h');
}

function moveCursor(x, y) {
  process.stdout.write(`\x1B[${y};${x}H`);
}

// Matrix rain effect
async function matrixRain(duration = 2000) {
  const width = process.stdout.columns;
  const height = process.stdout.rows;
  const drops = Array(width).fill(0);

  clearScreen();
  hideCursor();

  const startTime = Date.now();

  const interval = setInterval(() => {
    // Draw matrix
    for (let i = 0; i < width; i++) {
      const char = matrixChars[Math.floor(Math.random() * matrixChars.length)];
      const y = drops[i];

      if (y < height) {
        moveCursor(i + 1, y + 1);
        process.stdout.write(`${colors.green}${char}${colors.reset}`);
      }

      // Reset drop randomly
      if (y > height && Math.random() > 0.975) {
        drops[i] = 0;
      }

      drops[i]++;
    }

    if (Date.now() - startTime > duration) {
      clearInterval(interval);
      clearScreen();
      showCursor();
    }
  }, 50);

  await sleep(duration);
}

// Progress bar
async function showProgress(message, steps) {
  const width = 50;

  for (let i = 0; i <= steps; i++) {
    const progress = Math.floor((i / steps) * width);
    const bar = '█'.repeat(progress) + '░'.repeat(width - progress);
    const percent = Math.floor((i / steps) * 100);

    process.stdout.write(
      `\r${colors.cyan}${message}${colors.reset} [${colors.green}${bar}${colors.reset}] ${percent}%`
    );

    await sleep(50);
  }

  process.stdout.write('\n');
}

// Animated text
async function typeText(text, delay = 50) {
  for (const char of text) {
    process.stdout.write(char);
    await sleep(delay);
  }
  process.stdout.write('\n');
}

// Main splash sequence
async function splash() {
  try {
    // 1. Matrix rain effect
    await matrixRain(1500);

    // 2. Show logo
    clearScreen();
    console.log(colors.green + logo + colors.reset);
    await sleep(1000);

    // 3. System check
    console.log(`\n${colors.cyan}═══════════════════════════════════════════════════════${colors.reset}\n`);

    await showProgress('🔍 Scanning system', 20);
    await showProgress('🔐 Initializing PolyCrypt™', 20);
    await showProgress('🎨 Loading themes', 15);
    await showProgress('🌐 Connecting to underground', 25);
    await showProgress('🤖 Activating AI assistant', 20);

    console.log(`\n${colors.cyan}═══════════════════════════════════════════════════════${colors.reset}\n`);

    // 4. System info
    await typeText(`${colors.green}✅ All systems operational${colors.reset}`, 30);
    await typeText(`${colors.yellow}⚡ Theme: ${process.env.TERMFORUM_THEME || 'dark_hacker'}${colors.reset}`, 30);
    await typeText(`${colors.magenta}🚀 Launching TUI interface...${colors.reset}`, 30);

    await sleep(1000);

    // 5. Launch main TUI
    console.log(`\n${colors.bright}${colors.cyan}Press ENTER to continue...${colors.reset}`);

    // Wait for enter
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.setEncoding('utf8');

    return new Promise((resolve) => {
      process.stdin.once('data', () => {
        process.stdin.setRawMode(false);
        clearScreen();
        resolve();
      });
    });
  } catch (error) {
    console.error('Error in splash:', error);
    showCursor();
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  splash().then(() => {
    console.log('Launching TermForum TUI...\n');
    // Launch main TUI
    import('./index.js');
  });
}

export default splash;
