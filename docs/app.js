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

  // --- Official Project Definitions ---
  // Each project has a matcher function, display info, and optional GitHub URL
  const OFFICIAL_PROJECTS = [
    {
      id: 'binance',
      name: 'Binance',
      icon: '🔶',
      github: 'https://github.com/binance/binance-skills-hub',
      matcher: (s) => s.author === 'binance' || s.name.startsWith('binance-official')
    },
    {
      id: 'okx',
      name: 'OKX',
      icon: '⚫',
      github: 'https://github.com/okx/onchainos-skills',
      matcher: (s) => s.author === 'okx' || s.name.startsWith('okx-official')
    },
    {
      id: 'gate',
      name: 'Gate.io',
      icon: '🔵',
      github: 'https://github.com/gateio',
      matcher: (s) => s.author === 'gate' && s.name.startsWith('gate-')
    },
    {
      id: 'nansen',
      name: 'Nansen',
      icon: '📊',
      github: 'https://www.nansen.ai',
      matcher: (s) => s.author === 'nansen' && s.name.startsWith('nansen-')
    },
    {
      id: 'cmc',
      name: 'CoinMarketCap',
      icon: '📈',
      github: 'https://github.com/coinmarketcap',
      matcher: (s) => s.author === 'cmc' && (s.name.startsWith('cmc-') || s.name.startsWith('coinmarketcap-'))
    },
    {
      id: 'bitget',
      name: 'Bitget',
      icon: '🟢',
      github: 'https://github.com/BitgetLimited/agent_hub',
      matcher: (s) => (s.author === 'bitget' || s.author === 'bitget-wallet-ai-lab') && s.name.startsWith('bitget-official')
    },
    {
      id: 'lightning',
      name: 'Lightning Labs',
      icon: '⚡',
      github: 'https://github.com/lightningnetwork',
      matcher: (s) => s.author === 'roasbeef' && s.name.startsWith('lightning-')
    },
    {
      id: 'opensea',
      name: 'OpenSea',
      icon: '🌊',
      github: 'https://github.com/ProjectOpenSea',
      matcher: (s) => s.author === 'opensea' && s.name.startsWith('opensea')
    },
    {
      id: 'sushiswap',
      name: 'SushiSwap',
      icon: '🍣',
      github: 'https://github.com/sushiswap',
      matcher: (s) => s.author === 'sushi' && s.name.startsWith('sushiswap')
    },
    {
      id: 'uniswap',
      name: 'Uniswap',
      icon: '🦄',
      github: 'https://github.com/Uniswap/uniswap-ai',
      matcher: (s) => s.name.startsWith('uniswap-official')
    },
    {
      id: 'solana',
      name: 'Solana Foundation',
      icon: '☀️',
      github: 'https://github.com/solana-foundation/solana-mcp-official',
      matcher: (s) => s.name === 'solana-mcp-official'
    },
    {
      id: 'bnbchain',
      name: 'BNB Chain',
      icon: '💛',
      github: 'https://github.com/bnb-chain/bnbchain-skills',
      matcher: (s) => s.name.startsWith('bnb-official') || s.name === 'bnbchain-mcp'
    },
    {
      id: 'aptos',
      name: 'Aptos',
      icon: '🔷',
      github: 'https://github.com/aptos-labs/aptos-agent',
      matcher: (s) => s.name.startsWith('aptos-official') || s.name === 'aptos-mcp'
    },
    {
      id: 'mcp-servers',
      name: 'MCP Servers',
      icon: '🔌',
      github: 'https://github.com/jiayaoqijia/cryptoskill',
      matcher: (s) => s.category === 'mcp-servers' && !s.name.startsWith('bnb') && !s.name.startsWith('aptos') && !s.name.startsWith('solana')
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

  // --- Load Skills Catalog ---
  async function loadSkills() {
    try {
      const res = await fetch('skills.json');
      const data = await res.json();
      skills = data.skills;
      categories = data.categories;
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
    const statProtocols = document.getElementById('statProtocols');
    if (statSkills) statSkills.textContent = skills.length + '+';
    if (statCategories) statCategories.textContent = Object.keys(categories).length;
    const protocols = new Set();
    skills.forEach(s => {
      if (s.tags && s.tags.length > 0) protocols.add(s.tags[0]);
    });
    if (statProtocols) statProtocols.textContent = protocols.size + '+';
  }

  // --- Render Official Projects ---
  function renderOfficialProjects() {
    if (!officialGrid) return;
    officialGrid.innerHTML = '';

    OFFICIAL_PROJECTS.forEach(project => {
      const projectSkills = officialSkills.filter(s => project.matcher(s));
      if (projectSkills.length === 0) return;

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
        <div class="official-card-bottom">
          <span class="official-skill-count"><strong>${projectSkills.length}</strong> skills</span>
          <a href="${project.github}" target="_blank" rel="noopener" class="official-github-link" onclick="event.stopPropagation()">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
          </a>
        </div>
      `;

      card.addEventListener('click', () => {
        toggleOfficialProject(project.id);
      });

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

  // --- Create Skill Card (shared between official and community) ---
  function createSkillCard(skill, isOfficial) {
    const card = document.createElement('div');
    card.className = 'skill-card fade-in-up';
    const cat = categories[skill.category];
    const badgeClass = isOfficial ? 'skill-badge official-tag' : 'skill-badge';
    const badgeText = isOfficial ? '&#10003; Official' : (cat ? cat.name : skill.category);

    card.innerHTML = `
      <div class="skill-card-header">
        <div class="skill-name">${skill.displayName}</div>
        <span class="${badgeClass}">${badgeText}</span>
      </div>
      <div class="skill-desc">${skill.description}</div>
      <div class="skill-footer">
        <div class="skill-tags">
          ${skill.tags.filter(t => t !== 'official').slice(0, 3).map(t => `<span class="skill-tag">${t}</span>`).join('')}
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

  // --- Install Tab Switching ---
  window.switchInstallTab = function (tab, btn) {
    document.querySelectorAll('.install-panel').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.install-tab').forEach(t => t.classList.remove('active'));
    const panel = document.getElementById('install-' + tab);
    if (panel) panel.style.display = 'block';
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
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
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
    loadSkills();
    observeElements();
  });

})();
