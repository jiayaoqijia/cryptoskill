const { test, expect } = require('@playwright/test');
const path = require('path');

async function waitForHome(page) {
  await page.waitForFunction(() => {
    const official = document.getElementById('officialGrid');
    const top = document.getElementById('skillsGrid');
    return official && official.children.length > 0 && top && top.children.length > 0;
  }, { timeout: 10000 });
}

async function waitForDirectory(page) {
  await page.waitForFunction(() => {
    const grid = document.getElementById('skillsGrid');
    return grid && grid.children.length > 0;
  }, { timeout: 10000 });
}

test.describe('CryptoSkill Homepage', () => {
  test('loads the lightweight homepage summary instead of the full skills catalog', async ({ page }) => {
    const requests = [];
    page.on('request', request => requests.push(request.url()));

    await page.goto('/');
    await waitForHome(page);

    expect(requests.some(url => url.endsWith('/home-summary.json'))).toBe(true);
    expect(requests.some(url => url.endsWith('/skills.json'))).toBe(false);
    expect(requests.some(url => url.endsWith('/capabilities.json'))).toBe(false);
  });

  test('page loads with correct title and stats', async ({ page }) => {
    await page.goto('/');
    await waitForHome(page);

    await expect(page).toHaveTitle(/CryptoSkill/);
    await expect(page.locator('h1')).toContainText('Crypto Skill Hub');
    await expect(page.locator('.hero-badge')).toContainText('Open Source');

    const skillCount = await page.locator('#statSkills').textContent();
    expect(parseInt(skillCount)).toBeGreaterThan(1200);

    const catCount = await page.locator('#statCategories').textContent();
    expect(parseInt(catCount)).toBeGreaterThanOrEqual(14);
  });

  test('top navigation sends full browsing to the real /skills/ route', async ({ page }) => {
    await page.goto('/');
    await waitForHome(page);

    await expect(page.locator('.nav-links a', { hasText: 'Skills' }).first()).toHaveAttribute('href', 'skills/');
    await expect(page.locator('.hero-actions .btn-primary')).toHaveAttribute('href', 'skills/');
  });

  test('official project cards and top skills render from summary data', async ({ page }) => {
    await page.goto('/');
    await waitForHome(page);

    const officialCards = page.locator('.official-project-card');
    expect(await officialCards.count()).toBeGreaterThanOrEqual(9);

    const binanceCard = page.locator('.official-project-card[data-project="binance"]');
    await expect(binanceCard).toBeVisible();
    await expect(binanceCard.locator('.official-project-name')).toContainText('Binance');

    const topCards = page.locator('#skillsGrid .skill-card');
    await expect(topCards).toHaveCount(12);
  });

  test('Cmd+K jumps to the skills directory search', async ({ page }) => {
    await page.goto('/');
    await waitForHome(page);

    await page.keyboard.press('Meta+k');
    await expect(page).toHaveURL(/\/skills\/#search$/);
  });
});

test.describe('Skills Directory', () => {
  test('renders 48 score-sorted skill cards on page 1', async ({ page }) => {
    await page.goto('/skills/');
    await waitForDirectory(page);

    const cards = page.locator('#skillsGrid .skill-card');
    await expect(cards).toHaveCount(48);

    const firstScore = await cards.first().locator('.card-grade').getAttribute('title');
    const secondScore = await cards.nth(1).locator('.card-grade').getAttribute('title');
    expect(parseInt(firstScore)).toBeGreaterThanOrEqual(parseInt(secondScore));
  });

  test('uses one icon-labeled category filter row', async ({ page }) => {
    await page.goto('/skills/');
    await waitForDirectory(page);

    await expect(page.locator('.directory-quick-cats')).toHaveCount(0);

    const exchangeFilter = page.locator('#filterContainer .filter-btn', { hasText: 'Exchanges' });
    await expect(exchangeFilter).toBeVisible();
    await expect(exchangeFilter.locator('.filter-btn-icon')).toContainText('🏦');
  });

  test('search, category, trust, sort, and page state survive refresh', async ({ page }) => {
    await page.goto('/skills/?q=a&category=exchanges&sort=score_desc&trust=can_execute_shell&page=2');
    await waitForDirectory(page);

    await expect(page.locator('#directorySearch')).toHaveValue('a');
    await expect(page.locator('.filter-btn.active', { hasText: 'Exchanges' })).toBeVisible();
    await expect(page.locator('#trustFilterRow .trust-filter-active', { hasText: 'Cannot execute shell' })).toBeVisible();
    await expect(page.locator('#directorySort')).toHaveValue('score_desc');
    await expect(page.locator('#paginationCurrent')).toContainText('Page 2');

    await page.reload();
    await waitForDirectory(page);

    await expect(page.locator('#directorySearch')).toHaveValue('a');
    await expect(page.locator('#paginationCurrent')).toContainText('Page 2');
  });

  test('pagination updates the URL and result set', async ({ page }) => {
    await page.goto('/skills/');
    await waitForDirectory(page);

    const firstCardName = await page.locator('#skillsGrid .card-name').first().textContent();
    await page.locator('#paginationNext').click();

    await expect(page).toHaveURL(/\/skills\/\?page=2$/);
    await expect(page.locator('#paginationCurrent')).toContainText('Page 2');
    await expect(page.locator('#skillsGrid .card-name').first()).not.toHaveText(firstCardName);
  });

  test('clicking a skill opens a details modal without changing URL', async ({ page }) => {
    await page.goto('/skills/?q=uniswap');
    await waitForDirectory(page);

    const before = page.url();
    const card = page.locator('#skillsGrid .skill-card').first();
    await card.click();

    await expect(page).toHaveURL(before);
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);
    await expect(page.locator('#modalOverlay .modal-title')).toContainText(/uniswap/i);
    await expect(page.locator('#modalOverlay .modal-section-title', { hasText: 'Install' })).toBeVisible();
    await expect(page.locator('#modalOverlay .modal-section-title', { hasText: /Trust/i })).toBeVisible();
  });

  test('details modal closes with button, overlay click, and Escape', async ({ page }) => {
    await page.goto('/skills/?q=uniswap');
    await waitForDirectory(page);

    await page.locator('#skillsGrid .skill-card').first().click();
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);

    await page.locator('#modalOverlay .modal-close').click();
    await expect(page.locator('#modalOverlay')).not.toHaveClass(/active/);

    await page.locator('#skillsGrid .skill-card').first().click();
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);
    await page.locator('#modalOverlay').click({ position: { x: 8, y: 8 } });
    await expect(page.locator('#modalOverlay')).not.toHaveClass(/active/);

    await page.locator('#skillsGrid .skill-card').first().click();
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);
    await page.keyboard.press('Escape');
    await expect(page.locator('#modalOverlay')).not.toHaveClass(/active/);
  });
});

test.describe('Generated Routes', () => {
  test('old category and skill detail routes are not generated', async ({ page }) => {
    const categoryResponse = await page.goto('/skills/analytics/');
    expect(categoryResponse.status()).toBe(404);

    const detailResponse = await page.goto('/skills/analytics/defillama-api.html');
    expect(detailResponse.status()).toBe(404);
  });

  test('sitemap includes /skills/ but no old category or detail pages', async ({ page }) => {
    const response = await page.goto('/sitemap.xml');
    expect(response.ok()).toBe(true);
    await expect(page.locator('body')).toContainText('https://cryptoskill.org/skills/');
    await expect(page.locator('body')).not.toContainText('https://cryptoskill.org/skills/analytics/');
    await expect(page.locator('body')).not.toContainText('https://cryptoskill.org/skills/analytics/defillama-api.html');
  });
});

test.describe('Local Preview Guardrails', () => {
  test('direct file opening explains that the directory needs an HTTP server', async ({ page }) => {
    await page.goto('file://' + path.resolve(__dirname, '../docs/_site/skills/index.html'));

    await expect(page.locator('#directoryResultSummary')).toContainText(
      'Run python3 -m http.server 8080 --directory docs/_site'
    );
  });
});

test.describe('Theme Persistence', () => {
  test('light mode persists from homepage to generated skills directory', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();

    await page.locator('#themeToggle').click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await expect.poll(() => page.evaluate(() => localStorage.getItem('cryptoskill-theme'))).toBe('light');

    await page.goto('/skills/');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  });
});

test.describe('Install Section', () => {
  test('shows install tabs with correct commands', async ({ page }) => {
    await page.goto('/');

    const claudePanel = page.locator('#install-claude');
    await expect(claudePanel).toBeVisible();
    await expect(claudePanel.locator('code').nth(1)).toContainText('git clone');

    await page.locator('.install-tab', { hasText: /MCP/ }).click();
    const mcpPanel = page.locator('#install-mcp');
    await expect(mcpPanel).toBeVisible();
    await expect(mcpPanel.locator('code').nth(1)).toContainText('claude mcp add');

    await page.locator('.install-tab', { hasText: /OpenClaw/ }).click();
    const openclawPanel = page.locator('#install-openclaw');
    await expect(openclawPanel).toBeVisible();
    await expect(openclawPanel.locator('code').last()).toContainText('clawhub install');
  });
});

test.describe('Responsive', () => {
  test('mobile nav toggle works', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');

    const toggle = page.locator('#mobileToggle');
    await expect(toggle).toBeVisible();

    await toggle.click();
    await expect(page.locator('#navLinks')).toHaveClass(/open/);
  });
});
