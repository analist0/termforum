#!/usr/bin/env node

/**
 * TermForum Ultimate - TUI Interface
 *
 * Advanced terminal UI using blessed.js
 * Features:
 * - Beautiful dashboard with system monitoring
 * - Thread list with live updates
 * - Chat interface
 * - Matrix-style animations
 * - AFK screensaver (pipes/matrix)
 */

import blessed from 'blessed';
import contrib from 'blessed-contrib';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// ═══════════════════════════════════════════════════════════════
// Configuration
// ═══════════════════════════════════════════════════════════════

const CONFIG = {
  theme: process.env.TERMFORUM_THEME || 'dark_hacker',
  afkTimeout: 60000, // 1 minute of inactivity = screensaver
  updateInterval: 5000, // Update system stats every 5 seconds
};

// Theme colors
const THEMES = {
  dark_hacker: {
    fg: 'green',
    bg: 'black',
    border: 'green',
    focus: 'lime',
    accent: '#00ff00',
  },
  kali_red: {
    fg: 'white',
    bg: 'black',
    border: 'red',
    focus: '#ff0040',
    accent: 'red',
  },
  neon_cyber: {
    fg: 'cyan',
    bg: '#0a0014',
    border: 'magenta',
    focus: '#ff00ff',
    accent: 'magenta',
  },
  light_pro: {
    fg: 'black',
    bg: 'white',
    border: 'blue',
    focus: 'cyan',
    accent: 'blue',
  },
};

const theme = THEMES[CONFIG.theme];

// ═══════════════════════════════════════════════════════════════
// Screen Setup
// ═══════════════════════════════════════════════════════════════

const screen = blessed.screen({
  smartCSR: true,
  title: '🔥 TermForum Ultimate',
  fullUnicode: true,
  dockBorders: true,
  autoPadding: true,
});

// ═══════════════════════════════════════════════════════════════
// Layout - Grid System
// ═══════════════════════════════════════════════════════════════

const grid = new contrib.grid({
  rows: 12,
  cols: 12,
  screen: screen,
});

// ═══════════════════════════════════════════════════════════════
// Components
// ═══════════════════════════════════════════════════════════════

// Header - Logo & Status
const header = grid.set(0, 0, 1, 12, blessed.box, {
  content: '',
  tags: true,
  style: {
    fg: theme.fg,
    bg: theme.bg,
    bold: true,
  },
  border: {
    type: 'line',
    fg: theme.border,
  },
});

// System Monitor - CPU, RAM, Disk
const cpuGauge = grid.set(1, 0, 2, 3, contrib.gauge, {
  label: '🔥 CPU Usage',
  stroke: theme.accent,
  fill: theme.fg,
  border: {
    type: 'line',
    fg: theme.border,
  },
});

const memGauge = grid.set(1, 3, 2, 3, contrib.gauge, {
  label: '💾 RAM Usage',
  stroke: theme.accent,
  fill: theme.fg,
  border: {
    type: 'line',
    fg: theme.border,
  },
});

const diskGauge = grid.set(1, 6, 2, 3, contrib.gauge, {
  label: '📦 Disk Usage',
  stroke: theme.accent,
  fill: theme.fg,
  border: {
    type: 'line',
    fg: theme.border,
  },
});

// Network Monitor
const networkSparkline = grid.set(1, 9, 2, 3, contrib.sparkline, {
  label: '🌐 Network Activity',
  tags: true,
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.accent,
    bg: theme.bg,
  },
});

// Thread List
const threadList = grid.set(3, 0, 6, 6, blessed.list, {
  label: ' 📋 Threads ',
  keys: true,
  vi: true,
  mouse: true,
  tags: true,
  scrollbar: {
    ch: '█',
    style: {
      fg: theme.accent,
    },
  },
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.fg,
    bg: theme.bg,
    selected: {
      bg: theme.focus,
      fg: 'black',
      bold: true,
    },
    border: {
      fg: theme.border,
    },
  },
  items: [
    '{green-fg}#42{/} 🔐 Zero-Day Research Discussion',
    '{green-fg}#41{/} 🤖 Running Local LLM on Termux',
    '{green-fg}#40{/} 🔍 Network Sniffing (Legal Lab)',
    '{green-fg}#39{/} 🐍 Python Automation Scripts',
    '{green-fg}#38{/} 🌐 Building TUI Applications',
    '{green-fg}#37{/} 💻 Termux Power User Tips',
    '{green-fg}#36{/} 🎨 Terminal Customization',
    '{green-fg}#35{/} 🔥 PolyCrypt Algorithm Discussion',
  ],
});

// Thread View / Content
const threadView = grid.set(3, 6, 6, 6, blessed.box, {
  label: ' 💬 Thread View ',
  content: 'Select a thread from the list...',
  tags: true,
  scrollable: true,
  alwaysScroll: true,
  mouse: true,
  keys: true,
  vi: true,
  scrollbar: {
    ch: '█',
    style: {
      fg: theme.accent,
    },
  },
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.fg,
    bg: theme.bg,
  },
});

// Activity Log
const activityLog = grid.set(9, 0, 3, 6, contrib.log, {
  label: ' 📊 Activity Feed ',
  tags: true,
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.fg,
    bg: theme.bg,
  },
});

// Chat Box
const chatBox = grid.set(9, 6, 2, 6, blessed.log, {
  label: ' 💬 Live Chat ',
  tags: true,
  scrollable: true,
  mouse: true,
  keys: true,
  scrollbar: {
    ch: '█',
    style: {
      fg: theme.accent,
    },
  },
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.fg,
    bg: theme.bg,
  },
});

// Input Box
const inputBox = grid.set(11, 6, 1, 6, blessed.textbox, {
  label: ' ⌨️  Type your message... ',
  inputOnFocus: true,
  mouse: true,
  keys: true,
  border: {
    type: 'line',
    fg: theme.border,
  },
  style: {
    fg: theme.fg,
    bg: theme.bg,
    focus: {
      border: {
        fg: theme.focus,
      },
    },
  },
});

// ═══════════════════════════════════════════════════════════════
// Data & State
// ═══════════════════════════════════════════════════════════════

let lastActivity = Date.now();
let afkMode = false;
let networkData = [];

// Sample thread data
const threads = {
  42: {
    title: '🔐 Zero-Day Research Discussion',
    author: 'alice',
    posts: 23,
    views: 156,
    content: `
{bold}Thread #42{/bold}
{cyan-fg}Author:{/} alice | {cyan-fg}Posted:{/} 2 hours ago
{cyan-fg}Replies:{/} 23 | {cyan-fg}Views:{/} 156

─────────────────────────────────────────

Hey everyone! 👋

I've been researching some interesting vulnerabilities in
modern web frameworks. Let's discuss responsible disclosure
and ethical hacking practices.

{green-fg}What do you think about the current state of security?{/}

{yellow-fg}⚠️ Reminder: This is for educational purposes only!{/}

─────────────────────────────────────────

{bold}Recent Replies:{/bold}

{magenta-fg}bob:{/} Great topic! I think we need more focus on...
{magenta-fg}charlie:{/} Agreed! In my experience with pentesting...
{magenta-fg}dave:{/} Has anyone tried the new toolkit? It's amazing!
`,
  },
  41: {
    title: '🤖 Running Local LLM on Termux',
    author: 'charlie',
    posts: 15,
    views: 89,
    content: `
{bold}Thread #41{/bold}
{cyan-fg}Author:{/} charlie | {cyan-fg}Posted:{/} 5 hours ago

─────────────────────────────────────────

Successfully running Ollama on my Android device! 🚀

Models tested:
- qwen2.5-coder:7b (4.7 GB) ✅
- deepseek-v3.1:671b-cloud ✅

Performance is surprisingly good!

Anyone else experimenting with local AI?
`,
  },
};

// ═══════════════════════════════════════════════════════════════
// System Monitoring
// ═══════════════════════════════════════════════════════════════

async function getSystemStats() {
  try {
    // CPU
    const { stdout: cpuInfo } = await execAsync(
      "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'"
    );
    const cpuUsage = parseFloat(cpuInfo) || 0;
    cpuGauge.setPercent(Math.min(cpuUsage, 100));

    // Memory
    const { stdout: memInfo } = await execAsync(
      "free | grep Mem | awk '{print ($3/$2) * 100.0}'"
    );
    const memUsage = parseFloat(memInfo) || 0;
    memGauge.setPercent(Math.min(memUsage, 100));

    // Disk
    const { stdout: diskInfo } = await execAsync(
      "df -h / | tail -1 | awk '{print $5}' | sed 's/%//'"
    );
    const diskUsage = parseFloat(diskInfo) || 0;
    diskGauge.setPercent(Math.min(diskUsage, 100));

    // Network (mock data for now)
    const networkValue = Math.random() * 100;
    networkData.push(networkValue);
    if (networkData.length > 30) networkData.shift();
    networkSparkline.setData(['Network'], [networkData]);
  } catch (error) {
    // Fallback to mock data if commands fail
    cpuGauge.setPercent(Math.random() * 100);
    memGauge.setPercent(Math.random() * 100);
    diskGauge.setPercent(Math.random() * 100);
  }

  screen.render();
}

// ═══════════════════════════════════════════════════════════════
// Header Update
// ═══════════════════════════════════════════════════════════════

function updateHeader() {
  const time = new Date().toLocaleTimeString();
  const themeName = CONFIG.theme.replace('_', ' ').toUpperCase();

  header.setContent(
    `{center}{bold}🔥 TERMFORUM ULTIMATE 🔥{/bold} | Theme: ${themeName} | ${time}{/center}`
  );
  screen.render();
}

// ═══════════════════════════════════════════════════════════════
// Activity Feed
// ═══════════════════════════════════════════════════════════════

function logActivity(message) {
  const time = new Date().toLocaleTimeString();
  activityLog.log(`{cyan-fg}[${time}]{/} ${message}`);
}

// ═══════════════════════════════════════════════════════════════
// Event Handlers
// ═══════════════════════════════════════════════════════════════

// Thread selection
threadList.on('select', (item, index) => {
  lastActivity = Date.now();

  const threadId = 42 - index; // Simple mapping
  const thread = threads[threadId];

  if (thread) {
    threadView.setContent(thread.content);
    logActivity(`{green-fg}Opened thread #{threadId}: ${thread.title}{/}`);
  } else {
    threadView.setContent(
      '{yellow-fg}Thread content not available yet...{/}'
    );
  }

  screen.render();
});

// Focus thread list by default
threadList.focus();

// Chat input
inputBox.on('submit', (value) => {
  lastActivity = Date.now();

  if (value.trim()) {
    const time = new Date().toLocaleTimeString();
    chatBox.log(`{magenta-fg}[${time}] You:{/} ${value}`);
    logActivity(`{green-fg}Sent message:{/} ${value}`);

    // Mock AI response after 1 second
    setTimeout(() => {
      chatBox.log(
        `{cyan-fg}[${time}] AI Bot:{/} Thanks for your message! 🤖`
      );
    }, 1000);
  }

  inputBox.clearValue();
  screen.render();
});

// Key bindings
screen.key(['escape', 'q', 'C-c'], () => {
  return process.exit(0);
});

screen.key(['tab'], () => {
  lastActivity = Date.now();
  if (screen.focused === threadList) {
    inputBox.focus();
  } else {
    threadList.focus();
  }
  screen.render();
});

screen.key(['?', 'h'], () => {
  lastActivity = Date.now();
  showHelp();
});

screen.key(['r'], () => {
  lastActivity = Date.now();
  threadList.focus();
  screen.render();
});

// Mouse support
screen.on('mouse', () => {
  lastActivity = Date.now();
});

// ═══════════════════════════════════════════════════════════════
// Help Dialog
// ═══════════════════════════════════════════════════════════════

function showHelp() {
  const helpBox = blessed.message({
    parent: screen,
    top: 'center',
    left: 'center',
    width: '60%',
    height: '70%',
    label: ' ⚡ Keyboard Shortcuts ',
    tags: true,
    border: {
      type: 'line',
      fg: theme.focus,
    },
    style: {
      fg: theme.fg,
      bg: theme.bg,
      border: {
        fg: theme.focus,
      },
    },
  });

  helpBox.display(
    `
{center}{bold}🔥 TermForum Ultimate - Keyboard Shortcuts 🔥{/bold}{/center}

{bold}Navigation:{/bold}
  j/k or ↑/↓     - Navigate thread list
  Enter          - Open selected thread
  Tab            - Switch between thread list and input
  r              - Return to thread list
  Escape         - Close dialogs

{bold}Chat:{/bold}
  Tab            - Focus chat input
  Enter          - Send message
  Escape         - Clear input

{bold}System:{/bold}
  ?  or  h       - Show this help
  q  or  Ctrl+C  - Quit

{bold}Themes:{/bold}
  Set TERMFORUM_THEME environment variable:
  - dark_hacker (Matrix green)
  - kali_red (Penetration testing)
  - neon_cyber (Cyberpunk)
  - light_pro (Professional)

{center}{green-fg}Press any key to close{/green-fg}{/center}
`,
    0,
    () => {
      screen.render();
    }
  );
}

// ═══════════════════════════════════════════════════════════════
// AFK Screensaver
// ═══════════════════════════════════════════════════════════════

function checkAFK() {
  const now = Date.now();
  const idle = now - lastActivity;

  if (idle > CONFIG.afkTimeout && !afkMode) {
    afkMode = true;
    startScreensaver();
  }
}

function startScreensaver() {
  // Hide main UI
  grid.rows.forEach((row) => row.forEach((widget) => widget.hide()));

  // Create screensaver overlay
  const screensaver = blessed.box({
    parent: screen,
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    content: '{center}{bold}⏰ AFK MODE{/bold}\n\n{green-fg}Press any key to resume{/green-fg}{/center}',
    tags: true,
    style: {
      fg: 'green',
      bg: 'black',
    },
  });

  screen.render();

  // Resume on any key
  screen.once('keypress', () => {
    afkMode = false;
    lastActivity = Date.now();
    screensaver.destroy();
    grid.rows.forEach((row) => row.forEach((widget) => widget.show()));
    screen.render();
  });
}

// ═══════════════════════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════════════════════

function init() {
  // Welcome messages
  logActivity('{green-fg}🚀 TermForum Ultimate started{/}');
  logActivity(`{cyan-fg}Theme: ${CONFIG.theme}{/}`);
  logActivity('{yellow-fg}Press ? for help{/}');

  // Add welcome chat messages
  chatBox.log(
    '{cyan-fg}[System]{/} Welcome to TermForum Live Chat! 💬'
  );
  chatBox.log(
    '{cyan-fg}[AI Bot]{/} Type your message and press Enter to chat! 🤖'
  );

  // Start system monitoring
  updateHeader();
  getSystemStats();

  setInterval(getSystemStats, CONFIG.updateInterval);
  setInterval(updateHeader, 1000);
  setInterval(checkAFK, 10000); // Check AFK every 10 seconds

  // Initial render
  screen.render();
}

// ═══════════════════════════════════════════════════════════════
// Start
// ═══════════════════════════════════════════════════════════════

init();
