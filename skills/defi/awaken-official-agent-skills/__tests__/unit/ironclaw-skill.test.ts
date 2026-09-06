import { describe, expect, test } from 'bun:test';
import { fileURLToPath } from 'url';
import packageJson from '../../package.json';

function getSkillParts() {
  const skillPath = fileURLToPath(new URL('../../SKILL.md', import.meta.url));
  const raw = Bun.file(skillPath).text();
  return raw.then(content => {
    const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (!match) {
      throw new Error('SKILL.md is missing YAML frontmatter');
    }
    return {
      frontmatter: match[1],
      body: match[2],
    };
  });
}

function getActivationList(frontmatter: string, key: string): string[] {
  const lines = frontmatter.split('\n');
  const results: string[] = [];
  let inActivation = false;
  let capture = false;

  for (const line of lines) {
    if (!inActivation) {
      if (line.trim() === 'activation:') {
        inActivation = true;
      }
      continue;
    }

    if (/^\S/.test(line)) {
      break;
    }

    if (new RegExp(`^  ${key}:\\s*$`).test(line)) {
      capture = true;
      continue;
    }

    if (capture && /^  [a-zA-Z_]/.test(line)) {
      break;
    }

    if (!capture) {
      continue;
    }

    const item = line.match(/^    -\s*(.+)$/);
    if (item) {
      results.push(item[1].trim().replace(/^['"]|['"]$/g, ''));
    }
  }

  return results;
}

function getActivationNumber(frontmatter: string, key: string): number | null {
  const match = frontmatter.match(new RegExp(`^  ${key}:\\s*(\\d+)$`, 'm'));
  return match ? Number(match[1]) : null;
}

describe('IronClaw skill prompt', () => {
  test('includes versioned frontmatter that matches package version', async () => {
    const { frontmatter } = await getSkillParts();
    expect(frontmatter).toContain('name: "awaken-agent-skills"');
    expect(frontmatter).toContain(`version: "${packageJson.version}"`);
    expect(frontmatter).toContain('activation:');
  });

  test('defines activation keywords, exclusions, and tags for IronClaw routing', async () => {
    const { frontmatter } = await getSkillParts();
    const keywords = getActivationList(frontmatter, 'keywords');
    const excludeKeywords = getActivationList(frontmatter, 'exclude_keywords');
    const tags = getActivationList(frontmatter, 'tags');

    expect(keywords).toEqual(
      expect.arrayContaining(['dex', 'swap', 'liquidity', 'quote', 'kline', 'awaken']),
    );
    expect(excludeKeywords).toEqual(
      expect.arrayContaining(['guardian', 'recovery', 'dao', 'nft mint', 'wallet create']),
    );
    expect(tags).toEqual(expect.arrayContaining(['dex', 'defi', 'aelf', 'awaken']));
    expect(getActivationNumber(frontmatter, 'max_context_tokens')).toBe(1800);
  });

  test('documents DEX routing and write confirmation rules', async () => {
    const { body } = await getSkillParts();
    expect(body).toContain('Default to this skill for DEX, swap, liquidity');
    expect(body).toContain('For write operations, require explicit user confirmation');
    expect(body).toContain('Install into IronClaw');
    expect(body).toContain('Do not use this skill for guardian, recovery, DAO governance');
  });
});
