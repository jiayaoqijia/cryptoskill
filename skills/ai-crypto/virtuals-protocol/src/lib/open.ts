// =============================================================================
// Open a URL in the user's default browser. Platform-specific, no dependencies.
// =============================================================================

import { exec } from "child_process";

export function openUrl(url: string): void {
  const platform = process.platform;
  let cmd: string;

  if (platform === "darwin") {
    cmd = `open "${url}"`;
  } else if (platform === "win32") {
    cmd = `start "" "${url}"`;
  } else {
    // Linux / others
    cmd = `xdg-open "${url}"`;
  }

  exec(cmd, (err) => {
    if (err) {
      // Silently fail — the URL is always printed as fallback
    }
  });
}
