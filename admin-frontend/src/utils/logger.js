// src/utils/logger.js
const isDev = import.meta.env.DEV;

const SENSITIVE_KEYS = [
  'password', 'access', 'refresh', 'token',
  'authorization', 'secret', 'api_token', 'otp', 'credential',
];

function isSensitive(key) {
  const k = String(key).toLowerCase();
  return SENSITIVE_KEYS.some((s) => k.includes(s));
}

function mask(value, depth = 0) {
  if (depth > 4) return '[deep]';
  if (value === null || value === undefined) return value;
  if (typeof value !== 'object') return value;
  if (value instanceof Error) return { name: value.name, message: value.message };
  if (Array.isArray(value)) return value.map((v) => mask(v, depth + 1));
  const out = {};
  for (const [k, v] of Object.entries(value)) {
    if (isSensitive(k)) out[k] = '***';
    else if (typeof v === 'object') out[k] = mask(v, depth + 1);
    else out[k] = v;
  }
  return out;
}

const safeArgs = (args) => args.map((a) => (typeof a === 'object' && a !== null ? mask(a) : a));

export const logger = {
  log: (...args) => { if (isDev) console.log(...safeArgs(args)); },
  info: (...args) => { if (isDev) console.info(...safeArgs(args)); },
  warn: (...args) => { if (isDev) console.warn(...safeArgs(args)); },
  error: (...args) => { if (isDev) console.error(...safeArgs(args)); },
};

export default logger;