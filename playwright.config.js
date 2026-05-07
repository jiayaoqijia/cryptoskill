const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:8082',
    headless: true,
  },
  webServer: {
    command: 'python3 scripts/generate-pages.py --serve 8082',
    port: 8082,
    reuseExistingServer: false,
  },
});
