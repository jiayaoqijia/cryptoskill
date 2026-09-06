export interface TruncationMeta {
  truncated: boolean;
  maxItems: number;
  maxChars: number;
  originalSizeEstimate: number;
}

export interface OutputGovernanceOptions {
  maxItems: number;
  maxChars: number;
  includeRaw: boolean;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function summarizeValue(value: unknown): Record<string, unknown> {
  if (Array.isArray(value)) {
    return {
      type: 'array',
      length: value.length,
      preview: value.slice(0, 3),
    };
  }

  if (isRecord(value)) {
    const keys = Object.keys(value);
    return {
      type: 'object',
      keys,
      keyCount: keys.length,
    };
  }

  return {
    type: typeof value,
    value,
  };
}

function truncateArrays(value: unknown, maxItems: number): { value: unknown; truncated: boolean } {
  if (Array.isArray(value)) {
    const truncatedItems = value.slice(0, maxItems).map(item => truncateArrays(item, maxItems));
    const wasTruncated = value.length > maxItems || truncatedItems.some(item => item.truncated);

    return {
      value: truncatedItems.map(item => item.value),
      truncated: wasTruncated,
    };
  }

  if (isRecord(value)) {
    let truncated = false;
    const next: Record<string, unknown> = {};

    for (const [key, itemValue] of Object.entries(value)) {
      const child = truncateArrays(itemValue, maxItems);
      if (child.truncated) {
        truncated = true;
      }
      next[key] = child.value;
    }

    return {
      value: next,
      truncated,
    };
  }

  return {
    value,
    truncated: false,
  };
}

function stripRawByConfig(value: unknown, includeRaw: boolean): unknown {
  if (includeRaw) {
    return value;
  }

  if (!isRecord(value)) {
    return value;
  }

  const next = { ...value };
  delete next.raw;
  return next;
}

function attachMeta(value: unknown, meta: TruncationMeta): unknown {
  if (isRecord(value)) {
    return {
      ...value,
      meta,
    };
  }

  return {
    data: value,
    meta,
  };
}

function safeSerialize(value: unknown): string {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return JSON.stringify({ data: summarizeValue(value) }, null, 2);
  }
}

function shrinkForMaxChars(value: unknown, meta: TruncationMeta): unknown {
  if (isRecord(value)) {
    return {
      success: value.success,
      traceId: value.traceId,
      dataSummary: summarizeValue(value.data),
      error: value.error,
      meta,
    };
  }

  return {
    dataSummary: summarizeValue(value),
    meta,
  };
}

export function applyOutputGovernance(
  value: unknown,
  options: OutputGovernanceOptions,
): { payload: unknown; serialized: string; meta: TruncationMeta } {
  const maxItems = Math.max(1, options.maxItems);
  const maxChars = Math.max(1, options.maxChars);
  const stripped = stripRawByConfig(value, options.includeRaw);
  const truncatedArrays = truncateArrays(stripped, maxItems);

  const initialMeta: TruncationMeta = {
    truncated: truncatedArrays.truncated,
    maxItems,
    maxChars,
    originalSizeEstimate: safeSerialize(truncatedArrays.value).length,
  };

  let payload = attachMeta(truncatedArrays.value, initialMeta);
  let serialized = safeSerialize(payload);

  if (serialized.length > maxChars) {
    const reducedMeta: TruncationMeta = {
      ...initialMeta,
      truncated: true,
    };

    payload = shrinkForMaxChars(truncatedArrays.value, reducedMeta);
    serialized = safeSerialize(payload);
    return { payload, serialized, meta: reducedMeta };
  }

  return { payload, serialized, meta: initialMeta };
}

export function applySummaryPolicy(
  value: unknown,
  maxItems: number,
): { value: unknown; truncated: boolean } {
  if (!isRecord(value) || !isRecord(value.data)) {
    return { value, truncated: false };
  }

  const data = value.data as Record<string, unknown>;
  const nextData = { ...data };
  let truncated = false;

  for (const key of ['list', 'items', 'blocks', 'transactions', 'logEvents']) {
    const item = nextData[key];
    if (Array.isArray(item) && item.length > maxItems) {
      nextData[key] = item.slice(0, maxItems);
      truncated = true;
    }
  }

  return {
    value: {
      ...value,
      data: nextData,
    },
    truncated,
  };
}
