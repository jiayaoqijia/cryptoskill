/* ============================================
   CryptoSkill - App JavaScript
   ============================================ */

(function () {
  'use strict';

  // --- State ---
  let skills = [];
  let categories = {};
  let officialSkills = [];
  let communitySkills = [];
  let activeFilter = 'all';
  let activeOfficialProject = null;
  const FEATURED_COUNT = 12;
  let showingAll = false;
  let sortByScore = false;
  // Sort modes for the new <select> dropdown — replaces the boolean toggle.
  // Reads `added_at` / `last_updated` from skills.json when present, falls
  // back to score / displayName. Default is `highest_score` because most
  // existing entries don't yet have date fields populated, so a recency
  // sort would be a stable-but-arbitrary order until update-catalog.py
  // backfills `added_at` from each skill's _meta.json.
  let activeSort = 'highest_score';
  const SORT_MODES = [
    { id: 'recently_updated', label: 'Recently updated' },
    { id: 'newest_added',     label: 'Newest added' },
    { id: 'highest_score',    label: 'Highest score' },
    { id: 'least_red_flags',  label: 'Fewest red flags' },
    { id: 'alpha',            label: 'A → Z' },
  ];

  // Trust manifest data, keyed by `${category}/${skillName}` (matches the
  // path in skills/ on disk). Loaded from docs/capabilities.json so the
  // home page never blocks on per-skill YAML parsing client-side.
  let trustData = {};
  // The four negative-only filters from TRUST.md §"UI: red flags first".
  // `id` is the capability key in TRUST.auto.yaml; an entry is included
  // only when the manifest reports the field as `false`.
  const TRUST_FILTERS = [
    { id: 'can_execute_shell',          label: 'Cannot execute shell' },
    { id: 'can_move_funds',             label: 'Cannot move funds' },
    { id: 'requires_hosted_operator',   label: 'No hosted operator required' },
    { id: 'uses_remote_install_script', label: 'No remote install scripts' },
  ];
  // Capability keys we want surfaced in the modal as "red flags". Order
  // mirrors scripts/generate-pages.py:RED_FLAG_CAPS. Each entry carries a
  // plain-language hint shown under the label so non-engineers can tell
  // what the flag means in practice.
  const RED_FLAG_CAPS = [
    ['can_move_funds',             'Can move funds',              'this skill can sign and send transactions on your behalf'],
    ['requires_private_key',       'Requires private key',        'you must hand over a private key, mnemonic, or wallet config'],
    ['requires_hosted_operator',   'Requires hosted operator',    'depends on a third-party hosted service to function'],
    ['uses_remote_install_script', 'Uses remote install script',  'setup pipes a remote shell script (curl | sh class)'],
    ['mutable_remote_runtime',     'Mutable remote runtime',      'runs remote code that can change behavior without a local diff'],
    ['can_install_code',           'Can install code',            'installs software at setup time (npx, pip, brew, etc.)'],
    ['can_execute_shell',          'Can execute shell',           'runs arbitrary shell commands on your machine'],
    ['can_browse_web',             'Can browse the web',          'fetches arbitrary URLs at runtime'],
    ['can_write_files',            'Can write files',             'writes to your local filesystem'],
    ['can_spawn_subagents',        'Can spawn sub-agents',        'delegates to other skills or sub-agents'],
    ['auto_invocable',             'Auto-invocable',              'may be invoked by the agent without your explicit prompt'],
  ];
  let activeTrustFilters = new Set();

  /**
   * Compute a coarse "<N> <unit> ago" label + an absolute date + a freshness
   * tier (fresh / recent / stale / ancient). The tier drives the badge colour
   * and lets sorts/filters surface skills the bot has touched recently.
   *
   * Returns null if the input is missing or unparseable so callers can
   * suppress the pill entirely (better than a misleading "0 days ago").
   */
  function relativeAge(isoDate) {
    if (!isoDate || typeof isoDate !== 'string') return null;
    const t = Date.parse(isoDate);
    if (isNaN(t)) return null;
    const diffMs = Date.now() - t;
    if (diffMs < 0) return null; // future timestamps – ignore
    const day = 86400000;
    const days = Math.floor(diffMs / day);
    let label, tier;
    if (days <= 7)        { tier = 'fresh';   label = days <= 0 ? 'today' : days === 1 ? '1d ago' : `${days}d ago`; }
    else if (days <= 30)  { tier = 'recent';  label = `${days}d ago`; }
    else if (days <= 180) { tier = 'recent';  label = `${Math.floor(days / 30)}mo ago`; }
    else if (days <= 365) { tier = 'stale';   label = `${Math.floor(days / 30)}mo ago`; }
    else                  { tier = 'ancient'; label = `${Math.floor(days / 365)}y ago`; }
    return { label, tier, absolute: isoDate.slice(0, 10) };
  }

  // --- Official Project Definitions ---
  // Only show big names. Skills from smaller projects still get "official" tag but no card.
  const OFFICIAL_PROJECTS = [
    {
      id: 'binance',
      name: 'Binance',
      icon: '🔶',
      github: 'https://github.com/binance/binance-skills-hub',
      description: 'Spot, futures, wallet, and Web3 trading skills.',
      matcher: (s) => s.author === 'binance' || s.name.startsWith('binance-official')
    },
    {
      id: 'okx',
      name: 'OKX',
      icon: '⚫',
      github: 'https://github.com/okx/onchainos-skills',
      description: 'CEX + DEX trading, wallet, and on-chain operations.',
      matcher: (s) => s.author === 'okx' || s.name.startsWith('okx-official')
    },
    {
      id: 'kraken',
      name: 'Kraken',
      icon: '🐙',
      github: 'https://github.com/krakenfx/kraken-cli',
      description: '50 trading skills + built-in MCP server for spot, futures, and earn.',
      matcher: (s) => s.name.startsWith('kraken-official')
    },
    {
      id: 'coinbase',
      name: 'Coinbase',
      icon: '🔵',
      github: 'https://github.com/coinbase/agentic-wallet-skills',
      description: 'AgentKit, wallets, Base chain, and on-chain agent tools.',
      matcher: (s) => s.name.startsWith('coinbase-official') || s.name.startsWith('base-official')
    },
    {
      id: 'uniswap',
      name: 'Uniswap',
      icon: '🦄',
      github: 'https://github.com/Uniswap/uniswap-ai',
      description: 'Swap integration, liquidity, v4 hooks, and CCA auctions.',
      matcher: (s) => s.name.startsWith('uniswap-official')
    },
    {
      id: 'metamask',
      name: 'MetaMask',
      icon: '🦊',
      github: 'https://github.com/MetaMask/openclaw-skills',
      description: 'Smart accounts, EIP-7702 delegations, and gator CLI.',
      matcher: (s) => s.name.startsWith('metamask-official')
    },
    {
      id: 'moonpay',
      name: 'MoonPay',
      icon: '🌙',
      github: 'https://github.com/moonpay/skills',
      description: '35 skills: onramp, trading, wallets, payments, and Messari research.',
      matcher: (s) => s.name.startsWith('moonpay-official')
    },
    {
      id: 'circle',
      name: 'Circle (USDC)',
      icon: '💵',
      github: 'https://github.com/circlefin/skills',
      description: 'USDC transfers, wallets, gateway, bridging, and smart contracts.',
      matcher: (s) => s.name.startsWith('circle-official')
    },
    {
      id: 'nethermind',
      name: 'Nethermind',
      icon: '🔷',
      github: 'https://github.com/NethermindEth/defi-skills',
      description: 'Natural language to DeFi transactions across 13 protocols.',
      matcher: (s) => s.name.startsWith('nethermind-official')
    },
    {
      id: 'defillama',
      name: 'DefiLlama',
      icon: '🦙',
      github: 'https://github.com/DefiLlama/defillama-skills',
      description: 'DeFi analytics: TVL, yields, risk assessment, and market analysis.',
      matcher: (s) => s.name.startsWith('defillama-official')
    },
    {
      id: 'alchemy',
      name: 'Alchemy',
      icon: '🔮',
      github: 'https://github.com/alchemyplatform/skills',
      description: 'Multi-chain RPC, token/NFT APIs, webhooks, and rollups.',
      matcher: (s) => s.name.startsWith('alchemy-official')
    },
    {
      id: 'surf',
      name: 'Surf AI',
      icon: '<img src="surf-icon.png" width="32" height="32" style="border-radius:6px">',
      github: 'https://github.com/asksurf-ai/surf-skills',
      description: '83+ commands across 14 data domains — prices, wallets, DeFi, on-chain SQL, and more.',
      matcher: (s) => s.name.startsWith('surf-official') || s.name === 'surf'
    },
    // ── 2026-05-08 autoresearch pulse: new official project rails ──
    {
      id: 'chainlink',
      name: 'Chainlink',
      icon: '🔗',
      github: 'https://github.com/smartcontractkit/chainlink-agent-skills',
      description: 'CCIP, Data Feeds, Data Streams, VRF, ACE, and CRE — official Chainlink skills.',
      matcher: (s) => s.name.startsWith('chainlink-official')
    },
    {
      id: 'helius',
      name: 'Helius',
      icon: '☀️',
      github: 'https://github.com/helius-labs/core-ai',
      description: 'Official Helius AI tooling: Sender, DAS, LaserStream, webhooks, priority fees.',
      matcher: (s) => s.name.startsWith('helius-official')
    },
    {
      id: 'quicknode',
      name: 'QuickNode',
      icon: '⚡',
      github: 'https://github.com/quiknode-labs/blockchain-skills',
      description: 'Multi-chain RPC, indexing, and stream skills for coding agents.',
      matcher: (s) => s.name.startsWith('quicknode-official')
    },
    {
      id: 'aptos',
      name: 'Aptos',
      icon: '🅰️',
      github: 'https://github.com/aptos-labs/aptos-agent-skills',
      description: 'Move contracts, TS SDK, and dApp frontend skills from Aptos Labs.',
      matcher: (s) => s.name.startsWith('aptos-official')
    },
    {
      id: 'sendai',
      name: 'SendAI',
      icon: '🌅',
      github: 'https://github.com/sendaifun/skills',
      description: 'Solana skills marketplace — Jupiter, Helius, Drift, Marinade, Jito.',
      matcher: (s) => s.name.startsWith('sendai-official')
    },
    {
      id: 'cryptocom',
      name: 'Crypto.com',
      icon: '💎',
      github: 'https://github.com/crypto-com/crypto-agent-trading',
      description: 'Buy/sell/swap/balances via Crypto.com Exchange and App.',
      matcher: (s) => s.name.startsWith('cryptocom-official')
    },
    {
      id: 'blockscout',
      name: 'Blockscout',
      icon: '🔍',
      github: 'https://github.com/blockscout/agent-skills',
      description: 'Explorer APIs and supporting services from the canonical Blockscout team.',
      matcher: (s) => s.name.startsWith('blockscout-official')
    },
    {
      id: 'celo',
      name: 'Celo',
      icon: '🟢',
      github: 'https://github.com/celo-org/agent-skills',
      description: 'Hardhat / Foundry EVM dev on Celo, plus the official Celo MCP.',
      matcher: (s) => s.name.startsWith('celo-official')
    },
    {
      id: 'worldcoin',
      name: 'Worldcoin',
      icon: '🌐',
      github: 'https://github.com/worldcoin/agentkit',
      description: 'World ID verification — one-per-human gating for AI agents.',
      matcher: (s) => s.name.startsWith('worldcoin-official')
    },
    {
      id: 'coinpaprika',
      name: 'CoinPaprika',
      icon: '🌶️',
      github: 'https://github.com/coinpaprika/claude-marketplace',
      description: 'CoinPaprika + DexPaprika official skills/agents for free crypto market data.',
      matcher: (s) => s.name.startsWith('coinpaprika-official')
    },
    {
      id: 'mcp-servers',
      name: 'MCP Servers',
      icon: '🔌',
      github: 'https://github.com/jiayaoqijia/cryptoskill',
      description: '85+ MCP servers: Solana, Tenderly, NEAR, EigenLayer, CoinGecko, and more.',
      matcher: (s) => s.category === 'mcp-servers'
    }
  ];

  // --- DOM Elements ---
  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  const modalOverlay = document.getElementById('modalOverlay');
  const categoriesGrid = document.getElementById('categoriesGrid');
  const skillsGrid = document.getElementById('skillsGrid');
  const filterContainer = document.getElementById('filterContainer');
  const showMoreBtn = document.getElementById('showMoreBtn');
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');
  const officialGrid = document.getElementById('officialGrid');
  const officialSkillsDetail = document.getElementById('officialSkillsDetail');
  const officialSkillsList = document.getElementById('officialSkillsList');
  const officialDetailTitle = document.getElementById('officialDetailTitle');
  const officialDetailClose = document.getElementById('officialDetailClose');

  // --- Theme Toggle ---
  function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    // Load saved preference (default is dark)
    const savedTheme = localStorage.getItem('cryptoskill-theme');
    if (savedTheme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
    }

    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      if (currentTheme === 'light') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('cryptoskill-theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('cryptoskill-theme', 'light');
      }
    });
  }

  // --- Load Skills Catalog ---
  async function loadSkills() {
    try {
      // Skills catalog is required; capabilities are best-effort. Don't let
      // a missing or malformed capabilities.json break page rendering.
      const [catalogRes, capsRes] = await Promise.allSettled([
        fetch('skills.json', { cache: 'no-cache' }),
        fetch('capabilities.json', { cache: 'no-cache' }),
      ]);
      if (catalogRes.status !== 'fulfilled' || !catalogRes.value.ok) {
        throw new Error('skills.json fetch failed');
      }
      const data = await catalogRes.value.json();
      skills = data.skills;
      categories = data.categories;
      if (capsRes.status === 'fulfilled' && capsRes.value.ok) {
        try {
          const capsJson = await capsRes.value.json();
          trustData = capsJson.skills || {};
        } catch (e) {
          // Malformed capabilities.json — fall through with empty trustData
          // so the UI keeps working without flag badges.
          trustData = {};
        }
      }
      separateSkills();
      renderOfficialProjects();
      renderCategories();
      renderFilters();
      renderRecentlyAddedRail();
      renderSkills();
      updateStats();
    } catch (err) {
      console.error('Failed to load skills catalog:', err);
    }
  }

  // --- Trust manifest accessors ---
  function trustFor(skill) {
    if (!skill) return null;
    return trustData[`${skill.category}/${skill.name}`] || null;
  }
  function capValue(t, key) {
    if (!t || !t.capabilities) return undefined;
    const raw = t.capabilities[key];
    // Python emitter writes scalar; JSON shape is the raw value.
    if (raw === null || raw === undefined) return undefined;
    if (typeof raw === 'object') {
      // Per-field provenance shape: {value, confidence, source, evidence}
      // — the .value can itself be null, treat that as unknown.
      return raw.value == null ? undefined : raw.value;
    }
    return raw;
  }
  function redFlagSummary(t) {
    if (!t) return null;
    let nTrue = 0, nUnknown = 0;
    for (const [k] of RED_FLAG_CAPS) {
      const v = capValue(t, k);
      if (v === true) nTrue += 1;
      // capValue() collapses null → undefined for us; check both anyway.
      else if (v === undefined || v === null || v === 'unknown') nUnknown += 1;
    }
    return { nTrue, nUnknown };
  }
  function redFlagCount(t) {
    const s = redFlagSummary(t);
    return s === null ? null : s.nTrue;
  }
  function passesTrustFilters(skill) {
    if (activeTrustFilters.size === 0) return true;
    const t = trustFor(skill);
    if (!t) return false; // when filter is active, manifests-not-yet are excluded
    for (const id of activeTrustFilters) {
      if (capValue(t, id) !== false) return false;
    }
    return true;
  }

  // --- Separate Official and Community Skills ---
  function separateSkills() {
    const officialSet = new Set();

    // Mark skills as official based on project matchers
    skills.forEach(skill => {
      for (const project of OFFICIAL_PROJECTS) {
        if (project.matcher(skill)) {
          officialSet.add(skill.name);
          break;
        }
      }
    });

    officialSkills = skills.filter(s => officialSet.has(s.name));
    communitySkills = skills.filter(s => !officialSet.has(s.name));
  }

  // --- Check if a skill is official ---
  function isOfficialSkill(skill) {
    return officialSkills.some(s => s.name === skill.name);
  }

  // --- Get project for a skill ---
  function getProjectForSkill(skill) {
    for (const project of OFFICIAL_PROJECTS) {
      if (project.matcher(skill)) return project;
    }
    return null;
  }

  // --- Update Stats ---
  function updateStats() {
    const statSkills = document.getElementById('statSkills');
    const statCategories = document.getElementById('statCategories');
    const statMCP = document.getElementById('statMCP');
    const statProtocols = document.getElementById('statProtocols');

    if (statSkills) statSkills.textContent = skills.length + '+';
    if (statCategories) statCategories.textContent = Object.keys(categories).length;

    // Auto-calculate MCP server count
    const mcpCount = skills.filter(s => s.category === 'mcp-servers').length;
    if (statMCP) statMCP.textContent = mcpCount;

    const protocols = new Set();
    skills.forEach(s => {
      if (s.tags && s.tags.length > 0) protocols.add(s.tags[0]);
    });
    if (statProtocols) statProtocols.textContent = protocols.size + '+';

    // Update official total count header
    const officialTotalCount = document.getElementById('officialTotalCount');
    if (officialTotalCount) {
      const totalOfficialSkills = officialSkills.length;
      const verifiedTeams = OFFICIAL_PROJECTS.filter(p => officialSkills.some(s => p.matcher(s))).length;
      officialTotalCount.innerHTML = `<strong>${totalOfficialSkills}+</strong> official skills from <strong>${verifiedTeams}</strong> verified teams`;
    }
  }

  // --- Render Official Projects ---
  function renderOfficialProjects() {
    if (!officialGrid) return;
    officialGrid.innerHTML = '';

    OFFICIAL_PROJECTS.forEach(project => {
      const projectSkills = officialSkills.filter(s => project.matcher(s));
      if (projectSkills.length === 0) return;

      // Get preview skill names (up to 4)
      const previewSkills = projectSkills.slice(0, 4);
      const previewHTML = previewSkills.map(s =>
        `<span class="official-skill-preview-tag">${s.displayName}</span>`
      ).join('');

      const card = document.createElement('div');
      card.className = 'official-project-card fade-in-up';
      card.setAttribute('data-project', project.id);
      card.innerHTML = `
        <div class="official-card-top">
          <div class="official-project-icon">${project.icon}</div>
          <div class="official-project-info">
            <div class="official-project-name">${project.name}</div>
            <span class="official-badge">&#10003; Official</span>
          </div>
        </div>
        <div class="official-project-desc">${project.description || ''}</div>
        <div class="official-skill-previews">${previewHTML}</div>
        <div class="official-card-bottom">
          <span class="official-skill-count"><strong>${projectSkills.length}</strong> skills</span>
          <button class="official-view-all-btn" onclick="event.stopPropagation()">
            View all ${projectSkills.length} skills
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
          <a href="${project.github}" target="_blank" rel="noopener" class="official-github-link" onclick="event.stopPropagation()">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
          </a>
        </div>
      `;

      // Click on the card or "View all" button opens the detail
      card.addEventListener('click', () => {
        toggleOfficialProject(project.id);
      });

      const viewAllBtn = card.querySelector('.official-view-all-btn');
      if (viewAllBtn) {
        viewAllBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          toggleOfficialProject(project.id);
        });
      }

      officialGrid.appendChild(card);
    });
  }

  // --- Toggle Official Project Detail ---
  function toggleOfficialProject(projectId) {
    if (activeOfficialProject === projectId) {
      // Close detail
      activeOfficialProject = null;
      officialSkillsDetail.classList.remove('active');
      document.querySelectorAll('.official-project-card').forEach(c => c.classList.remove('active'));
      return;
    }

    activeOfficialProject = projectId;
    const project = OFFICIAL_PROJECTS.find(p => p.id === projectId);
    if (!project) return;

    const projectSkills = officialSkills.filter(s => project.matcher(s));

    // Highlight active card
    document.querySelectorAll('.official-project-card').forEach(c => {
      c.classList.toggle('active', c.getAttribute('data-project') === projectId);
    });

    // Update detail header
    officialDetailTitle.textContent = `${project.name} Skills (${projectSkills.length})`;

    // Render project skills
    officialSkillsList.innerHTML = '';
    projectSkills.forEach(skill => {
      const card = createSkillCard(skill, true);
      officialSkillsList.appendChild(card);
    });

    // Show detail panel
    officialSkillsDetail.classList.add('active');

    // Scroll to detail
    setTimeout(() => {
      officialSkillsDetail.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    // Re-observe for animations
    observeElements();
  }

  // --- Close Official Detail ---
  if (officialDetailClose) {
    officialDetailClose.addEventListener('click', () => {
      activeOfficialProject = null;
      officialSkillsDetail.classList.remove('active');
      document.querySelectorAll('.official-project-card').forEach(c => c.classList.remove('active'));
    });
  }

  // --- Score Badge Helper ---
  function getGradeClass(grade) {
    if (!grade) return '';
    // Convert 'A+' / 'B-' to 'grade-a-plus' / 'grade-b-minus' so the resulting
    // class is a valid CSS identifier. Plain '+'/'−' produce '.grade-a+' which
    // CSS parses as '.grade-a' followed by an adjacent-sibling combinator and
    // never matches.
    const slug = grade.toLowerCase().replace('+', '-plus').replace('-', '-minus');
    return 'grade-' + slug;
  }

  function renderScoreBadge(skill) {
    if (!skill.score || skill.score.total == null) return '';
    const grade = skill.score.grade || 'F';
    const total = skill.score.total;
    const gradeClass = getGradeClass(grade);
    const riskWarn = skill.score.risk_gate === 'FAIL'
      ? '<span class="risk-warn" title="Risk gate: FAIL">&#9888;</span>'
      : '';
    return `<span class="skill-score-badge ${gradeClass}">${riskWarn}${grade} ${total}</span>`;
  }

  // --- Create Skill Card (shared between official and community) ---
  // Card structure (Linear-inspired, four horizontal bands separated by
  // hairline borders; everything left-aligned; metadata in mono):
  //
  //   ┌────────────────────────────────────────┐
  //   │ ⊙ Skill name                    A grade │  ← title row
  //   │ category · @author · v1.0.0             │  ← meta row
  //   ├────────────────────────────────────────┤
  //   │ Two-line description, ellipsis-clamped  │  ← body
  //   ├────────────────────────────────────────┤
  //   │ TRUST  ⚠ flag1  ⚠ flag2  +N            │  ← trust strip
  //   ├────────────────────────────────────────┤
  //   │ tag tag tag                   Official  │  ← footer
  //   └────────────────────────────────────────┘
  function createSkillCard(skill, isOfficial) {
    const card = document.createElement('article');
    card.className = 'skill-card skill-card-v2 fade-in-up';
    // Accessibility: cards are interactive, so they need a keyboard-reachable
    // role + tabindex and Enter/Space handlers (the click listener alone
    // serves only mouse users).
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-haspopup', 'dialog');
    card.setAttribute('aria-label', `${skill.displayName}, ${skill.category}, view details`);
    const cat = categories[skill.category];
    const catIcon = cat?.icon || '&#128230;'; // 📦
    const catName = cat?.name || skill.category;
    const trust = trustFor(skill);
    const summary = redFlagSummary(trust);

    // --- Trust strip: top 3 active red flags with icons.
    let trustStrip = '';
    if (summary !== null) {
      const { nTrue, nUnknown } = summary;
      const trueCaps = RED_FLAG_CAPS
        .filter(([k]) => capValue(trust, k) === true)
        .slice(0, 3)
        .map(([, label]) => `<span class="trust-strip-flag" role="img" aria-label="${escHTML(label)}: yes" title="${escHTML(label)}: yes"><span aria-hidden="true">&#x26A0;</span> ${escHTML(label)}</span>`)
        .join('');
      const moreCount = Math.max(0, nTrue - 3);
      const moreSpan = moreCount > 0 ? `<span class="trust-strip-more" aria-label="${moreCount} more red flags">+${moreCount}</span>` : '';
      const title = `${nTrue} true, ${nUnknown} unknown of 11 capability flags`;
      if (nTrue === 0 && nUnknown === 0) {
        trustStrip = `<div class="trust-strip trust-strip--clean" role="status" aria-label="Trust: no red flags detected" title="${title}"><span class="trust-strip-label" aria-hidden="true">TRUST</span><span class="trust-strip-clean"><span aria-hidden="true">✓</span> No red flags detected</span></div>`;
      } else if (nTrue === 0 && nUnknown > 0) {
        trustStrip = `<div class="trust-strip trust-strip--unknown" role="status" aria-label="Trust: ${nUnknown} capabilities not measured yet — treat as a possible red flag" title="${title}"><span class="trust-strip-label" aria-hidden="true">TRUST</span><span class="trust-strip-unknown"><span aria-hidden="true">?</span> ${nUnknown} not measured yet</span></div>`;
      } else {
        trustStrip = `<div class="trust-strip trust-strip--some" role="status" aria-label="Trust: ${nTrue} red flag${nTrue === 1 ? '' : 's'} detected" title="${title}"><span class="trust-strip-label" aria-hidden="true">TRUST</span>${trueCaps}${moreSpan}</div>`;
      }
    }

    // --- Title row score badge.
    const grade = skill.score?.grade;
    const total = skill.score?.total;
    const gradeClass = grade ? getGradeClass(grade) : '';
    const riskWarn = skill.score?.risk_gate === 'FAIL' ? '<span aria-hidden="true">&#9888;</span> ' : '';
    const gradeAria = grade ? `Grade ${grade}${total != null ? `, ${total} of 100` : ''}` : '';
    const gradePill = grade ? `<span class="card-grade ${gradeClass}" role="img" aria-label="${gradeAria}" title="${total != null ? total + '/100' : ''}">${riskWarn}${escHTML(grade)}</span>` : '';

    const officialPill = isOfficial ? '<span class="card-official"><span aria-hidden="true">&#10003;</span> Official</span>' : '';
    const author = skill.author || 'unknown';
    const version = skill.version || '1.0.0';
    const tags = Array.isArray(skill.tags) ? skill.tags : [];
    // Copy-install line — same format as the modal & detail page; lets a
    // user grab the install command without leaving the home grid.
    const installCmd = skill.category === 'mcp-servers'
      ? `claude mcp add ${skill.name}`
      : `clawhub install ${skill.name}`;
    // Freshness pill — relative time since last update so a user scanning
    // the grid can tell stale skills apart from active ones at a glance.
    const freshness = relativeAge(skill.last_updated || skill.added_at);
    const freshnessPill = freshness
      ? `<span class="card-fresh card-fresh--${freshness.tier}" title="${escHTML(freshness.absolute)}">${escHTML(freshness.label)}</span>`
      : '';

    card.innerHTML = `
      <div class="card-title-row">
        <span class="card-icon" aria-hidden="true">${catIcon}</span>
        <span class="card-name">${escHTML(skill.displayName)}</span>
        ${gradePill}
      </div>
      <div class="card-meta-row">
        <span class="card-meta-cat">${escHTML(catName)}</span>
        <span class="card-meta-sep" aria-hidden="true">·</span>
        <span class="card-meta-author">@${escHTML(author)}</span>
        <span class="card-meta-sep" aria-hidden="true">·</span>
        <span class="card-meta-version">v${escHTML(version)}</span>
        ${freshnessPill ? '<span class="card-meta-sep" aria-hidden="true">·</span>' + freshnessPill : ''}
      </div>
      <p class="card-desc">${escHTML(skill.description || '')}</p>
      ${trustStrip}
      <div class="card-install-row">
        <code class="card-install-cmd">${escHTML(installCmd)}</code>
        <button class="card-install-copy" type="button"
                aria-label="Copy install command"
                data-cmd="${escHTML(installCmd)}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round"
               stroke-linejoin="round" aria-hidden="true">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
        </button>
      </div>
      <footer class="card-footer-row">
        <div class="card-tags">
          ${tags.filter(t => t !== 'official').slice(0, 3).map(t => `<span class="card-tag">${escHTML(t)}</span>`).join('')}
        </div>
        ${officialPill}
      </footer>
    `;
    // Copy-install button: stop the click from bubbling to the card so we
    // don't open the modal at the same time. Show "✓ Copied" on success
    // or "Press ⌘+C" on permission denial / unsupported browsers — never
    // a misleading silent success (codex AR1 finding).
    const copyBtn = card.querySelector('.card-install-copy');
    if (copyBtn) {
      const ok  = () => {
        copyBtn.classList.remove('card-install-copy--err');
        copyBtn.classList.add('card-install-copy--ok');
        setTimeout(() => copyBtn.classList.remove('card-install-copy--ok'), 1100);
      };
      const err = () => {
        copyBtn.classList.remove('card-install-copy--ok');
        copyBtn.classList.add('card-install-copy--err');
        setTimeout(() => copyBtn.classList.remove('card-install-copy--err'), 1600);
      };
      const fallbackCopy = (cmd) => {
        // Last-resort: programmatic textarea + execCommand. Safari /
        // permissions-denied / non-HTTPS contexts hit this path. We
        // surface the error microstate either way so the user knows
        // to grab the command manually.
        try {
          const ta = document.createElement('textarea');
          ta.value = cmd;
          ta.setAttribute('readonly', '');
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          const success = document.execCommand && document.execCommand('copy');
          document.body.removeChild(ta);
          if (success) ok(); else err();
        } catch (_) { err(); }
      };
      copyBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const cmd = copyBtn.getAttribute('data-cmd') || installCmd;
        if (navigator.clipboard?.writeText) {
          navigator.clipboard.writeText(cmd).then(ok, () => fallbackCopy(cmd));
        } else {
          fallbackCopy(cmd);
        }
      });
      copyBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.stopPropagation();
        }
      });
    }
    card.addEventListener('click', () => openModal(skill));
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal(skill);
      }
    });
    return card;
  }

  // --- Render Categories ---
  function renderCategories() {
    if (!categoriesGrid) return;
    categoriesGrid.innerHTML = '';
    Object.entries(categories).forEach(([key, cat]) => {
      const count = skills.filter(s => s.category === key).length;
      const card = document.createElement('div');
      card.className = 'category-card fade-in-up';
      card.setAttribute('data-category', key);
      card.innerHTML = `
        <span class="category-icon">${cat.icon}</span>
        <div class="category-name">${cat.name}</div>
        <div class="category-desc">${cat.description}</div>
        <span class="category-count">${count} skills</span>
      `;
      card.addEventListener('click', () => {
        filterByCategory(key);
        const skillsSection = document.getElementById('skills');
        if (skillsSection) {
          skillsSection.scrollIntoView({ behavior: 'smooth' });
        }
      });
      categoriesGrid.appendChild(card);
    });
  }

  // --- Render Filters ---
  function renderFilters() {
    if (!filterContainer) return;
    filterContainer.innerHTML = '';
    const allBtn = createFilterBtn('all', 'All');
    filterContainer.appendChild(allBtn);
    Object.entries(categories).forEach(([key, cat]) => {
      const btn = createFilterBtn(key, cat.name);
      filterContainer.appendChild(btn);
    });

    // Sort dropdown — replaces the binary "Sort by Score" toggle so users
    // can browse by recency / score / red flags / name. Uses DOM APIs only
    // (no innerHTML) since labels and option text are static constants.
    const sortWrap = document.createElement('label');
    sortWrap.className = 'filter-sort-wrap';
    const sortLabel = document.createElement('span');
    sortLabel.className = 'filter-sort-label';
    sortLabel.textContent = 'Sort:';
    sortWrap.appendChild(sortLabel);
    const sortSelect = document.createElement('select');
    sortSelect.className = 'filter-sort-select';
    sortSelect.setAttribute('aria-label', 'Sort skills');
    SORT_MODES.forEach(m => {
      const o = document.createElement('option');
      o.value = m.id;
      o.textContent = m.label;
      if (m.id === activeSort) o.selected = true;
      sortSelect.appendChild(o);
    });
    sortSelect.addEventListener('change', (e) => {
      activeSort = e.target.value;
      sortByScore = (activeSort === 'highest_score');
      renderSkills();
    });
    sortWrap.appendChild(sortSelect);
    filterContainer.appendChild(sortWrap);

    // Trust filter row (TRUST.md §"UI: red flags first, green checks last").
    // Negative-only — these all read "Cannot X" / "No X required". A skill
    // qualifies only when its TRUST.auto.yaml capability is explicitly false.
    let trustRow = document.getElementById('trustFilterRow');
    if (!trustRow) {
      trustRow = document.createElement('div');
      trustRow.id = 'trustFilterRow';
      trustRow.className = 'trust-filter-row';
      filterContainer.parentNode.insertBefore(trustRow, filterContainer.nextSibling);
    }
    trustRow.innerHTML = '';
    const lbl = document.createElement('span');
    lbl.className = 'trust-filter-label';
    lbl.textContent = 'Trust filters:';
    trustRow.appendChild(lbl);
    TRUST_FILTERS.forEach(f => {
      const tb = document.createElement('button');
      const isOn = activeTrustFilters.has(f.id);
      tb.className = 'filter-btn' + (isOn ? ' trust-filter-active' : '');
      tb.textContent = f.label;
      tb.title = `Show only skills whose TRUST.auto.yaml records ${f.id}: false`;
      tb.addEventListener('click', () => {
        if (activeTrustFilters.has(f.id)) activeTrustFilters.delete(f.id);
        else activeTrustFilters.add(f.id);
        tb.classList.toggle('trust-filter-active');
        renderSkills();
      });
      trustRow.appendChild(tb);
    });
  }

  function createFilterBtn(key, label) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn' + (key === activeFilter ? ' active' : '');
    btn.textContent = label;
    btn.addEventListener('click', () => filterByCategory(key));
    return btn;
  }

  function filterByCategory(category) {
    activeFilter = category;
    showingAll = false;
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.toggle('active', btn.textContent === (category === 'all' ? 'All' : categories[category]?.name));
    });
    document.querySelectorAll('.category-card').forEach(card => {
      card.style.outline = card.getAttribute('data-category') === category ? '1px solid rgba(10, 132, 255, 0.4)' : '';
    });
    renderSkills();
  }

  // --- Render "Recently added" rail above the home grid -----------------
  // Surfaces the 8 most recently added skills (any provenance — official or
  // community) so a returning visitor sees fresh content above the fold.
  // Lives in its own DOM node so the standard renderSkills() flow doesn't
  // have to know about it; a sibling element placed in front of skillsGrid.
  function renderRecentlyAddedRail() {
    if (!skillsGrid) return;
    let rail = document.getElementById('recentlyAddedRail');
    if (!rail) {
      rail = document.createElement('section');
      rail.id = 'recentlyAddedRail';
      rail.className = 'recently-added-rail';
      skillsGrid.parentNode.insertBefore(rail, skillsGrid);
    }
    rail.innerHTML = '';

    // Pick the 8 most-recent entries with a *valid*, non-future added_at.
    // Filter on parsed Date so a malformed string or a future-clocked
    // commit can't pollute the rail by sorting to the top of a localeCompare
    // on raw strings (e.g. "9999-12-31" or NaN from "garbage" would otherwise
    // win the sort even though relativeAge() suppresses the per-card pill).
    const now = Date.now();
    const dated = skills
      .filter(s => {
        if (!s || !s.added_at || typeof s.added_at !== 'string') return false;
        const t = Date.parse(s.added_at);
        return !isNaN(t) && t <= now;
      })
      .sort((a, b) => Date.parse(b.added_at) - Date.parse(a.added_at))
      .slice(0, 8);
    if (!dated.length) return;

    const header = document.createElement('header');
    header.className = 'recently-added-header';
    const h2 = document.createElement('h2');
    h2.textContent = 'Recently added';
    const sub = document.createElement('span');
    sub.className = 'recently-added-sub';
    sub.textContent = `${dated.length} of the newest skills the bot has shipped`;
    header.appendChild(h2);
    header.appendChild(sub);
    rail.appendChild(header);

    const list = document.createElement('div');
    list.className = 'recently-added-list';
    rail.appendChild(list);

    dated.forEach(skill => {
      const cat = categories[skill.category] || {};
      const item = document.createElement('a');
      item.className = 'recently-added-card';
      item.href = `skills/${encodeURIComponent(skill.category)}/${encodeURIComponent(skill.name)}.html`;
      item.setAttribute('aria-label',
        `${skill.displayName}, ${skill.category}, added ${skill.added_at}`);
      const icon = document.createElement('span');
      icon.className = 'recently-added-icon';
      icon.setAttribute('aria-hidden', 'true');
      icon.textContent = cat.icon || '📦'; // 📦
      const body = document.createElement('div');
      body.className = 'recently-added-body';
      const name = document.createElement('span');
      name.className = 'recently-added-name';
      name.textContent = skill.displayName || skill.name;
      const meta = document.createElement('span');
      meta.className = 'recently-added-meta';
      const fresh = relativeAge(skill.added_at);
      meta.textContent = `${cat.name || skill.category} · ${fresh ? fresh.label : skill.added_at}`;
      body.appendChild(name);
      body.appendChild(meta);
      item.appendChild(icon);
      item.appendChild(body);
      list.appendChild(item);
    });
  }

  // --- Render Community Skills ---
  function renderSkills() {
    if (!skillsGrid) return;
    skillsGrid.innerHTML = '';
    let filtered = activeFilter === 'all' ? [...communitySkills] : communitySkills.filter(s => s.category === activeFilter);
    if (activeTrustFilters.size > 0) {
      filtered = filtered.filter(passesTrustFilters);
    }
    if (filtered.length === 0 && activeTrustFilters.size > 0) {
      // Honest empty state: explain why and offer to clear the filters.
      const labels = Array.from(activeTrustFilters)
        .map(id => (TRUST_FILTERS.find(f => f.id === id) || {}).label || id)
        .join(', ');
      skillsGrid.innerHTML = `
        <div class="trust-empty-filters" style="grid-column:1/-1;padding:24px;border:1px dashed var(--border);border-radius:12px;background:var(--bg-secondary)">
          <p style="margin:0 0 6px;font-size:15px"><strong>No skills match every active trust filter.</strong></p>
          <p style="margin:0 0 12px;color:var(--text-secondary);font-size:14px">Active: ${labels}. A skill qualifies only when our scanner has confirmed the capability is <code>false</code>. Capabilities that are still <code>unknown</code> (the scanner couldn't make a confident call) are excluded on purpose, so red flags we haven't measured yet can't slip past the filter and look safe.</p>
          <button class="filter-btn" id="trustFilterClearBtn">Clear trust filters</button>
        </div>`;
      const clear = skillsGrid.querySelector('#trustFilterClearBtn');
      if (clear) clear.addEventListener('click', () => {
        activeTrustFilters.clear();
        document.querySelectorAll('#trustFilterRow .trust-filter-active').forEach(b => b.classList.remove('trust-filter-active'));
        renderSkills();
      });
      if (showMoreBtn) showMoreBtn.style.display = 'none';
      return;
    }
    // Sort modes — `activeSort` is the canonical state; `sortByScore` is
    // kept in sync for backwards compatibility with older bits of UI.
    const cmpScore = (a, b) => {
      const sa = (a.score && a.score.total != null) ? a.score.total : -1;
      const sb = (b.score && b.score.total != null) ? b.score.total : -1;
      return sb - sa;
    };
    const cmpRecent = (a, b) => {
      const da = (a.last_updated || a.added_at || '').localeCompare(
                 (b.last_updated || b.added_at || ''));
      return -da;
    };
    const cmpAdded = (a, b) => (b.added_at || '').localeCompare(a.added_at || '');
    const cmpAlpha = (a, b) => (a.displayName || a.name).localeCompare(
                                b.displayName || b.name);
    const cmpFlags = (a, b) => {
      const fa = redFlagCount(trustFor(a)) ?? 99;
      const fb = redFlagCount(trustFor(b)) ?? 99;
      return fa - fb;
    };
    const SORTERS = {
      recently_updated: cmpRecent,
      newest_added:     cmpAdded,
      highest_score:    cmpScore,
      least_red_flags:  cmpFlags,
      alpha:            cmpAlpha,
    };
    if (sortByScore || activeSort) {
      filtered.sort(SORTERS[activeSort] || cmpScore);
    }
    const displaySkills = showingAll ? filtered : filtered.slice(0, FEATURED_COUNT);

    displaySkills.forEach(skill => {
      const card = createSkillCard(skill, false);
      skillsGrid.appendChild(card);
    });

    if (showMoreBtn) {
      if (filtered.length > FEATURED_COUNT && !showingAll) {
        showMoreBtn.style.display = 'block';
        showMoreBtn.querySelector('button').textContent = `Show all ${filtered.length} skills`;
      } else {
        showMoreBtn.style.display = 'none';
      }
    }

    observeElements();
  }

  // --- Show More ---
  if (showMoreBtn) {
    showMoreBtn.addEventListener('click', () => {
      showingAll = true;
      renderSkills();
    });
  }

  // --- Trust panel (modal) ---
  function escHTML(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));
  }
  function renderTrustPanel(skill) {
    const t = trustFor(skill);
    // URL-encode path segments — skill.category and skill.name come from our
    // own catalog so they're trusted today, but defense-in-depth is cheap.
    const cat = encodeURIComponent(skill.category);
    const nm = encodeURIComponent(skill.name);
    const ghBlob = `https://github.com/jiayaoqijia/cryptoskill/blob/main/skills/${cat}/${nm}`;
    const ghTree = `https://github.com/jiayaoqijia/cryptoskill/tree/main/skills/${cat}/${nm}`;
    const links = `
      <p class="trust-source-links">
        <a href="${ghBlob}/SKILL.md" target="_blank" rel="noopener">SKILL.md &rarr;</a>
        <a href="${ghBlob}/SOURCE.md" target="_blank" rel="noopener">SOURCE.md &rarr;</a>
        <a href="${ghBlob}/TRUST.auto.yaml" target="_blank" rel="noopener">TRUST.auto.yaml &rarr;</a>
        <a href="${ghTree}" target="_blank" rel="noopener">Browse directory &rarr;</a>
      </p>`;
    if (!t) {
      return `
      <div class="modal-section-title">Trust Manifest</div>
      <div class="trust-panel">
        <p class="trust-empty">No trust manifest computed for this skill yet. Treat capabilities as <strong>unknown</strong> until the bot generates one.</p>
        ${links}
      </div>`;
    }
    // Group capabilities by state — same layout as the per-skill HTML
    // page (scripts/generate-pages.py:_capability_section).
    const caps = t.capabilities || {};
    const buckets = { true: [], false: [], unknown: [] };
    const ICON = { true: '&#x26A0;', false: '&#x2713;', unknown: '?' };
    const ARIA = { true: 'Yes — red flag', false: 'No — cleared', unknown: 'Not measured' };
    for (const [key, label, hint] of RED_FLAG_CAPS) {
      const raw = caps[key];
      const val  = (raw && typeof raw === 'object') ? raw.value      : raw;
      const conf = (raw && typeof raw === 'object') ? raw.confidence : null;
      const src  = (raw && typeof raw === 'object') ? raw.source     : null;
      const group = (val === true) ? 'true' : (val === false) ? 'false' : 'unknown';
      const confDot = (group !== 'unknown' && conf)
        ? `<span class="trust-cap-confidence trust-cap-confidence--${escHTML(conf)}" title="${escHTML(conf)} confidence (${escHTML(src || 'unknown')})" aria-label="${escHTML(conf)} confidence based on ${escHTML(src || 'unknown')} evidence"></span>`
        : '';
      buckets[group].push(
        `<li class="trust-cap-v2" data-state="${group}">` +
        `<span class="trust-cap-icon" aria-label="${ARIA[group]}" title="${ARIA[group]}">${ICON[group]}</span>` +
        `<div class="trust-cap-body">` +
        `<span class="trust-cap-label">${escHTML(label)}</span>` +
        `<span class="trust-cap-hint">${escHTML(hint)}</span>` +
        `</div>` +
        confDot +
        `</li>`
      );
    }
    const SECTIONS = [
      { state: 'true',    title: 'Red flags',          kicker: 'things this skill can do that affect your security or funds' },
      { state: 'false',   title: 'Cleared by scanner', kicker: 'we scanned the skill’s text & scripts and found no evidence of these' },
      { state: 'unknown', title: 'Not measured yet',   kicker: 'scanner couldn’t make a confident call — treat as a possible red flag' },
    ];
    const groupClass = { true: 'flags', false: 'clear', unknown: 'unknown' };
    const sections = SECTIONS.map(({ state, title, kicker }) => {
      const items = buckets[state];
      if (!items.length) return '';
      return `
        <section class="trust-cap-group trust-cap-group--${groupClass[state]}">
          <header class="trust-cap-group-header">
            <span class="trust-cap-group-count">${items.length}</span>
            <span class="trust-cap-group-title">${escHTML(title)}</span>
            <span class="trust-cap-group-kicker">${escHTML(kicker)}</span>
          </header>
          <ul class="trust-cap-list-v2">${items.join('')}</ul>
        </section>`;
    }).join('');
    // capabilities.json uses `hosted_operators`; per-skill TRUST.auto.yaml
    // uses `detected_hosted_operators`. Accept either.
    const operators = t.detected_hosted_operators || t.hosted_operators || [];
    const ingredients = operators.length
      ? `<h3 class="trust-subhead">Ingredients (services this skill talks to)</h3>
         <p class="trust-help">External services this skill needs in order to work. Today we only show services we recognize from a curated list of ~50 well-known hosts; a complete dependency list is on the roadmap.</p>
         <ul class="trust-ingredient-list">${operators.map(op => `<li class="trust-ingredient"><span class="trust-ingredient-kind">service</span> <code>${escHTML(op)}</code></li>`).join('')}</ul>`
      : '<h3 class="trust-subhead">Ingredients (services this skill talks to)</h3><p class="trust-empty trust-help">We did not find any well-known hosted services in this skill’s text or scripts. <strong>This does NOT mean the skill is local-only</strong> — it might use services we don’t yet recognize. A complete dependency list is on the roadmap.</p>';
    const audits = (t.audits || []);
    const auditsHTML = audits.length
      ? `<h3 class="trust-subhead">Audits</h3><ul class="trust-audit-list">${audits.map(a => {
          const r = a.reviewer || {};
          return `<li class="trust-audit"><strong>${escHTML(r.name || 'Unknown')}</strong> <span class="trust-tier trust-tier--${escHTML(r.tier || 'unverified')}">${escHTML(r.tier || 'unverified')}</span> &middot; subject <code>${escHTML(a.subject || '')}</code> &middot; ${escHTML(a.date || '')}</li>`;
        }).join('')}</ul>`
      : '<h3 class="trust-subhead">Audits</h3><p class="trust-empty trust-help"><strong>No one has audited this skill yet.</strong> That is different from "audited and clean" — it just means no professional reviewer has signed off on it. There are no audit reports to read.</p>';
    const stage = t.stage == null ? 'trust grade not computed yet' : escHTML(String(t.stage));
    const nTrue = buckets.true.length;
    const nFalse = buckets.false.length;
    const nUnknown = buckets.unknown.length;
    const quickPills = `
      <div class="trust-quick-pills">
        <span class="trust-pill trust-pill--flags">${nTrue} red flag${nTrue === 1 ? '' : 's'}</span>
        <span class="trust-pill trust-pill--clear">${nFalse} cleared</span>
        <span class="trust-pill trust-pill--unknown">${nUnknown} not measured</span>
      </div>`;
    return `
      <div class="modal-section-title">Trust profile <span class="trust-stage-pill">${stage}</span></div>
      ${quickPills}
      <p class="trust-help">Detected automatically by an open-source scanner that reads the skill’s text and scripts. <strong>Not measured</strong> means the scanner couldn’t make a confident call — it is NOT a green check, treat it as a possible red flag until a human or a stronger scanner has measured it.</p>
      <div class="trust-panel">
        ${sections}
        ${ingredients}
        ${auditsHTML}
        ${links}
      </div>`;
  }

  // --- Score Detail Rendering for Modal ---
  function renderScoreDetail(skill) {
    if (!skill.score || skill.score.total == null) return '';
    const s = skill.score;
    const grade = s.grade || 'F';
    const gradeClass = getGradeClass(grade);
    const riskClass = s.risk_gate === 'PASS' ? 'pass' : 'fail';
    const riskIcon = s.risk_gate === 'PASS' ? '&#10003;' : '&#9888;';
    const riskLabel = s.risk_gate || 'N/A';

    // Dimension max totals from the scoring schema
    const dimensionMaxes = { static: 40, security: 20, depth: 40 };

    function fillClass(pts, max) {
      const pct = max > 0 ? (pts / max) * 100 : 0;
      if (pct >= 80) return 'fill-a';
      if (pct >= 60) return 'fill-b';
      if (pct >= 40) return 'fill-c';
      if (pct >= 20) return 'fill-d';
      return 'fill-f';
    }

    const dims = ['static', 'security', 'depth'];
    const barsHTML = dims.map(dim => {
      const pts = s[dim] != null ? s[dim] : 0;
      const max = dimensionMaxes[dim] || 40;
      const pct = max > 0 ? Math.round((pts / max) * 100) : 0;
      const fc = fillClass(pts, max);
      return `
        <div class="score-dimension">
          <span class="score-dimension-label">${dim}</span>
          <div class="score-dimension-bar">
            <div class="score-dimension-fill ${fc}" style="width:${pct}%"></div>
          </div>
          <span class="score-dimension-value">${pts}/${max}</span>
        </div>`;
    }).join('');

    return `
      <div class="modal-score-section">
        <div class="modal-score-header">
          <div class="modal-score-overall">
            <span class="modal-score-number">${s.total}</span>
            <span class="modal-score-max">/ 100</span>
            <span class="modal-score-grade skill-score-badge ${gradeClass}">${grade}</span>
          </div>
          <div class="modal-risk-gate ${riskClass}">
            <span>${riskIcon}</span>
            Risk: ${riskLabel}
          </div>
        </div>
        <div class="modal-score-dimensions">
          ${barsHTML}
        </div>
      </div>`;
  }

  // --- Modal ---
  function openModal(skill) {
    const cat = categories[skill.category];
    const isOfficial = isOfficialSkill(skill);
    const project = getProjectForSkill(skill);
    const modalContent = modalOverlay.querySelector('.modal');

    const officialBadgeHTML = isOfficial
      ? `<span class="modal-official-badge">&#10003; Official</span>`
      : '';

    const projectInfoHTML = project
      ? `<span>&#183;</span><span>${project.name}</span>`
      : '';

    modalContent.innerHTML = `
      <div class="modal-header">
        <div class="modal-icon">${cat ? cat.icon : '&#128230;'}</div>
        <div>
          <div class="modal-title">${skill.displayName}</div>
          <div class="modal-meta">
            <span class="author">@${skill.author}</span>
            <span>&#183;</span>
            <span>v${skill.version}</span>
            <span>&#183;</span>
            <span>${cat ? cat.name : skill.category}</span>
            ${projectInfoHTML}
            ${officialBadgeHTML}
          </div>
        </div>
      </div>
      <div class="modal-desc">${skill.description}</div>
      <div class="modal-section-title">Tags</div>
      <div class="modal-tags">
        ${skill.tags.map(t => `<span class="modal-tag">${t}</span>`).join('')}
      </div>
      <div class="modal-section-title">Install</div>
      <div class="modal-install">
        ${skill.category === 'mcp-servers' ? `
        <div class="install-cmd" style="margin-bottom:6px">
          <span class="prompt" style="color:var(--accent)">MCP</span>
          <code>claude mcp add ${skill.name}</code>
          <button class="copy-btn" onclick="copyToClipboard('claude mcp add ${skill.name}', this)" title="Copy">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          </button>
        </div>
        <div class="install-cmd">
          <span class="prompt" style="color:var(--text-tertiary)">Git</span>
          <code>git clone ${skill.tags.find(t => t.startsWith('http')) || 'https://github.com/jiayaoqijia/cryptoskill'}</code>
          <button class="copy-btn" onclick="copyToClipboard('git clone ${skill.tags.find(t => t.startsWith('http')) || ''}', this)" title="Copy">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          </button>
        </div>
        ` : `
        <div class="install-cmd" style="margin-bottom:6px">
          <span class="prompt" style="color:var(--accent)">Claude</span>
          <code>cp -r cryptoskill/skills/${skill.category}/${skill.name} .claude/skills/</code>
          <button class="copy-btn" onclick="copyToClipboard('cp -r cryptoskill/skills/${skill.category}/${skill.name} .claude/skills/', this)" title="Copy">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          </button>
        </div>
        <div class="install-cmd">
          <span class="prompt" style="color:var(--success)">Claw</span>
          <code>clawhub install ${skill.name}</code>
          <button class="copy-btn" onclick="copyToClipboard('clawhub install ${skill.name}', this)" title="Copy">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          </button>
        </div>
        `}
      </div>
      ${renderScoreDetail(skill)}
      ${renderTrustPanel(skill)}
    `;
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  // --- Search ---
  function openSearch() {
    searchOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    setTimeout(() => searchInput.focus(), 100);
  }

  function closeSearch() {
    searchOverlay.classList.remove('active');
    document.body.style.overflow = '';
    searchInput.value = '';
    searchResults.innerHTML = '';
  }

  document.querySelectorAll('.nav-search-btn, .mobile-search-btn').forEach(btn => {
    btn.addEventListener('click', openSearch);
  });

  searchOverlay.addEventListener('click', (e) => {
    if (e.target === searchOverlay) closeSearch();
  });

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      if (searchOverlay.classList.contains('active')) {
        closeSearch();
      } else {
        openSearch();
      }
    }
    if (e.key === 'Escape') {
      if (searchOverlay.classList.contains('active')) closeSearch();
      if (modalOverlay.classList.contains('active')) closeModal();
    }
  });

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) {
      searchResults.innerHTML = '';
      return;
    }
    const results = fuzzySearch(query);
    renderSearchResults(results);
  });

  function fuzzySearch(query) {
    const terms = query.split(/\s+/);
    return skills
      .map(skill => {
        let score = 0;
        const searchable = [
          skill.name,
          skill.displayName,
          skill.description,
          skill.category,
          ...skill.tags
        ].join(' ').toLowerCase();

        terms.forEach(term => {
          if (skill.name.toLowerCase().includes(term)) score += 10;
          if (skill.displayName.toLowerCase().includes(term)) score += 8;
          if (skill.tags.some(t => t.toLowerCase().includes(term))) score += 5;
          if (skill.category.toLowerCase().includes(term)) score += 3;
          if (skill.description.toLowerCase().includes(term)) score += 1;
          if (!searchable.includes(term)) score -= 100;
        });
        return { skill, score };
      })
      .filter(r => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 12)
      .map(r => r.skill);
  }

  function renderSearchResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-empty">No skills found. Try a different search term.</div>';
      return;
    }
    searchResults.innerHTML = results.map(skill => {
      const cat = categories[skill.category];
      const isOfficial = isOfficialSkill(skill);
      const badgeHTML = isOfficial
        ? '<span class="result-badge official">Official</span>'
        : '<span class="result-badge community">Community</span>';
      return `
        <div class="search-result-item" data-skill="${skill.name}">
          <div class="result-icon">${cat ? cat.icon : '&#128230;'}</div>
          <div class="result-info">
            <div class="result-name">${skill.displayName}</div>
            <div class="result-desc">${skill.description}</div>
          </div>
          ${badgeHTML}
          <span class="result-category">${cat ? cat.name : skill.category}</span>
        </div>
      `;
    }).join('');

    searchResults.querySelectorAll('.search-result-item').forEach(item => {
      item.addEventListener('click', () => {
        const skillName = item.getAttribute('data-skill');
        const skill = skills.find(s => s.name === skillName);
        if (skill) {
          closeSearch();
          openModal(skill);
        }
      });
    });
  }

  // --- Quick Submit Form (initialized in DOMContentLoaded) ---
  function initSubmitForm() {
    const quickSubmitForm = document.getElementById('quickSubmitForm');
    if (!quickSubmitForm) return;

    quickSubmitForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const name = document.getElementById('submitName').value.trim();
      const url = document.getElementById('submitURL').value.trim();
      const category = document.getElementById('submitCategory').value;
      const desc = document.getElementById('submitDesc').value.trim();
      const email = document.getElementById('submitEmail').value.trim();

      if (!name || !url) {
        alert('Please fill in at least the skill name and GitHub URL.');
        return;
      }

      const subject = encodeURIComponent('[CryptoSkill] New Skill Submission: ' + name);
      const body = encodeURIComponent(
        'Skill Name: ' + name + '\n' +
        'GitHub URL: ' + url + '\n' +
        'Category: ' + (category || 'Not specified') + '\n' +
        'Description: ' + (desc || 'Not provided') + '\n' +
        'Submitter Email: ' + (email || 'Not provided') + '\n\n' +
        '---\nSubmitted via cryptoskill.org'
      );

      // Try mailto
      window.location.href = 'mailto:maintainers+cryptoskills@altresear.ch?subject=' + subject + '&body=' + body;

      // Show confirmation with fallback
      setTimeout(function () {
        var msg = 'Your email client should have opened with the submission details.\n\n' +
          'If it didn\'t open, please email maintainers+cryptoskills@altresear.ch directly with:\n\n' +
          'Skill: ' + name + '\nURL: ' + url + '\nCategory: ' + (category || 'N/A');
        alert(msg);
      }, 500);
    });
  }

  // --- Install Tab Switching ---
  window.switchInstallTab = function (tab, btn) {
    document.querySelectorAll('.install-panel').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.install-tab').forEach(t => t.classList.remove('active'));
    const panel = document.getElementById('install-' + tab);
    if (panel) {
      panel.style.display = 'block';
      // Re-trigger animation
      panel.style.animation = 'none';
      panel.offsetHeight; // force reflow
      panel.style.animation = '';
    }
    if (btn) btn.classList.add('active');
  };

  // --- Copy to Clipboard ---
  window.copyToClipboard = function (text, btn) {
    navigator.clipboard.writeText(text).then(() => {
      btn.classList.add('copied');
      const svg = btn.innerHTML;
      btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.innerHTML = svg;
      }, 2000);
    });
  };

  // --- Mobile Nav Toggle ---
  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  // --- Scroll Animations (IntersectionObserver) ---
  function observeElements() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px 50px 0px'
    });

    document.querySelectorAll('.fade-in-up:not(.visible), .stagger:not(.visible)').forEach(el => {
      observer.observe(el);
    });
  }

  // --- Smooth Anchor Scrolling ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
        if (navLinks) navLinks.classList.remove('open');
      }
    });
  });

  // --- Init ---
  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSubmitForm();
    loadSkills();
    observeElements();
  });

})();
