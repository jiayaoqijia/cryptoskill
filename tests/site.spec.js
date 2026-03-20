const { test, expect } = require('@playwright/test');

test.describe('CryptoSkill Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for skills.json to load
    await page.waitForFunction(() => {
      const grid = document.getElementById('officialGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });
  });

  test('page loads with correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/CryptoSkill/);
  });

  test('hero section renders correctly', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Crypto Skill Hub');
    await expect(page.locator('.subtitle')).toBeVisible();
    await expect(page.locator('.hero-badge')).toContainText('Open Source');
  });

  test('stats bar shows correct numbers', async ({ page }) => {
    const skillCount = await page.locator('#statSkills').textContent();
    expect(parseInt(skillCount)).toBeGreaterThan(200);

    const catCount = await page.locator('#statCategories').textContent();
    expect(parseInt(catCount)).toBeGreaterThanOrEqual(13);
  });

  test('official skills section appears before community', async ({ page }) => {
    const officialSection = page.locator('#official');
    const communitySection = page.locator('#skills');

    const officialY = await officialSection.boundingBox();
    const communityY = await communitySection.boundingBox();

    expect(officialY.y).toBeLessThan(communityY.y);
  });

  test('official project cards render with correct data', async ({ page }) => {
    const cards = page.locator('.official-project-card');
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(8);

    // Check Binance card exists
    const binanceCard = page.locator('.official-project-card[data-project="binance"]');
    await expect(binanceCard).toBeVisible();
    await expect(binanceCard.locator('.official-project-name')).toContainText('Binance');
    await expect(binanceCard.locator('.official-badge')).toContainText('Official');
  });

  test('clicking official project card expands skill list', async ({ page }) => {
    const binanceCard = page.locator('.official-project-card[data-project="binance"]');
    await binanceCard.click();

    const detail = page.locator('#officialSkillsDetail');
    await expect(detail).toHaveClass(/active/);
    await expect(page.locator('#officialDetailTitle')).toContainText('Binance');

    // Should show individual skills
    const skillCards = page.locator('#officialSkillsList .skill-card');
    const skillCount = await skillCards.count();
    expect(skillCount).toBeGreaterThan(0);
  });

  test('close button hides official detail panel', async ({ page }) => {
    // Open
    await page.locator('.official-project-card[data-project="binance"]').click();
    await expect(page.locator('#officialSkillsDetail')).toHaveClass(/active/);

    // Close
    await page.locator('#officialDetailClose').click();
    await expect(page.locator('#officialSkillsDetail')).not.toHaveClass(/active/);
  });

  test('official GitHub links point to correct repos', async ({ page }) => {
    const binanceLink = page.locator('.official-project-card[data-project="binance"] .official-github-link');
    await expect(binanceLink).toHaveAttribute('href', 'https://github.com/binance/binance-skills-hub');

    const okxLink = page.locator('.official-project-card[data-project="okx"] .official-github-link');
    await expect(okxLink).toHaveAttribute('href', 'https://github.com/okx/onchainos-skills');
  });
});

test.describe('Categories Section', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForFunction(() => {
      const grid = document.getElementById('categoriesGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });
  });

  test('all 13 categories render', async ({ page }) => {
    const cards = page.locator('.category-card');
    const count = await cards.count();
    expect(count).toBe(13);
  });

  test('clicking category scrolls to skills and filters', async ({ page }) => {
    await page.locator('.category-card').first().click();
    // Should scroll to skills section
    await page.waitForTimeout(500);
    const activeFilter = page.locator('.filter-btn.active');
    const count = await activeFilter.count();
    expect(count).toBe(1);
  });
});

test.describe('Community Skills Section', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForFunction(() => {
      const grid = document.getElementById('skillsGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });
  });

  test('community skills render (not official ones)', async ({ page }) => {
    const cards = page.locator('#skillsGrid .skill-card');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
    expect(count).toBeLessThanOrEqual(12); // FEATURED_COUNT

    // None should have official badge
    const officialBadges = page.locator('#skillsGrid .official-tag');
    const officialCount = await officialBadges.count();
    expect(officialCount).toBe(0);
  });

  test('show more button works', async ({ page }) => {
    const showMore = page.locator('#showMoreBtn button');
    if (await showMore.isVisible()) {
      const beforeCount = await page.locator('#skillsGrid .skill-card').count();
      await showMore.click();
      await page.waitForTimeout(500);
      const afterCount = await page.locator('#skillsGrid .skill-card').count();
      expect(afterCount).toBeGreaterThan(beforeCount);
    }
  });

  test('filter buttons work', async ({ page }) => {
    const allBtn = page.locator('.filter-btn', { hasText: /^All$/ });
    await expect(allBtn).toHaveClass(/active/);

    // Click a category filter
    const exchangeBtn = page.locator('.filter-btn', { hasText: /^Exchanges$/ });
    if (await exchangeBtn.isVisible()) {
      await exchangeBtn.click();
      await expect(exchangeBtn).toHaveClass(/active/);
      await expect(allBtn).not.toHaveClass(/active/);
    }
  });
});

test.describe('Search', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForFunction(() => {
      const grid = document.getElementById('officialGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });
  });

  test('Cmd+K opens search overlay', async ({ page }) => {
    await page.keyboard.press('Meta+k');
    await expect(page.locator('#searchOverlay')).toHaveClass(/active/);
  });

  test('search finds skills', async ({ page }) => {
    await page.keyboard.press('Meta+k');
    await page.locator('#searchInput').fill('binance');
    await page.waitForTimeout(300);

    const results = page.locator('.search-result-item');
    const count = await results.count();
    expect(count).toBeGreaterThan(0);
  });

  test('search shows official/community badges', async ({ page }) => {
    await page.keyboard.press('Meta+k');
    await page.locator('#searchInput').fill('binance');
    await page.waitForTimeout(300);

    const badges = page.locator('.result-badge');
    const count = await badges.count();
    expect(count).toBeGreaterThan(0);
  });

  test('Escape closes search', async ({ page }) => {
    await page.keyboard.press('Meta+k');
    await expect(page.locator('#searchOverlay')).toHaveClass(/active/);
    await page.keyboard.press('Escape');
    await expect(page.locator('#searchOverlay')).not.toHaveClass(/active/);
  });

  test('clicking search result opens modal', async ({ page }) => {
    await page.keyboard.press('Meta+k');
    await page.locator('#searchInput').fill('uniswap');
    await page.waitForTimeout(300);

    const firstResult = page.locator('.search-result-item').first();
    if (await firstResult.isVisible()) {
      await firstResult.click();
      await expect(page.locator('#modalOverlay')).toHaveClass(/active/);
    }
  });
});

test.describe('Skill Modal', () => {
  test('modal shows install command with correct path', async ({ page }) => {
    await page.goto('/');
    await page.waitForFunction(() => {
      const grid = document.getElementById('skillsGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });

    await page.locator('#skillsGrid .skill-card').first().click();
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);

    const installCmd = page.locator('.modal .install-cmd code');
    const cmdText = await installCmd.textContent();
    expect(cmdText).toContain('cp -r cryptoskill/skills/');
  });

  test('modal closes on overlay click', async ({ page }) => {
    await page.goto('/');
    await page.waitForFunction(() => {
      const grid = document.getElementById('skillsGrid');
      return grid && grid.children.length > 0;
    }, { timeout: 10000 });

    await page.locator('#skillsGrid .skill-card').first().click();
    await expect(page.locator('#modalOverlay')).toHaveClass(/active/);

    // Click the overlay (not the modal content)
    await page.locator('#modalOverlay').click({ position: { x: 10, y: 10 } });
    await expect(page.locator('#modalOverlay')).not.toHaveClass(/active/);
  });
});

test.describe('Install Section', () => {
  test('shows real git clone command', async ({ page }) => {
    await page.goto('/');
    const installCode = page.locator('#install .install-cmd code').first();
    await expect(installCode).toContainText('git clone');
    await expect(installCode).toContainText('jiayaoqijia/cryptoskill');
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
