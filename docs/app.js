/* ============================================
   CryptoSkill - App JavaScript
   ============================================ */

(function () {
  'use strict';

  // --- State ---
  let skills = [];
  let categories = {};
  let activeFilter = 'all';
  const FEATURED_COUNT = 12;
  let showingAll = false;

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

  // --- Load Skills Catalog ---
  async function loadSkills() {
    try {
      const res = await fetch('skills.json');
      const data = await res.json();
      skills = data.skills;
      categories = data.categories;
      renderCategories();
      renderFilters();
      renderSkills();
      updateStats();
    } catch (err) {
      console.error('Failed to load skills catalog:', err);
    }
  }

  // --- Update Stats ---
  function updateStats() {
    const statSkills = document.getElementById('statSkills');
    const statCategories = document.getElementById('statCategories');
    const statProtocols = document.getElementById('statProtocols');
    if (statSkills) statSkills.textContent = skills.length + '+';
    if (statCategories) statCategories.textContent = Object.keys(categories).length;
    // Count unique first tags (proxy for protocols)
    const protocols = new Set();
    skills.forEach(s => {
      if (s.tags && s.tags.length > 0) protocols.add(s.tags[0]);
    });
    if (statProtocols) statProtocols.textContent = protocols.size + '+';
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
    // All filter
    const allBtn = createFilterBtn('all', 'All');
    filterContainer.appendChild(allBtn);
    // Category filters
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
    // Update buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.toggle('active', btn.textContent === (category === 'all' ? 'All' : categories[category]?.name));
    });
    // Also update category cards
    document.querySelectorAll('.category-card').forEach(card => {
      card.style.outline = card.getAttribute('data-category') === category ? '1px solid rgba(99, 102, 241, 0.4)' : '';
    });
    renderSkills();
  }

  // --- Render Skills ---
  function renderSkills() {
    if (!skillsGrid) return;
    skillsGrid.innerHTML = '';
    let filtered = activeFilter === 'all' ? [...skills] : skills.filter(s => s.category === activeFilter);
    const displaySkills = showingAll ? filtered : filtered.slice(0, FEATURED_COUNT);

    displaySkills.forEach(skill => {
      const card = document.createElement('div');
      card.className = 'skill-card fade-in-up';
      const cat = categories[skill.category];
      card.innerHTML = `
        <div class="skill-card-header">
          <div class="skill-name">${skill.displayName}</div>
          <span class="skill-badge">${cat ? cat.name : skill.category}</span>
        </div>
        <div class="skill-desc">${skill.description}</div>
        <div class="skill-footer">
          <div class="skill-tags">
            ${skill.tags.slice(0, 3).map(t => `<span class="skill-tag">${t}</span>`).join('')}
          </div>
          <span class="skill-version">v${skill.version}</span>
        </div>
      `;
      card.addEventListener('click', () => openModal(skill));
      skillsGrid.appendChild(card);
    });

    // Show/hide "Show More" button
    if (showMoreBtn) {
      if (filtered.length > FEATURED_COUNT && !showingAll) {
        showMoreBtn.style.display = 'block';
        showMoreBtn.querySelector('button').textContent = `Show all ${filtered.length} skills`;
      } else {
        showMoreBtn.style.display = 'none';
      }
    }

    // Re-observe for animations
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
    const modalContent = modalOverlay.querySelector('.modal');
    modalContent.innerHTML = `
      <div class="modal-header">
        <div class="modal-icon">${cat ? cat.icon : '📦'}</div>
        <div>
          <div class="modal-title">${skill.displayName}</div>
          <div class="modal-meta">
            <span class="author">@${skill.author}</span>
            <span>·</span>
            <span>v${skill.version}</span>
            <span>·</span>
            <span>${cat ? cat.name : skill.category}</span>
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
        <div class="install-cmd">
          <span class="prompt">$</span>
          <code>cryptoskill install ${skill.name}</code>
          <button class="copy-btn" onclick="copyToClipboard('cryptoskill install ${skill.name}', this)" title="Copy">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
          </button>
        </div>
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

  // Search button in nav
  document.querySelectorAll('.nav-search-btn, .mobile-search-btn').forEach(btn => {
    btn.addEventListener('click', openSearch);
  });

  // Close on overlay click
  searchOverlay.addEventListener('click', (e) => {
    if (e.target === searchOverlay) closeSearch();
  });

  // Keyboard shortcut
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

  // Search input
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
      return `
        <div class="search-result-item" data-skill="${skill.name}">
          <div class="result-icon">${cat ? cat.icon : '📦'}</div>
          <div class="result-info">
            <div class="result-name">${skill.displayName}</div>
            <div class="result-desc">${skill.description}</div>
          </div>
          <span class="result-category">${cat ? cat.name : skill.category}</span>
        </div>
      `;
    }).join('');

    // Bind clicks
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
        // Close mobile nav if open
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
