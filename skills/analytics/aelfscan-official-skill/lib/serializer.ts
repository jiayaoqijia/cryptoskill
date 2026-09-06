function pushQueryPart(parts: string[], key: string, value: unknown): void {
  if (value === undefined || value === null) {
    return;
  }

  if (value === '') {
    parts.push(`${key}=`);
    return;
  }

  parts.push(`${key}=${encodeURIComponent(String(value))}`);
}

function processObject(parts: string[], source: Record<string, unknown>, prefix?: string, isObjectItem = false): void {
  Object.keys(source).forEach((key) => {
    const value = source[key];
    const prefixedKey = prefix ? (isObjectItem ? `${prefix}.${key}` : `${prefix}[${key}]`) : key;

    if (Array.isArray(value)) {
      value.forEach((item, index) => {
        if (item && typeof item === 'object') {
          processObject(parts, item as Record<string, unknown>, `${prefixedKey}[${index}]`, true);
        } else {
          pushQueryPart(parts, `${prefixedKey}[${index}]`, item);
        }
      });
      return;
    }

    if (value && typeof value === 'object') {
      processObject(parts, value as Record<string, unknown>, prefixedKey, false);
      return;
    }

    if (value === undefined || value === null) {
      return;
    }

    if (typeof value === 'number' && Number.isNaN(value)) {
      return;
    }

    // Primitive values reach here after null/undefined/object filtering.
    pushQueryPart(parts, prefixedKey, value);
  });
}

export function serializeQuery(params?: Record<string, unknown>): string {
  if (!params) {
    return '';
  }

  const keys = Object.keys(params);
  if (keys.length === 0) {
    return '';
  }

  const parts: string[] = [];
  processObject(parts, params);

  if (parts.length === 0) {
    return '';
  }

  return parts.join('&');
}
