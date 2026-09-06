const ADDRESS_WITH_PREFIX = /^(?:ELF_)?(.+?)(?:_[^_]+)?$/;

export function normalizeChainId(input?: string): string {
  if (!input) {
    return '';
  }

  const trimmed = input.trim();
  if (!trimmed) {
    return '';
  }

  if (trimmed === 'multiChain') {
    return '';
  }

  return trimmed;
}

export function normalizeAddress(input?: string): string {
  if (!input) {
    return '';
  }

  const trimmed = input.trim();
  if (!trimmed) {
    return '';
  }

  const match = trimmed.match(ADDRESS_WITH_PREFIX);
  if (!match || !match[1]) {
    return trimmed;
  }

  return match[1];
}
