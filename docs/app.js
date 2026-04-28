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
  // mirrors scripts/generate-pages.py:RED_FLAG_CAPS.
  const RED_FLAG_CAPS = [
    ['can_move_funds',             'Can move funds'],
    ['requires_private_key',       'Requires private key'],
    ['requires_hosted_operator',   'Requires hosted operator'],
    ['uses_remote_install_script', 'Uses remote install script'],
    ['mutable_remote_runtime',     'Mutable remote runtime'],
    ['can_install_code',           'Can install code'],
    ['can_execute_shell',          'Can execute shell'],
    ['can_browse_web',             'Can browse the web'],
    ['can_write_files',            'Can write files'],
    ['can_spawn_subagents',        'Can spawn sub-agents'],
    ['auto_invocable',             'Auto-invocable'],
  ];
  let activeTrustFilters = new Set();

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
    return 'grade-' + grade.toLowerCase();
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
  function createSkillCard(skill, isOfficial) {
    const card = document.createElement('div');
    card.className = 'skill-card fade-in-up';
    const cat = categories[skill.category];
    const badgeClass = isOfficial ? 'skill-badge official-tag' : 'skill-badge';
    const badgeText = isOfficial ? '&#10003; Official' : (cat ? cat.name : skill.category);

    // Note: skill data comes from our own skills.json catalog, not user input
    const summary = redFlagSummary(trustFor(skill));
    let flagBadge = '';
    if (summary !== null) {
      const { nTrue, nUnknown } = summary;
      const title = `${nTrue} true, ${nUnknown} unknown of 11 capability flags`;
      if (nTrue === 0 && nUnknown === 0) {
        flagBadge = `<span class="skill-badge trust-flag-badge trust-flag-zero" title="${title}">0 known flags</span>`;
      } else if (nTrue === 0 && nUnknown > 0) {
        flagBadge = `<span class="skill-badge trust-flag-badge trust-flag-mostly-unknown" title="${title}">0 known &middot; ${nUnknown} unknown</span>`;
      } else {
        const plural = nTrue === 1 ? '' : 's';
        flagBadge = `<span class="skill-badge trust-flag-badge trust-flag-some" title="${title}">${nTrue} flag${plural}</span>`;
      }
    }
    card.innerHTML = `
      ${renderScoreBadge(skill)}
      <div class="skill-card-header">
        <div class="skill-name">${skill.displayName}</div>
        <span class="${badgeClass}">${badgeText}</span>
      </div>
      <div class="skill-desc">${skill.description}</div>
      <div class="skill-footer">
        <div class="skill-tags">
          ${skill.tags.filter(t => t !== 'official').slice(0, 3).map(t => `<span class="skill-tag">${t}</span>`).join('')}
          ${flagBadge}
        </div>
        <span class="skill-version">v${skill.version}</span>
      </div>
    `;
    card.addEventListener('click', () => openModal(skill));
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

    // Add sort-by-score toggle
    const sortBtn = document.createElement('button');
    sortBtn.className = 'filter-btn' + (sortByScore ? ' sort-active' : '');
    sortBtn.textContent = 'Sort by Score';
    sortBtn.title = 'Sort skills by quality score (highest first)';
    sortBtn.addEventListener('click', () => {
      sortByScore = !sortByScore;
      sortBtn.classList.toggle('sort-active', sortByScore);
      renderSkills();
    });
    filterContainer.appendChild(sortBtn);

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
    if (sortByScore) {
      filtered.sort((a, b) => {
        const sa = (a.score && a.score.total != null) ? a.score.total : -1;
        const sb = (b.score && b.score.total != null) ? b.score.total : -1;
        return sb - sa;
      });
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
    const caps = t.capabilities || {};
    const rows = RED_FLAG_CAPS.map(([key, label]) => {
      const raw = caps[key];
      const val = (raw && typeof raw === 'object') ? raw.value : raw;
      const conf = (raw && typeof raw === 'object') ? raw.confidence : null;
      const src = (raw && typeof raw === 'object') ? raw.source : null;
      let cls, icon, suffix = '';
      if (val === true) { cls = 'trust-cap--true'; icon = '&#x26A0;'; }
      else if (val === false) { cls = 'trust-cap--false'; icon = '&#x2713;'; }
      else { cls = 'trust-cap--unknown'; icon = '&#x25CB;'; suffix = " <span class='trust-unknown-note'>not yet measured</span>"; }
      // Surface confidence on every asserted (true OR false) value so users
      // can tell "high-confidence false" apart from "low-confidence false".
      const showConf = (val === true || val === false) && conf;
      const confSpan = showConf ? ` <span class='trust-conf trust-conf--${escHTML(conf)}'>${escHTML(conf)}</span>` : '';
      const srcSpan = (src && src !== 'unknown') ? ` <span class='trust-src'>${escHTML(src)}</span>` : '';
      return `<li class="trust-cap ${cls}"><span class="trust-icon" aria-hidden="true">${icon}</span> <span class="trust-cap-label">${escHTML(label)}</span>${suffix}${confSpan}${srcSpan}</li>`;
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
    const summary = redFlagSummary(t);
    let flagBadge = '';
    let flagsLabel = 'capabilities not yet extracted';
    if (summary !== null) {
      const { nTrue, nUnknown } = summary;
      const title = `${nTrue} true, ${nUnknown} unknown of 11 capability flags`;
      if (nTrue === 0 && nUnknown === 0) {
        flagBadge = ` <span class="skill-badge trust-flag-badge trust-flag-zero" title="${title}">0 known flags</span>`;
        flagsLabel = '0 known capability flags';
      } else if (nTrue === 0 && nUnknown > 0) {
        flagBadge = ` <span class="skill-badge trust-flag-badge trust-flag-mostly-unknown" title="${title}">0 known &middot; ${nUnknown} unknown</span>`;
        flagsLabel = `0 known &middot; ${nUnknown} unknown`;
      } else {
        const plural = nTrue === 1 ? '' : 's';
        flagBadge = ` <span class="skill-badge trust-flag-badge trust-flag-some" title="${title}">${nTrue} flag${plural}</span>`;
        flagsLabel = `${nTrue} capability flag${plural}`;
      }
    }
    return `
      <div class="modal-section-title">Trust profile <span class="trust-stage-pill">${stage}</span>${flagBadge}</div>
      <p class="trust-help"><strong>${flagsLabel}.</strong> Detected automatically by an open-source scanner; <code>unknown</code> means the scanner couldn't make a confident call — treat it as a possible red flag, not a green check.</p>
      <div class="trust-panel">
        <h3 class="trust-subhead">Capabilities</h3>
        <ul class="trust-cap-list">${rows}</ul>
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
