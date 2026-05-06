/* ============================================
   CryptoSkill - Static Pages App
   ============================================ */

(function () {
  'use strict';

  const pageMode = document.body?.dataset?.page || 'home';
  const rootPrefix = document.body?.dataset?.rootPrefix || '';
  const PAGE_SIZE = 48;
  const FEATURED_COUNT = 12;

  let skills = [];
  let categories = {};
  let officialSkills = [];
  let trustData = {};
  let homeOfficialProjects = [];
  let activeOfficialProject = null;

  const TRUST_FILTERS = [
    { id: 'can_execute_shell', label: 'Cannot execute shell' },
    { id: 'can_move_funds', label: 'Cannot move funds' },
    { id: 'requires_hosted_operator', label: 'No hosted operator required' },
    { id: 'uses_remote_install_script', label: 'No remote install scripts' },
  ];

  const RED_FLAG_CAPS = [
    ['can_move_funds', 'Can move funds', 'this skill can sign and send transactions on your behalf'],
    ['requires_private_key', 'Requires private key', 'you must hand over a private key, mnemonic, or wallet config'],
    ['requires_hosted_operator', 'Requires hosted operator', 'depends on a third-party hosted service to function'],
    ['uses_remote_install_script', 'Uses remote install script', 'setup pipes a remote shell script (curl | sh class)'],
    ['mutable_remote_runtime', 'Mutable remote runtime', 'runs remote code that can change behavior without a local diff'],
    ['can_install_code', 'Can install code', 'installs software at setup time (npx, pip, brew, etc.)'],
    ['can_execute_shell', 'Can execute shell', 'runs arbitrary shell commands on your machine'],
    ['can_browse_web', 'Can browse the web', 'fetches arbitrary URLs at runtime'],
    ['can_write_files', 'Can write files', 'writes to your local filesystem'],
    ['can_spawn_subagents', 'Can spawn sub-agents', 'delegates to other skills or sub-agents'],
    ['auto_invocable', 'Auto-invocable', 'may be invoked by the agent without your explicit prompt'],
  ];

  const CATEGORY_DEFAULTS = {
    exchanges: { name: 'Exchanges', icon: '&#127974;', description: 'CEX & DEX integrations' },
    chains: { name: 'Chains', icon: '&#9939;', description: 'Blockchain protocols' },
    defi: { name: 'DeFi', icon: '&#127959;', description: 'DeFi protocols & tools' },
    wallets: { name: 'Wallets', icon: '&#128091;', description: 'Wallet integrations' },
    analytics: { name: 'Analytics', icon: '&#128202;', description: 'Data & analytics platforms' },
    'dev-tools': { name: 'Dev Tools', icon: '&#128295;', description: 'Developer tools & SDKs' },
    trading: { name: 'Trading', icon: '&#128200;', description: 'Trading bots & strategies' },
    'prediction-markets': { name: 'Prediction Markets', icon: '&#127919;', description: 'Prediction market protocols' },
    payments: { name: 'Payments', icon: '&#128179;', description: 'Crypto payment protocols' },
    social: { name: 'Social', icon: '&#128172;', description: 'Decentralized social protocols' },
    'ai-crypto': { name: 'AI x Crypto', icon: '&#129302;', description: 'AI-powered crypto tools' },
    identity: { name: 'Identity', icon: '&#129529;', description: 'On-chain identity & reputation' },
    'mcp-servers': { name: 'MCP Servers', icon: '&#128268;', description: 'Official MCP protocol servers' },
    dex: { name: 'DEX', icon: '&#128257;', description: 'Decentralized exchange integrations' },
  };

  const OFFICIAL_PROJECTS = [
    { id: 'binance', name: 'Binance', matcher: s => s.author === 'binance' || s.name.startsWith('binance-official') },
    { id: 'okx', name: 'OKX', matcher: s => s.author === 'okx' || s.name.startsWith('okx-official') },
    { id: 'kraken', name: 'Kraken', matcher: s => s.name.startsWith('kraken-official') },
    { id: 'coinbase', name: 'Coinbase', matcher: s => s.name.startsWith('coinbase-official') || s.name.startsWith('base-official') },
    { id: 'uniswap', name: 'Uniswap', matcher: s => s.name.startsWith('uniswap-official') },
    { id: 'metamask', name: 'MetaMask', matcher: s => s.name.startsWith('metamask-official') },
    { id: 'moonpay', name: 'MoonPay', matcher: s => s.name.startsWith('moonpay-official') },
    { id: 'circle', name: 'Circle (USDC)', matcher: s => s.name.startsWith('circle-official') },
    { id: 'nethermind', name: 'Nethermind', matcher: s => s.name.startsWith('nethermind-official') },
    { id: 'defillama', name: 'DefiLlama', matcher: s => s.name.startsWith('defillama-official') },
    { id: 'alchemy', name: 'Alchemy', matcher: s => s.name.startsWith('alchemy-official') },
    { id: 'surf', name: 'Surf AI', matcher: s => s.name.startsWith('surf-official') || s.name === 'surf' },
    { id: 'mcp-servers', name: 'MCP Servers', matcher: s => s.category === 'mcp-servers' },
  ];

  const directoryState = {
    q: '',
    category: 'all',
    sort: 'score_desc',
    trust: new Set(),
    page: 1,
  };

  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  const categoriesGrid = document.getElementById('categoriesGrid');
  const skillsGrid = document.getElementById('skillsGrid');
  const filterContainer = document.getElementById('filterContainer');
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');
  const officialGrid = document.getElementById('officialGrid');
  const officialSkillsDetail = document.getElementById('officialSkillsDetail');
  const officialSkillsList = document.getElementById('officialSkillsList');
  const officialDetailTitle = document.getElementById('officialDetailTitle');
  const officialDetailClose = document.getElementById('officialDetailClose');
  const directorySearch = document.getElementById('directorySearch');
  const directorySort = document.getElementById('directorySort');
  const directoryResultSummary = document.getElementById('directoryResultSummary');
  const paginationPrev = document.getElementById('paginationPrev');
  const paginationNext = document.getElementById('paginationNext');
  const paginationCurrent = document.getElementById('paginationCurrent');
  const modalOverlay = document.getElementById('modalOverlay');

  function asset(path) {
    return rootPrefix + path;
  }

  function skillsDirectoryUrl(suffix = '') {
    return `${rootPrefix}skills/${suffix}`;
  }

  function escHTML(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[ch]));
  }

  function normalizeCategories(input, skillList) {
    const out = Object.assign({}, CATEGORY_DEFAULTS, input || {});
    for (const skill of skillList || []) {
      const key = skill.category;
      if (!key || out[key]) continue;
      out[key] = {
        name: key.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        icon: '',
        description: `${key.replace(/-/g, ' ')} skills`,
      };
    }
    return out;
  }

  function skillSearchUrl(skill) {
    return skillsDirectoryUrl(`?q=${encodeURIComponent(skill.name || skill.displayName || '')}`);
  }

  function scoreTotal(skill) {
    const total = skill.score && skill.score.total;
    return Number.isFinite(total) ? total : -1;
  }

  function getGradeClass(grade) {
    if (!grade) return '';
    const slug = String(grade).toLowerCase().replace('+', '-plus').replace('-', '-minus');
    return 'grade-' + slug;
  }

  function trustFor(skill) {
    if (!skill) return null;
    return trustData[`${skill.category}/${skill.name}`] || null;
  }

  function capValue(t, key) {
    if (!t || !t.capabilities) return undefined;
    const raw = t.capabilities[key];
    if (raw == null) return undefined;
    if (typeof raw === 'object') return raw.value == null ? undefined : raw.value;
    return raw;
  }

  function redFlagSummary(t) {
    if (!t) return null;
    let nTrue = 0;
    let nUnknown = 0;
    const trueFlags = [];
    for (const [key, label] of RED_FLAG_CAPS) {
      const v = capValue(t, key);
      if (v === true) {
        nTrue += 1;
        trueFlags.push({ key, label });
      } else if (v === undefined || v === null || v === 'unknown') {
        nUnknown += 1;
      }
    }
    return { nTrue, nUnknown, trueFlags };
  }

  function summaryForSkill(skill) {
    return skill.trustSummary || redFlagSummary(trustFor(skill));
  }

  function passesTrustFilters(skill) {
    if (directoryState.trust.size === 0) return true;
    const t = trustFor(skill);
    if (!t) return false;
    for (const id of directoryState.trust) {
      if (capValue(t, id) !== false) return false;
    }
    return true;
  }

  function isOfficialSkill(skill) {
    return officialSkills.some(s => s.category === skill.category && s.name === skill.name);
  }

  function computeOfficialSkills() {
    const official = [];
    for (const skill of skills) {
      if (OFFICIAL_PROJECTS.some(project => project.matcher(skill))) official.push(skill);
    }
    officialSkills = official;
  }

  function getProjectForSkill(skill) {
    const homeProject = homeOfficialProjects.find(project =>
      (project.skills || []).some(s => s.category === skill.category && s.name === skill.name)
    );
    if (homeProject) return homeProject;
    return OFFICIAL_PROJECTS.find(project => project.matcher(skill)) || null;
  }

  function createSkillCard(skill, isOfficial, action = pageMode === 'skills-directory' ? 'modal' : 'directory-search') {
    const card = document.createElement('article');
    card.className = 'skill-card skill-card-v2 fade-in-up';
    card.setAttribute('role', action === 'modal' ? 'button' : 'link');
    card.setAttribute('tabindex', '0');
    if (action !== 'modal') card.setAttribute('data-href', skillSearchUrl(skill));
    card.setAttribute('aria-label', `${skill.displayName || skill.name}, ${skill.category}, ${action === 'modal' ? 'view details' : 'open in skills directory'}`);

    const cat = categories[skill.category];
    const catIcon = cat?.icon || '&#128230;';
    const catName = cat?.name || skill.category;
    const summary = summaryForSkill(skill);
    let trustStrip = '';
    if (summary) {
      const trueFlags = (summary.trueFlags || []).slice(0, 3)
        .map(flag => `<span class="trust-strip-flag" title="${escHTML(flag.label)}: yes"><span aria-hidden="true">&#x26A0;</span> ${escHTML(flag.label)}</span>`)
        .join('');
      const more = Math.max(0, summary.nTrue - 3);
      const moreSpan = more > 0 ? `<span class="trust-strip-more">+${more}</span>` : '';
      const title = `${summary.nTrue} true, ${summary.nUnknown} unknown of 11 capability flags`;
      if (summary.nTrue === 0 && summary.nUnknown === 0) {
        trustStrip = `<div class="trust-strip trust-strip--clean" title="${title}"><span class="trust-strip-label">TRUST</span><span class="trust-strip-clean"><span aria-hidden="true">✓</span> No red flags detected</span></div>`;
      } else if (summary.nTrue === 0) {
        trustStrip = `<div class="trust-strip trust-strip--unknown" title="${title}"><span class="trust-strip-label">TRUST</span><span class="trust-strip-unknown"><span aria-hidden="true">?</span> ${summary.nUnknown} not measured yet</span></div>`;
      } else {
        trustStrip = `<div class="trust-strip trust-strip--some" title="${title}"><span class="trust-strip-label">TRUST</span>${trueFlags}${moreSpan}</div>`;
      }
    }

    const grade = skill.score?.grade;
    const total = skill.score?.total;
    const gradePill = grade
      ? `<span class="card-grade ${getGradeClass(grade)}" title="${total != null ? total + '/100' : ''}">${skill.score?.risk_gate === 'FAIL' ? '<span aria-hidden="true">&#9888;</span> ' : ''}${escHTML(grade)}</span>`
      : '';
    const officialPill = isOfficial ? '<span class="card-official"><span aria-hidden="true">&#10003;</span> Official</span>' : '';
    const tags = Array.isArray(skill.tags) ? skill.tags : [];

    card.innerHTML = `
      <div class="card-title-row">
        <span class="card-icon" aria-hidden="true">${catIcon}</span>
        <span class="card-name">${escHTML(skill.displayName || skill.name)}</span>
        ${gradePill}
      </div>
      <div class="card-meta-row">
        <span class="card-meta-cat">${escHTML(catName)}</span>
        <span class="card-meta-sep" aria-hidden="true">·</span>
        <span class="card-meta-author">@${escHTML(skill.author || 'unknown')}</span>
        <span class="card-meta-sep" aria-hidden="true">·</span>
        <span class="card-meta-version">v${escHTML(skill.version || '1.0.0')}</span>
      </div>
      <p class="card-desc">${escHTML(skill.description || '')}</p>
      ${trustStrip}
      <footer class="card-footer-row">
        <div class="card-tags">${tags.filter(t => t !== 'official').slice(0, 3).map(t => `<span class="card-tag">${escHTML(t)}</span>`).join('')}</div>
        ${officialPill}
      </footer>
    `;

    const go = () => {
      if (action === 'modal') openSkillModal(skill);
      else window.location.href = skillSearchUrl(skill);
    };
    card.addEventListener('click', go);
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        go();
      }
    });
    return card;
  }

  function updateStats(stats) {
    const statSkills = document.getElementById('statSkills');
    const statCategories = document.getElementById('statCategories');
    const statMCP = document.getElementById('statMCP');
    const statProtocols = document.getElementById('statProtocols');
    const officialTotalCount = document.getElementById('officialTotalCount');

    if (statSkills) statSkills.textContent = `${stats.skills}+`;
    if (statCategories) statCategories.textContent = stats.categories;
    if (statMCP) statMCP.textContent = stats.mcpServers;
    if (statProtocols) statProtocols.textContent = `${stats.protocols}+`;
    if (officialTotalCount) {
      officialTotalCount.innerHTML = `<strong>${stats.officialSkills}+</strong> official skills from <strong>${stats.officialProjects}</strong> verified teams`;
    }
  }

  function renderOfficialProjects() {
    if (!officialGrid) return;
    officialGrid.innerHTML = '';
    const projects = homeOfficialProjects.length
      ? homeOfficialProjects
      : OFFICIAL_PROJECTS.map(project => ({
          ...project,
          github: '#',
          description: '',
          skills: skills.filter(s => project.matcher(s)),
        })).filter(project => project.skills.length);

    for (const project of projects) {
      const previewHTML = project.skills.slice(0, 4).map(s =>
        `<span class="official-skill-preview-tag">${escHTML(s.displayName || s.name)}</span>`
      ).join('');

      const card = document.createElement('div');
      card.className = 'official-project-card fade-in-up';
      card.setAttribute('data-project', project.id);
      card.innerHTML = `
        <div class="official-card-top">
          <div class="official-project-icon">${project.icon}</div>
          <div class="official-project-info">
            <div class="official-project-name">${escHTML(project.name)}</div>
            <span class="official-badge">&#10003; Official</span>
          </div>
        </div>
        <div class="official-project-desc">${escHTML(project.description || '')}</div>
        <div class="official-skill-previews">${previewHTML}</div>
        <div class="official-card-bottom">
          <span class="official-skill-count"><strong>${project.skills.length}</strong> skills</span>
          <button class="official-view-all-btn" type="button">View all ${project.skills.length} skills</button>
          <a href="${escHTML(project.github || '#')}" target="_blank" rel="noopener" class="official-github-link" onclick="event.stopPropagation()">GitHub</a>
        </div>
      `;
      card.addEventListener('click', () => toggleOfficialProject(project.id, projects));
      const viewAllBtn = card.querySelector('.official-view-all-btn');
      viewAllBtn?.addEventListener('click', e => {
        e.stopPropagation();
        toggleOfficialProject(project.id, projects);
      });
      officialGrid.appendChild(card);
    }
  }

  function toggleOfficialProject(projectId, projects = homeOfficialProjects) {
    if (!officialSkillsDetail || !officialSkillsList || !officialDetailTitle) return;
    if (activeOfficialProject === projectId) {
      activeOfficialProject = null;
      officialSkillsDetail.classList.remove('active');
      document.querySelectorAll('.official-project-card').forEach(c => c.classList.remove('active'));
      return;
    }
    activeOfficialProject = projectId;
    const project = projects.find(p => p.id === projectId);
    if (!project) return;
    document.querySelectorAll('.official-project-card').forEach(c => {
      c.classList.toggle('active', c.getAttribute('data-project') === projectId);
    });
    officialDetailTitle.textContent = `${project.name} Skills (${project.skills.length})`;
    officialSkillsList.innerHTML = '';
    project.skills.forEach(skill => officialSkillsList.appendChild(createSkillCard(skill, true)));
    officialSkillsDetail.classList.add('active');
    setTimeout(() => officialSkillsDetail.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
    observeElements();
  }

  function renderCategories() {
    if (!categoriesGrid) return;
    categoriesGrid.innerHTML = '';
    Object.entries(categories)
      .sort((a, b) => (a[1].name || a[0]).localeCompare(b[1].name || b[0]))
      .forEach(([key, cat]) => {
        const count = Number.isFinite(cat.count) ? cat.count : skills.filter(s => s.category === key).length;
        const card = document.createElement('div');
        card.className = 'category-card fade-in-up';
        card.setAttribute('data-category', key);
        card.innerHTML = `
          <span class="category-icon">${cat.icon || ''}</span>
          <div class="category-name">${escHTML(cat.name || key)}</div>
          <div class="category-desc">${escHTML(cat.description || '')}</div>
          <span class="category-count">${count} skills</span>
        `;
        card.addEventListener('click', () => {
          window.location.href = skillsDirectoryUrl(`?category=${encodeURIComponent(key)}`);
        });
        categoriesGrid.appendChild(card);
      });
  }

  function renderHomeTopSkills() {
    if (!skillsGrid) return;
    skillsGrid.innerHTML = '';
    skills.slice(0, FEATURED_COUNT).forEach(skill => {
      skillsGrid.appendChild(createSkillCard(skill, isOfficialSkill(skill)));
    });
    observeElements();
  }

  async function loadHome() {
    try {
      const res = await fetch(asset('home-summary.json'), { cache: 'no-cache' });
      if (!res.ok) throw new Error('home-summary.json fetch failed');
      const summary = await res.json();
      skills = summary.topSkills || [];
      categories = normalizeCategories(summary.categories || {}, skills);
      homeOfficialProjects = summary.officialProjects || [];
      officialSkills = homeOfficialProjects.flatMap(project => project.skills || []);
      updateStats(summary.stats || {
        skills: skills.length,
        mcpServers: 0,
        categories: Object.keys(categories).length,
        protocols: 0,
        officialProjects: homeOfficialProjects.length,
        officialSkills: officialSkills.length,
      });
      renderOfficialProjects();
      renderCategories();
      renderHomeTopSkills();
    } catch (err) {
      console.error('Failed to load homepage summary:', err);
    }
  }

  function parseDirectoryState() {
    const params = new URLSearchParams(window.location.search);
    directoryState.q = (params.get('q') || '').trim();
    directoryState.category = params.get('category') || 'all';
    if (directoryState.category !== 'all' && !categories[directoryState.category]) {
      directoryState.category = 'all';
    }
    directoryState.sort = params.get('sort') || 'score_desc';
    if (!['score_desc', 'name_asc'].includes(directoryState.sort)) directoryState.sort = 'score_desc';
    directoryState.trust = new Set(
      (params.get('trust') || '')
        .split(',')
        .map(s => s.trim())
        .filter(id => TRUST_FILTERS.some(f => f.id === id))
    );
    const page = parseInt(params.get('page') || '1', 10);
    directoryState.page = Number.isFinite(page) && page > 0 ? page : 1;
  }

  function directoryParams() {
    const params = new URLSearchParams();
    if (directoryState.q) params.set('q', directoryState.q);
    if (directoryState.category !== 'all') params.set('category', directoryState.category);
    if (directoryState.sort !== 'score_desc') params.set('sort', directoryState.sort);
    if (directoryState.trust.size) params.set('trust', Array.from(directoryState.trust).join(','));
    if (directoryState.page > 1) params.set('page', String(directoryState.page));
    return params;
  }

  function syncDirectoryURL(replace = false) {
    const query = directoryParams().toString();
    const next = query ? `/skills/?${query}` : '/skills/';
    window.history[replace ? 'replaceState' : 'pushState']({}, '', next);
  }

  function searchableText(skill) {
    return [
      skill.name,
      skill.displayName,
      skill.description,
      skill.category,
      ...(skill.tags || []),
    ].join(' ').toLowerCase();
  }

  function filteredDirectorySkills() {
    const terms = directoryState.q.toLowerCase().split(/\s+/).filter(Boolean);
    let result = skills.filter(skill => {
      if (directoryState.category !== 'all' && skill.category !== directoryState.category) return false;
      if (terms.length && !terms.every(term => searchableText(skill).includes(term))) return false;
      return passesTrustFilters(skill);
    });
    if (directoryState.sort === 'name_asc') {
      result.sort((a, b) => (a.displayName || a.name).localeCompare(b.displayName || b.name));
    } else {
      result.sort((a, b) => scoreTotal(b) - scoreTotal(a) || (a.displayName || a.name).localeCompare(b.displayName || b.name));
    }
    return result;
  }

  function renderDirectoryFilters() {
    if (!filterContainer) return;
    filterContainer.innerHTML = '';
    const allBtn = createDirectoryFilterBtn('all', 'All');
    filterContainer.appendChild(allBtn);
    Object.entries(categories)
      .sort((a, b) => (a[1].name || a[0]).localeCompare(b[1].name || b[0]))
      .forEach(([key, cat]) => filterContainer.appendChild(createDirectoryFilterBtn(key, cat.name || key, cat.icon || '')));

    let trustRow = document.getElementById('trustFilterRow');
    if (!trustRow) {
      trustRow = document.createElement('div');
      trustRow.id = 'trustFilterRow';
      trustRow.className = 'trust-filter-row';
      filterContainer.parentNode.insertBefore(trustRow, filterContainer.nextSibling);
    }
    trustRow.innerHTML = '<span class="trust-filter-label">Trust filters:</span>';
    TRUST_FILTERS.forEach(filter => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'filter-btn' + (directoryState.trust.has(filter.id) ? ' trust-filter-active' : '');
      btn.textContent = filter.label;
      btn.addEventListener('click', () => {
        if (directoryState.trust.has(filter.id)) directoryState.trust.delete(filter.id);
        else directoryState.trust.add(filter.id);
        directoryState.page = 1;
        syncDirectoryURL();
        renderDirectoryFilters();
        renderDirectoryResults();
      });
      trustRow.appendChild(btn);
    });
  }

  function createDirectoryFilterBtn(key, label, icon = '') {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'filter-btn' + (key === directoryState.category ? ' active' : '');
    btn.innerHTML = icon
      ? `<span class="filter-btn-icon" aria-hidden="true">${escHTML(icon)}</span><span class="filter-btn-label">${escHTML(label)}</span>`
      : `<span class="filter-btn-label">${escHTML(label)}</span>`;
    btn.addEventListener('click', () => {
      directoryState.category = key;
      directoryState.page = 1;
      syncDirectoryURL();
      renderDirectoryFilters();
      renderDirectoryResults();
    });
    return btn;
  }

  function renderDirectoryResults(replaceURL = false) {
    if (!skillsGrid) return;
    const filtered = filteredDirectorySkills();
    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (directoryState.page > totalPages) {
      directoryState.page = totalPages;
      syncDirectoryURL(true);
    } else if (replaceURL) {
      syncDirectoryURL(true);
    }
    const start = (directoryState.page - 1) * PAGE_SIZE;
    const pageSkills = filtered.slice(start, start + PAGE_SIZE);
    skillsGrid.innerHTML = '';
    pageSkills.forEach(skill => skillsGrid.appendChild(createSkillCard(skill, isOfficialSkill(skill))));
    if (directoryResultSummary) {
      const end = Math.min(start + pageSkills.length, filtered.length);
      directoryResultSummary.textContent = filtered.length
        ? `Showing ${start + 1}-${end} of ${filtered.length} skills`
        : 'No skills match the active filters';
    }
    if (paginationCurrent) paginationCurrent.textContent = `Page ${directoryState.page} of ${totalPages}`;
    if (paginationPrev) paginationPrev.disabled = directoryState.page <= 1;
    if (paginationNext) paginationNext.disabled = directoryState.page >= totalPages;
    observeElements();
  }

  function wireDirectoryControls() {
    if (directorySearch) {
      directorySearch.value = directoryState.q;
      directorySearch.addEventListener('input', e => {
        directoryState.q = e.target.value.trim();
        directoryState.page = 1;
        syncDirectoryURL();
        renderDirectoryResults();
      });
    }
    if (directorySort) {
      directorySort.value = directoryState.sort;
      directorySort.addEventListener('change', e => {
        directoryState.sort = e.target.value;
        directoryState.page = 1;
        syncDirectoryURL();
        renderDirectoryResults();
      });
    }
    paginationPrev?.addEventListener('click', () => {
      if (directoryState.page <= 1) return;
      directoryState.page -= 1;
      syncDirectoryURL();
      renderDirectoryResults();
    });
    paginationNext?.addEventListener('click', () => {
      directoryState.page += 1;
      syncDirectoryURL();
      renderDirectoryResults();
    });
    window.addEventListener('popstate', () => {
      parseDirectoryState();
      if (directorySearch) directorySearch.value = directoryState.q;
      if (directorySort) directorySort.value = directoryState.sort;
      renderDirectoryFilters();
      renderDirectoryResults(true);
    });
    if (window.location.hash === '#search') setTimeout(() => directorySearch?.focus(), 100);
  }

  async function loadDirectory() {
    try {
      const [catalogRes, capsRes] = await Promise.all([
        fetch(asset('skills.json'), { cache: 'no-cache' }),
        fetch(asset('capabilities.json'), { cache: 'no-cache' }),
      ]);
      if (!catalogRes.ok) throw new Error(`skills.json fetch failed (${catalogRes.status})`);
      const catalog = await catalogRes.json();
      skills = (catalog.skills || []).map(skill => Object.assign({}, skill));
      categories = normalizeCategories(catalog.categories || {}, skills);
      if (capsRes.ok) {
        const caps = await capsRes.json();
        trustData = caps.skills || {};
      }
      computeOfficialSkills();
      parseDirectoryState();
      renderDirectoryFilters();
      wireDirectoryControls();
      renderDirectoryResults(true);
    } catch (err) {
      console.error('Failed to load skills directory:', err);
      if (directoryResultSummary) {
        directoryResultSummary.textContent = window.location.protocol === 'file:'
          ? 'This page was opened as a local file, so the browser cannot load skills.json. Run python3 -m http.server 8080 --directory docs/_site, then open http://localhost:8080/skills/.'
          : 'Could not load skills directory. Check that skills.json is available beside the published site.';
      }
    }
  }

  function renderTrustPanel(skill) {
    const t = trustFor(skill);
    const cat = encodeURIComponent(skill.category || '');
    const nm = encodeURIComponent(skill.name || '');
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
        <div class="modal-section-title">Trust profile</div>
        <div class="trust-panel">
          <p class="trust-empty">No trust manifest computed for this skill yet. Treat capabilities as <strong>unknown</strong> until the scanner generates one.</p>
          ${links}
        </div>`;
    }

    const caps = t.capabilities || {};
    const buckets = { true: [], false: [], unknown: [] };
    const icon = { true: '&#x26A0;', false: '&#x2713;', unknown: '?' };
    const aria = { true: 'Yes - red flag', false: 'No - cleared', unknown: 'Not measured' };

    for (const [key, label, hint] of RED_FLAG_CAPS) {
      const raw = caps[key];
      const val = raw && typeof raw === 'object' ? raw.value : raw;
      const conf = raw && typeof raw === 'object' ? raw.confidence : null;
      const src = raw && typeof raw === 'object' ? raw.source : null;
      const group = val === true ? 'true' : val === false ? 'false' : 'unknown';
      const confDot = group !== 'unknown' && conf
        ? `<span class="trust-cap-confidence trust-cap-confidence--${escHTML(conf)}" title="${escHTML(conf)} confidence (${escHTML(src || 'unknown')})" aria-label="${escHTML(conf)} confidence based on ${escHTML(src || 'unknown')} evidence"></span>`
        : '';

      buckets[group].push(
        `<li class="trust-cap-v2" data-state="${group}">` +
          `<span class="trust-cap-icon" aria-label="${aria[group]}" title="${aria[group]}">${icon[group]}</span>` +
          '<div class="trust-cap-body">' +
            `<span class="trust-cap-label">${escHTML(label)}</span>` +
            `<span class="trust-cap-hint">${escHTML(hint)}</span>` +
          '</div>' +
          confDot +
        '</li>'
      );
    }

    const sectionDefs = [
      { state: 'true', title: 'Red flags', kicker: 'things this skill can do that affect your security or funds' },
      { state: 'false', title: 'Cleared by scanner', kicker: 'we scanned the skill text and scripts and found no evidence of these' },
      { state: 'unknown', title: 'Not measured yet', kicker: 'the scanner could not make a confident call; treat as possible risk' },
    ];
    const groupClass = { true: 'flags', false: 'clear', unknown: 'unknown' };
    const sections = sectionDefs.map(({ state, title, kicker }) => {
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

    const operators = t.detected_hosted_operators || t.hosted_operators || [];
    const ingredients = operators.length
      ? `<h3 class="trust-subhead">Ingredients</h3>
         <p class="trust-help">External services this skill needs in order to work.</p>
         <ul class="trust-ingredient-list">${operators.map(op => `<li class="trust-ingredient"><span class="trust-ingredient-kind">service</span> <code>${escHTML(op)}</code></li>`).join('')}</ul>`
      : '<h3 class="trust-subhead">Ingredients</h3><p class="trust-empty trust-help">No recognized hosted services were found in this skill text or scripts. This does not prove the skill is local-only.</p>';

    const audits = t.audits || [];
    const auditsHTML = audits.length
      ? `<h3 class="trust-subhead">Audits</h3><ul class="trust-audit-list">${audits.map(a => {
          const reviewer = a.reviewer || {};
          return `<li class="trust-audit"><strong>${escHTML(reviewer.name || 'Unknown')}</strong> <span class="trust-tier trust-tier--${escHTML(reviewer.tier || 'unverified')}">${escHTML(reviewer.tier || 'unverified')}</span> &middot; subject <code>${escHTML(a.subject || '')}</code> &middot; ${escHTML(a.date || '')}</li>`;
        }).join('')}</ul>`
      : '<h3 class="trust-subhead">Audits</h3><p class="trust-empty trust-help">No audit has been recorded for this skill yet.</p>';

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
      <p class="trust-help">Detected automatically by an open-source scanner that reads the skill text and scripts. Not measured is not a green check.</p>
      <div class="trust-panel">
        ${sections}
        ${ingredients}
        ${auditsHTML}
        ${links}
      </div>`;
  }

  function renderScoreDetail(skill) {
    if (!skill.score || skill.score.total == null) return '';
    const s = skill.score;
    const grade = s.grade || 'F';
    const gradeClass = getGradeClass(grade);
    const riskClass = s.risk_gate === 'PASS' ? 'pass' : 'fail';
    const riskIcon = s.risk_gate === 'PASS' ? '&#10003;' : '&#9888;';
    const riskLabel = s.risk_gate || 'N/A';
    const dimensionMaxes = { static: 40, security: 20, depth: 40 };

    function fillClass(points, max) {
      const pct = max > 0 ? (points / max) * 100 : 0;
      if (pct >= 80) return 'fill-a';
      if (pct >= 60) return 'fill-b';
      if (pct >= 40) return 'fill-c';
      if (pct >= 20) return 'fill-d';
      return 'fill-f';
    }

    const barsHTML = ['static', 'security', 'depth'].map(dim => {
      const points = s[dim] != null ? s[dim] : 0;
      const max = dimensionMaxes[dim] || 40;
      const pct = max > 0 ? Math.round((points / max) * 100) : 0;
      return `
        <div class="score-dimension">
          <span class="score-dimension-label">${escHTML(dim)}</span>
          <div class="score-dimension-bar">
            <div class="score-dimension-fill ${fillClass(points, max)}" style="width:${pct}%"></div>
          </div>
          <span class="score-dimension-value">${points}/${max}</span>
        </div>`;
    }).join('');

    return `
      <div class="modal-score-section">
        <div class="modal-score-header">
          <div class="modal-score-overall">
            <span class="modal-score-number">${escHTML(s.total)}</span>
            <span class="modal-score-max">/ 100</span>
            <span class="modal-score-grade skill-score-badge ${gradeClass}">${escHTML(grade)}</span>
          </div>
          <div class="modal-risk-gate ${riskClass}">
            <span>${riskIcon}</span>
            Risk: ${escHTML(riskLabel)}
          </div>
        </div>
        <div class="modal-score-dimensions">${barsHTML}</div>
      </div>`;
  }

  function installCommandsFor(skill) {
    if (skill.category === 'mcp-servers') {
      return [
        { label: 'MCP', command: `claude mcp add ${skill.name || ''}` },
        { label: 'Git', command: 'git clone https://github.com/jiayaoqijia/cryptoskill.git' },
      ];
    }
    return [
      { label: 'Claude', command: `cp -r cryptoskill/skills/${skill.category || ''}/${skill.name || ''} .claude/skills/` },
      { label: 'Claw', command: `clawhub install ${skill.name || ''}` },
    ];
  }

  function openSkillModal(skill) {
    if (!modalOverlay) return;
    const modalContent = modalOverlay.querySelector('.modal');
    if (!modalContent) return;

    const cat = categories[skill.category] || {};
    const project = getProjectForSkill(skill);
    const isOfficial = isOfficialSkill(skill);
    const sourceUrl = `https://github.com/jiayaoqijia/cryptoskill/tree/main/skills/${encodeURIComponent(skill.category || '')}/${encodeURIComponent(skill.name || '')}`;
    const tags = Array.isArray(skill.tags) ? skill.tags.filter(Boolean) : [];
    const tagHTML = tags.length
      ? tags.map(t => `<span class="modal-tag">${escHTML(t)}</span>`).join('')
      : '<span class="modal-tag">untagged</span>';
    const installHTML = installCommandsFor(skill).map(({ label, command }) => `
      <div class="install-cmd">
        <span class="prompt">${escHTML(label)}</span>
        <code>${escHTML(command)}</code>
        <button class="copy-btn" type="button" data-copy="${escHTML(command)}" title="Copy">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
        </button>
      </div>`).join('');

    modalContent.innerHTML = `
      <button class="modal-close" type="button" aria-label="Close details">&times;</button>
      <div class="modal-header">
        <div class="modal-icon" aria-hidden="true">${cat.icon || '&#128230;'}</div>
        <div>
          <div class="modal-title">${escHTML(skill.displayName || skill.name)}</div>
          <div class="modal-meta">
            <span class="author">@${escHTML(skill.author || 'unknown')}</span>
            <span>&middot;</span>
            <span>v${escHTML(skill.version || '1.0.0')}</span>
            <span>&middot;</span>
            <span>${escHTML(cat.name || skill.category || 'Uncategorized')}</span>
            ${project ? `<span>&middot;</span><span>${escHTML(project.name)}</span>` : ''}
            ${isOfficial ? '<span class="modal-official-badge">&#10003; Official</span>' : ''}
          </div>
        </div>
      </div>
      <div class="modal-desc">${escHTML(skill.description || '')}</div>
      <div class="modal-section-title">Tags</div>
      <div class="modal-tags">${tagHTML}</div>
      <div class="modal-section-title">Install</div>
      <div class="modal-install">${installHTML}</div>
      <div class="modal-section-title">Source</div>
      <p class="trust-source-links"><a href="${sourceUrl}" target="_blank" rel="noopener">View source on GitHub &rarr;</a></p>
      ${renderScoreDetail(skill)}
      ${renderTrustPanel(skill)}
    `;

    modalContent.querySelector('.modal-close')?.addEventListener('click', closeSkillModal);
    modalContent.querySelectorAll('[data-copy]').forEach(btn => {
      btn.addEventListener('click', () => copyToClipboard(btn.getAttribute('data-copy') || '', btn));
    });
    modalOverlay.classList.add('active');
    modalOverlay.setAttribute('aria-modal', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeSkillModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove('active');
    modalOverlay.removeAttribute('aria-modal');
    document.body.style.overflow = '';
  }

  function focusOrNavigateSearch() {
    if (pageMode === 'skills-directory') {
      directorySearch?.focus();
      if (window.location.hash !== '#search') {
        window.history.replaceState({}, '', `${window.location.pathname}${window.location.search}#search`);
      }
      return;
    }
    window.location.href = skillsDirectoryUrl('#search');
  }

  function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    const savedTheme = localStorage.getItem('cryptoskill-theme') || localStorage.getItem('theme');
    if (savedTheme === 'light') document.documentElement.setAttribute('data-theme', 'light');
    else document.documentElement.removeAttribute('data-theme');
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const next = currentTheme === 'light' ? 'dark' : 'light';
      if (next === 'dark') document.documentElement.removeAttribute('data-theme');
      else document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('cryptoskill-theme', next);
      localStorage.setItem('theme', next);
    });
  }

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
      window.location.href = 'mailto:maintainers+cryptoskills@altresear.ch?subject=' + subject + '&body=' + body;
    });
  }

  function observeElements() {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px 50px 0px' });
    document.querySelectorAll('.fade-in-up:not(.visible), .stagger:not(.visible)').forEach(el => observer.observe(el));
  }

  window.switchInstallTab = function (tab, btn) {
    document.querySelectorAll('.install-panel').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.install-tab').forEach(t => t.classList.remove('active'));
    const panel = document.getElementById('install-' + tab);
    if (panel) panel.style.display = 'block';
    if (btn) btn.classList.add('active');
  };

  window.copyToClipboard = function (text, btn) {
    navigator.clipboard.writeText(text).then(() => {
      btn.classList.add('copied');
      const old = btn.innerHTML;
      btn.textContent = 'Copied';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.innerHTML = old;
      }, 1600);
    });
  };

  if (officialDetailClose) {
    officialDetailClose.addEventListener('click', () => {
      activeOfficialProject = null;
      officialSkillsDetail?.classList.remove('active');
      document.querySelectorAll('.official-project-card').forEach(c => c.classList.remove('active'));
    });
  }

  document.querySelectorAll('.nav-search-btn, .mobile-search-btn').forEach(btn => {
    btn.addEventListener('click', focusOrNavigateSearch);
  });

  searchOverlay?.addEventListener('click', e => {
    if (e.target === searchOverlay) searchOverlay.classList.remove('active');
  });

  modalOverlay?.addEventListener('click', e => {
    if (e.target === modalOverlay) closeSkillModal();
  });

  searchInput?.addEventListener('input', e => {
    if (!searchResults) return;
    const value = e.target.value.trim();
    searchResults.innerHTML = value
      ? `<div class="search-empty">Press Enter to search for "${escHTML(value)}" in the full directory.</div>`
      : '';
  });

  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      focusOrNavigateSearch();
    }
    if (e.key === 'Enter' && searchOverlay?.classList.contains('active') && searchInput?.value.trim()) {
      window.location.href = skillsDirectoryUrl(`?q=${encodeURIComponent(searchInput.value.trim())}#search`);
    }
    if (e.key === 'Escape') {
      searchOverlay?.classList.remove('active');
      closeSkillModal();
    }
  });

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => navLinks?.classList.toggle('open'));
  }

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
        navLinks?.classList.remove('open');
      }
    });
  });

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSubmitForm();
    if (pageMode === 'skills-directory') loadDirectory();
    else loadHome();
    observeElements();
  });
})();
