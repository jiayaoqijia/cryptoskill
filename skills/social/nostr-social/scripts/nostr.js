#!/usr/bin/env node
/**
 * Nostr CLI - General purpose Nostr operations using nostr-tools
 * Wallet operations: use cocod (Cashu + Lightning)
 * 
 * Usage: node nostr.js <command> [args]
 */

import { SimplePool, useWebSocketImplementation } from 'nostr-tools/pool';
import { finalizeEvent, getPublicKey, verifyEvent } from 'nostr-tools/pure';
import * as nip04 from 'nostr-tools/nip04';
import * as nip05 from 'nostr-tools/nip05';
import * as nip19 from 'nostr-tools/nip19';
import WebSocket from 'ws';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { HDKey } from '@scure/bip32';
import { mnemonicToSeedSync } from '@scure/bip39';

useWebSocketImplementation(WebSocket);

// Config
const RELAYS = [
  'wss://relay.damus.io',
  'wss://nos.lol', 
  'wss://relay.primal.net',
  'wss://relay.snort.social',
  'wss://relay.nostr.band',
  'wss://purplepag.es',
  'wss://nostr.wine',
  'wss://relay.nostr.net'
];

// Hex utilities
function hexToBytes(hex) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
  }
  return bytes;
}

function bytesToHex(bytes) {
  return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Read content from stdin (for safe message passing without shell injection)
async function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        data += chunk;
      }
    });
    process.stdin.on('end', () => {
      resolve(data.trim());
    });
    // If stdin is a TTY (interactive), return empty immediately
    if (process.stdin.isTTY) {
      resolve('');
    }
  });
}

// Get content: from stdin if '-', otherwise from args
async function getContent(args, joinFrom = 0) {
  const content = args.slice(joinFrom).join(' ');
  if (content === '-' || content === '') {
    const stdinContent = await readStdin();
    if (stdinContent) return stdinContent;
    if (content === '-') throw new Error('No content provided via stdin');
  }
  return content;
}

// Config paths
const NOSTR_DIR = path.join(process.env.HOME, '.nostr');
const SECRET_KEY_FILE = path.join(NOSTR_DIR, 'secret.key');

// Check if configured
function isConfigured() {
  const paths = [
    SECRET_KEY_FILE,
    path.join(process.env.HOME, '.clawstr', 'secret.key'),
  ];
  for (const p of paths) {
    if (fs.existsSync(p)) return true;
  }
  return false;
}

// Load secret key
function loadSecretKey() {
  const paths = [
    SECRET_KEY_FILE,
    path.join(process.env.HOME, '.clawstr', 'secret.key'),
  ];
  for (const p of paths) {
    if (fs.existsSync(p)) {
      return hexToBytes(fs.readFileSync(p, 'utf8').trim());
    }
  }
  throw new Error('No secret key found. Run: node nostr.js init');
}

// Generate random secret key
function generateSecretKey() {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  return bytes;
}

// Derive Nostr key from mnemonic using NIP-06
function deriveKeyFromMnemonic(mnemonic) {
  const seed = mnemonicToSeedSync(mnemonic);
  const root = HDKey.fromMasterSeed(seed);
  const key = root.derive("m/44'/1237'/0'/0/0");
  // key.privateKey is 32 bytes
  return new Uint8Array(key.privateKey);
}

// Get cocod mnemonic if available
function getCocodMnemonic() {
  const configPath = path.join(process.env.HOME, '.cocod', 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.mnemonic;
    } catch {}
  }
  return null;
}

// Save secret key
function saveSecretKey(sk) {
  if (!fs.existsSync(NOSTR_DIR)) {
    fs.mkdirSync(NOSTR_DIR, { recursive: true });
  }
  fs.writeFileSync(SECRET_KEY_FILE, bytesToHex(sk));
  fs.chmodSync(SECRET_KEY_FILE, 0o600);
}

// INIT: Setup new identity
async function init(existingKey) {
  if (isConfigured()) {
    console.log('⚠️  Already configured. Current identity:');
    const sk = loadSecretKey();
    const pk = getPublicKey(sk);
    console.log(`  npub: ${nip19.npubEncode(pk)}`);
    console.log(`\nTo reset, delete ~/.nostr/secret.key and run init again.`);
    return;
  }
  
  let sk;
  let fromCocod = false;
  
  if (existingKey) {
    // Import existing key
    if (existingKey.startsWith('nsec1')) {
      const decoded = nip19.decode(existingKey);
      sk = decoded.data;
    } else if (/^[0-9a-f]{64}$/i.test(existingKey)) {
      sk = hexToBytes(existingKey);
    } else {
      throw new Error('Invalid key format. Provide nsec1... or 64-char hex.');
    }
    console.log('Importing existing key...');
  } else {
    // Check if cocod wallet exists - derive from its mnemonic for unified identity
    const mnemonic = getCocodMnemonic();
    if (mnemonic) {
      console.log('Found cocod wallet - deriving Nostr identity from wallet mnemonic (NIP-06)...');
      sk = deriveKeyFromMnemonic(mnemonic);
      fromCocod = true;
    } else {
      // Generate new key
      sk = generateSecretKey();
      console.log('Generating new Nostr identity...');
    }
  }
  
  saveSecretKey(sk);
  const pk = getPublicKey(sk);
  
  console.log('\n✅ Nostr identity configured!\n');
  console.log(`  Public Key: ${pk}`);
  console.log(`  npub: ${nip19.npubEncode(pk)}`);
  console.log(`\n  Key saved to: ${SECRET_KEY_FILE}`);
  
  if (fromCocod) {
    console.log('\n🔗 Identity derived from cocod wallet mnemonic.');
    console.log('   Your wallet mnemonic backs up BOTH wallet AND Nostr identity.');
    console.log('   NIP-05 via npubx.cash will match this identity.');
  } else {
    console.log('\n⚠️  BACKUP YOUR NSEC! If lost, your identity cannot be recovered.');
    console.log('\nNext steps:');
    console.log('  node nostr.js profile "Your Name" "Your bio"');
    console.log('  node nostr.js post "Hello Nostr!"');
    console.log('  cocod init    # Setup wallet for payments');
  }
}

// STATUS: Check configuration status
function status() {
  console.log('Nostr Skill Status\n');
  
  // Check key
  if (isConfigured()) {
    const sk = loadSecretKey();
    const pk = getPublicKey(sk);
    console.log('✅ Identity configured');
    console.log(`   npub: ${nip19.npubEncode(pk)}`);
  } else {
    console.log('❌ Identity not configured');
    console.log('   Run: node nostr.js init');
  }
  
  console.log('\nDefault relays:');
  RELAYS.forEach(r => console.log(`   ${r}`));
  
  console.log('\nWallet: use cocod for Cashu + Lightning');
  console.log('   cocod status     # Check wallet');
  console.log('   cocod balance    # Check balance');
}

const sk = loadSecretKey();
const pk = getPublicKey(sk);
const pool = new SimplePool();

// Resolve npub/nprofile/hex to hex pubkey
function resolvePubkey(input) {
  if (/^[0-9a-f]{64}$/i.test(input)) return input.toLowerCase();
  if (input.startsWith('npub1')) return nip19.decode(input).data;
  if (input.startsWith('nprofile1')) return nip19.decode(input).data.pubkey;
  throw new Error(`Invalid pubkey: ${input}`);
}

// Resolve note1/nevent1/hex to event id
function resolveEventId(input) {
  if (/^[0-9a-f]{64}$/i.test(input)) return input.toLowerCase();
  if (input.startsWith('note1')) return nip19.decode(input).data;
  if (input.startsWith('nevent1')) return nip19.decode(input).data.id;
  throw new Error(`Invalid event id: ${input}`);
}

// Parse nostr: mentions from content
function parseMentions(content) {
  const mentionRegex = /nostr:(npub1[a-z0-9]+|nprofile1[a-z0-9]+)/gi;
  const matches = content.match(mentionRegex) || [];
  const pubkeys = [];
  for (const m of matches) {
    try {
      pubkeys.push(resolvePubkey(m.replace('nostr:', '')));
    } catch {}
  }
  return [...new Set(pubkeys)];
}

// ============ COMMANDS ============

// POST: kind 1 note
async function post(content) {
  const mentions = parseMentions(content);
  const tags = mentions.map(p => ['p', p]);
  
  const event = finalizeEvent({
    kind: 1,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Posted: ${nip19.noteEncode(event.id)}`);
}

// REPLY: kind 1 reply
async function reply(eventRef, content) {
  const eventId = resolveEventId(eventRef);
  const original = await pool.get(RELAYS, { ids: [eventId] });
  if (!original) throw new Error('Event not found');
  
  const mentions = parseMentions(content);
  const tags = [
    ['e', eventId, RELAYS[0], 'root'],
    ['p', original.pubkey]
  ];
  for (const p of mentions) {
    if (!tags.some(t => t[0] === 'p' && t[1] === p)) {
      tags.push(['p', p]);
    }
  }
  
  const event = finalizeEvent({
    kind: 1,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Replied: ${nip19.noteEncode(event.id)}`);
}

// FOLLOW: kind 3 contact list
async function follow(pubkeyRef) {
  const targetPk = resolvePubkey(pubkeyRef);
  const existing = await pool.get(RELAYS, { kinds: [3], authors: [pk] });
  let tags = existing?.tags?.filter(t => t[0] === 'p') || [];
  
  if (tags.some(t => t[1] === targetPk)) {
    console.log('Already following');
    return;
  }
  
  tags.push(['p', targetPk]);
  const event = finalizeEvent({
    kind: 3,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: existing?.content || ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Followed: ${nip19.npubEncode(targetPk)}`);
}

// UNFOLLOW: kind 3 contact list  
async function unfollow(pubkeyRef) {
  const targetPk = resolvePubkey(pubkeyRef);
  const existing = await pool.get(RELAYS, { kinds: [3], authors: [pk] });
  if (!existing) throw new Error('No contact list found');
  
  const tags = existing.tags.filter(t => !(t[0] === 'p' && t[1] === targetPk));
  const event = finalizeEvent({
    kind: 3,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: existing.content || ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Unfollowed: ${nip19.npubEncode(targetPk)}`);
}

// DM: NIP-04 encrypted DM
async function dm(pubkeyRef, message) {
  const targetPk = resolvePubkey(pubkeyRef);
  const ciphertext = await nip04.encrypt(bytesToHex(sk), targetPk, message);
  
  const event = finalizeEvent({
    kind: 4,
    created_at: Math.floor(Date.now() / 1000),
    tags: [['p', targetPk]],
    content: ciphertext
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ DM sent to ${nip19.npubEncode(targetPk)}`);
}

// READ DMS: NIP-04 encrypted DMs
async function readDms(limit = 10) {
  const events = await pool.querySync(RELAYS, [
    { kinds: [4], authors: [pk], limit },
    { kinds: [4], '#p': [pk], limit }
  ]);
  
  events.sort((a, b) => b.created_at - a.created_at);
  console.log(`📨 DMs (${events.length}):\n`);
  
  for (const e of events.slice(0, limit)) {
    const isFromMe = e.pubkey === pk;
    const otherPk = isFromMe ? e.tags.find(t => t[0] === 'p')?.[1] : e.pubkey;
    
    try {
      const plaintext = await nip04.decrypt(bytesToHex(sk), otherPk, e.content);
      const date = new Date(e.created_at * 1000).toLocaleString();
      const dir = isFromMe ? '→' : '←';
      console.log(`${dir} ${nip19.npubEncode(otherPk).slice(0, 16)}... • ${date}`);
      console.log(`  ${plaintext}\n`);
    } catch {
      console.log(`[Failed to decrypt]\n`);
    }
  }
}

// ZAP: NIP-57 - generates invoice, pay with cocod
async function zap(pubkeyRef, amount, comment = '') {
  const targetPk = resolvePubkey(pubkeyRef);
  
  // Get profile for lud16
  const profile = await pool.get(RELAYS, { kinds: [0], authors: [targetPk] });
  if (!profile) throw new Error('Profile not found');
  
  const metadata = JSON.parse(profile.content);
  if (!metadata.lud16) throw new Error('No Lightning address in profile');
  
  // Get LNURL endpoint
  const [name, domain] = metadata.lud16.split('@');
  const lnurlEndpoint = `https://${domain}/.well-known/lnurlp/${name}`;
  const lnurlRes = await fetch(lnurlEndpoint);
  const lnurlInfo = await lnurlRes.json();
  
  if (!lnurlInfo.allowsNostr) throw new Error('Does not support Nostr zaps');
  
  // Create zap request
  const zapRequest = finalizeEvent({
    kind: 9734,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['relays', ...RELAYS],
      ['amount', String(amount * 1000)],
      ['p', targetPk]
    ],
    content: comment
  }, sk);
  
  // Get invoice
  const callbackUrl = new URL(lnurlInfo.callback);
  callbackUrl.searchParams.set('amount', String(amount * 1000));
  callbackUrl.searchParams.set('nostr', JSON.stringify(zapRequest));
  
  const invoiceRes = await fetch(callbackUrl.toString());
  const { pr } = await invoiceRes.json();
  
  if (!pr) throw new Error('No invoice returned');
  
  console.log(`⚡ Zap ${amount} sats to ${metadata.lud16}\n`);
  console.log(`Invoice: ${pr}\n`);
  console.log(`To pay: cocod send bolt11 ${pr}`);
}

// MENTIONS: check mentions/replies
async function mentions(limit = 20) {
  const events = await pool.querySync(RELAYS, { kinds: [1], '#p': [pk], limit });
  events.sort((a, b) => b.created_at - a.created_at);
  
  console.log(`📬 Mentions (${events.length}):\n`);
  for (const e of events.slice(0, limit)) {
    const date = new Date(e.created_at * 1000).toLocaleString();
    const preview = e.content.slice(0, 100) + (e.content.length > 100 ? '...' : '');
    console.log(`${nip19.npubEncode(e.pubkey).slice(0, 16)}... • ${date}`);
    console.log(`  ${preview}`);
    console.log(`  ID: ${nip19.noteEncode(e.id)}\n`);
  }
}

// SHOW: display full content of a note
async function show(noteId) {
  if (!noteId) {
    console.log('Usage: show <note1...>');
    return;
  }
  
  let eventId;
  try {
    if (noteId.startsWith('note1')) {
      const decoded = nip19.decode(noteId);
      eventId = decoded.data;
    } else if (noteId.startsWith('nevent1')) {
      const decoded = nip19.decode(noteId);
      eventId = decoded.data.id;
    } else {
      eventId = noteId; // assume hex
    }
  } catch (e) {
    console.log('Invalid note ID');
    return;
  }
  
  const event = await pool.get(RELAYS, { ids: [eventId] });
  
  if (!event) {
    console.log('Note not found');
    return;
  }
  
  const date = new Date(event.created_at * 1000).toLocaleString();
  const npub = nip19.npubEncode(event.pubkey);
  
  console.log(`📝 Note by ${npub}`);
  console.log(`   ${date}\n`);
  console.log(event.content);
  console.log(`\n---`);
  console.log(`ID: ${nip19.noteEncode(event.id)}`);
  
  // Show reply context if it's a reply
  const replyTag = event.tags.find(t => t[0] === 'e' && t[3] === 'reply');
  const rootTag = event.tags.find(t => t[0] === 'e' && t[3] === 'root');
  if (replyTag || rootTag) {
    console.log(`Reply to: ${nip19.noteEncode(replyTag?.at(1) || rootTag?.at(1))}`);
  }
}

// FEED: get feed from follows
async function feed(limit = 20) {
  const contactList = await pool.get(RELAYS, { kinds: [3], authors: [pk] });
  const follows = contactList?.tags?.filter(t => t[0] === 'p').map(t => t[1]) || [];
  
  if (follows.length === 0) {
    console.log('Not following anyone');
    return;
  }
  
  const events = await pool.querySync(RELAYS, { kinds: [1], authors: follows, limit });
  events.sort((a, b) => b.created_at - a.created_at);
  
  console.log(`📰 Feed (${events.length} posts from ${follows.length} follows):\n`);
  for (const e of events.slice(0, limit)) {
    const date = new Date(e.created_at * 1000).toLocaleString();
    const preview = e.content.slice(0, 150) + (e.content.length > 150 ? '...' : '');
    console.log(`${nip19.npubEncode(e.pubkey).slice(0, 16)}... • ${date}`);
    console.log(`  ${preview}`);
    console.log(`  ${nip19.noteEncode(e.id)}\n`);
  }
}

// PROFILE: get/set profile (kind 0)
async function profile(name, about) {
  if (!name) {
    // Get profile
    const p = await pool.get(RELAYS, { kinds: [0], authors: [pk] });
    if (p) {
      const meta = JSON.parse(p.content);
      console.log('Profile:');
      console.log(`  Name: ${meta.name || '-'}`);
      console.log(`  About: ${meta.about || '-'}`);
      console.log(`  NIP-05: ${meta.nip05 || '-'}`);
      console.log(`  Lightning: ${meta.lud16 || '-'}`);
      console.log(`  Picture: ${meta.picture || '-'}`);
      console.log(`  Banner: ${meta.banner || '-'}`);
    } else {
      console.log('No profile found');
    }
    return;
  }
  
  // Set profile
  const existing = await pool.get(RELAYS, { kinds: [0], authors: [pk] });
  const meta = existing ? JSON.parse(existing.content) : {};
  meta.name = name;
  if (about) meta.about = about;
  
  const event = finalizeEvent({
    kind: 0,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content: JSON.stringify(meta)
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Profile updated`);
}

// PROFILE-SET: set specific profile fields (JSON)
async function profileSet(jsonStr) {
  const updates = JSON.parse(jsonStr);
  const existing = await pool.get(RELAYS, { kinds: [0], authors: [pk] });
  const meta = existing ? JSON.parse(existing.content) : {};
  
  // Merge updates
  for (const [key, value] of Object.entries(updates)) {
    if (value === null || value === '') {
      delete meta[key];
    } else {
      meta[key] = value;
    }
  }
  
  const event = finalizeEvent({
    kind: 0,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content: JSON.stringify(meta)
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Profile updated`);
  console.log(JSON.stringify(meta, null, 2));
}

// LOOKUP: NIP-05 lookup
async function lookup(nip05Addr) {
  const result = await nip05.queryProfile(nip05Addr);
  if (result) {
    console.log(`NIP-05: ${nip05Addr}`);
    console.log(`Pubkey: ${result.pubkey}`);
    console.log(`npub: ${nip19.npubEncode(result.pubkey)}`);
    console.log(`Relays: ${result.relays?.join(', ') || 'none'}`);
  } else {
    console.log('Not found');
  }
}

// REACT: reaction (kind 7)
async function react(eventRef, emoji = '🤙') {
  const eventId = resolveEventId(eventRef);
  const original = await pool.get(RELAYS, { ids: [eventId] });
  if (!original) throw new Error('Event not found');
  
  const event = finalizeEvent({
    kind: 7,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['e', eventId],
      ['p', original.pubkey]
    ],
    content: emoji
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Reacted: ${emoji}`);
}

// REPOST: kind 6 (NIP-18)
async function repost(eventRef) {
  const eventId = resolveEventId(eventRef);
  const original = await pool.get(RELAYS, { ids: [eventId] });
  if (!original) throw new Error('Event not found');
  
  const event = finalizeEvent({
    kind: 6,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['e', eventId, RELAYS[0]],
      ['p', original.pubkey]
    ],
    content: JSON.stringify(original)
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Reposted: ${nip19.noteEncode(eventId)}`);
}

// DELETE: kind 5
async function deleteEvent(eventRef) {
  const eventId = resolveEventId(eventRef);
  
  const event = finalizeEvent({
    kind: 5,
    created_at: Math.floor(Date.now() / 1000),
    tags: [['e', eventId]],
    content: 'deleted'
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Deleted: ${nip19.noteEncode(eventId)}`);
}

// MUTE: kind 10000 (add to mute list)
async function mute(pubkeyRef) {
  const targetPk = resolvePubkey(pubkeyRef);
  
  // Get existing mute list
  const existing = await pool.get(RELAYS, { kinds: [10000], authors: [pk] });
  let tags = existing?.tags || [];
  
  // Check if already muted
  if (tags.some(t => t[0] === 'p' && t[1] === targetPk)) {
    console.log('Already muted');
    return;
  }
  
  tags.push(['p', targetPk]);
  
  const event = finalizeEvent({
    kind: 10000,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: existing?.content || ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Muted: ${nip19.npubEncode(targetPk)}`);
}

// UNMUTE: remove from kind 10000
async function unmute(pubkeyRef) {
  const targetPk = resolvePubkey(pubkeyRef);
  
  const existing = await pool.get(RELAYS, { kinds: [10000], authors: [pk] });
  if (!existing) {
    console.log('No mute list found');
    return;
  }
  
  const tags = existing.tags.filter(t => !(t[0] === 'p' && t[1] === targetPk));
  
  const event = finalizeEvent({
    kind: 10000,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: existing.content || ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Unmuted: ${nip19.npubEncode(targetPk)}`);
}

// BOOKMARK: kind 10003
async function bookmark(eventRef) {
  const eventId = resolveEventId(eventRef);
  
  // Get existing bookmarks
  const existing = await pool.get(RELAYS, { kinds: [10003], authors: [pk] });
  let tags = existing?.tags || [];
  
  // Check if already bookmarked
  if (tags.some(t => t[0] === 'e' && t[1] === eventId)) {
    console.log('Already bookmarked');
    return;
  }
  
  tags.push(['e', eventId]);
  
  const event = finalizeEvent({
    kind: 10003,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Bookmarked: ${nip19.noteEncode(eventId)}`);
}

// UNBOOKMARK: remove from kind 10003
async function unbookmark(eventRef) {
  const eventId = resolveEventId(eventRef);
  
  const existing = await pool.get(RELAYS, { kinds: [10003], authors: [pk] });
  if (!existing) {
    console.log('No bookmarks found');
    return;
  }
  
  const tags = existing.tags.filter(t => !(t[0] === 'e' && t[1] === eventId));
  
  const event = finalizeEvent({
    kind: 10003,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Unbookmarked: ${nip19.noteEncode(eventId)}`);
}

// BOOKMARKS: list bookmarks
async function listBookmarks() {
  const existing = await pool.get(RELAYS, { kinds: [10003], authors: [pk] });
  if (!existing || existing.tags.length === 0) {
    console.log('No bookmarks');
    return;
  }
  
  const eventIds = existing.tags.filter(t => t[0] === 'e').map(t => t[1]);
  console.log(`📑 Bookmarks (${eventIds.length}):\n`);
  
  for (const id of eventIds) {
    const event = await pool.get(RELAYS, { ids: [id] });
    if (event) {
      const preview = event.content.slice(0, 80) + (event.content.length > 80 ? '...' : '');
      console.log(`${nip19.noteEncode(id)}`);
      console.log(`  ${preview}\n`);
    } else {
      console.log(`${nip19.noteEncode(id)} [not found]\n`);
    }
  }
}

// RELAYS: manage relay list (NIP-65, kind 10002)
async function listRelays() {
  const existing = await pool.get(RELAYS, { kinds: [10002], authors: [pk] });
  if (!existing) {
    console.log('No relay list published. Using defaults:');
    RELAYS.forEach(r => console.log(`  ${r}`));
    return;
  }
  
  console.log('📡 Your relay list:\n');
  for (const tag of existing.tags) {
    if (tag[0] === 'r') {
      const mode = tag[2] || 'read+write';
      console.log(`  ${tag[1]} (${mode})`);
    }
  }
}

async function addRelay(relayUrl, mode = '') {
  const existing = await pool.get(RELAYS, { kinds: [10002], authors: [pk] });
  let tags = existing?.tags?.filter(t => t[0] === 'r') || [];
  
  // Remove if exists, then add
  tags = tags.filter(t => t[1] !== relayUrl);
  const newTag = mode ? ['r', relayUrl, mode] : ['r', relayUrl];
  tags.push(newTag);
  
  const event = finalizeEvent({
    kind: 10002,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Added relay: ${relayUrl}${mode ? ` (${mode})` : ''}`);
}

async function removeRelay(relayUrl) {
  const existing = await pool.get(RELAYS, { kinds: [10002], authors: [pk] });
  if (!existing) {
    console.log('No relay list found');
    return;
  }
  
  const tags = existing.tags.filter(t => !(t[0] === 'r' && t[1] === relayUrl));
  
  const event = finalizeEvent({
    kind: 10002,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Removed relay: ${relayUrl}`);
}

// CHANNELS: public chat (NIP-28)
async function createChannel(name, about = '', picture = '') {
  const metadata = { name, about, picture };
  
  const event = finalizeEvent({
    kind: 40,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content: JSON.stringify(metadata)
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Channel created: ${name}`);
  console.log(`  ID: ${event.id}`);
}

async function channelPost(channelId, message) {
  const event = finalizeEvent({
    kind: 42,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['e', channelId, RELAYS[0], 'root']
    ],
    content: message
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Posted to channel`);
}

async function channelMessages(channelId, limit = 20) {
  const events = await pool.querySync(RELAYS, {
    kinds: [42],
    '#e': [channelId],
    limit
  });
  
  events.sort((a, b) => a.created_at - b.created_at);
  console.log(`💬 Channel messages (${events.length}):\n`);
  
  for (const e of events) {
    const date = new Date(e.created_at * 1000).toLocaleString();
    console.log(`${nip19.npubEncode(e.pubkey).slice(0, 12)}... • ${date}`);
    console.log(`  ${e.content}\n`);
  }
}

// BADGES: NIP-58
async function listBadges() {
  // Get badges awarded to us (kind 8)
  const awards = await pool.querySync(RELAYS, {
    kinds: [8],
    '#p': [pk],
    limit: 50
  });
  
  if (awards.length === 0) {
    console.log('No badges awarded');
    return;
  }
  
  console.log(`🏅 Badges (${awards.length}):\n`);
  
  for (const award of awards) {
    const badgeTag = award.tags.find(t => t[0] === 'a');
    if (badgeTag) {
      // Fetch badge definition
      const [kind, pubkey, identifier] = badgeTag[1].split(':');
      const badgeDef = await pool.get(RELAYS, {
        kinds: [30009],
        authors: [pubkey],
        '#d': [identifier]
      });
      
      if (badgeDef) {
        const meta = JSON.parse(badgeDef.content || '{}');
        const name = badgeDef.tags.find(t => t[0] === 'name')?.[1] || identifier;
        const desc = badgeDef.tags.find(t => t[0] === 'description')?.[1] || '';
        console.log(`  ${name}`);
        if (desc) console.log(`    ${desc}`);
        console.log(`    From: ${nip19.npubEncode(pubkey).slice(0, 16)}...\n`);
      } else {
        console.log(`  ${badgeTag[1]}\n`);
      }
    }
  }
}

async function createBadge(identifier, name, description = '', imageUrl = '') {
  const tags = [
    ['d', identifier],
    ['name', name]
  ];
  if (description) tags.push(['description', description]);
  if (imageUrl) tags.push(['image', imageUrl]);
  
  const event = finalizeEvent({
    kind: 30009,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Badge created: ${name}`);
  console.log(`  ID: 30009:${pk}:${identifier}`);
}

async function awardBadge(badgeId, recipientPubkey) {
  const targetPk = resolvePubkey(recipientPubkey);
  
  const event = finalizeEvent({
    kind: 8,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['a', badgeId],
      ['p', targetPk]
    ],
    content: ''
  }, sk);
  
  await Promise.any(pool.publish(RELAYS, event));
  console.log(`✅ Badge awarded to ${nip19.npubEncode(targetPk)}`);
}

// WHOAMI
function whoami() {
  console.log(`Pubkey: ${pk}`);
  console.log(`npub: ${nip19.npubEncode(pk)}`);
}

// ============ AUTORESPONSE STATE MANAGEMENT ============

const DEFAULT_STATE_FILE = path.join(process.env.HOME, '.openclaw/workspace/memory/nostr-autoresponse-state.json');

// Agent's own pubkey for WoT lookup (automatically detected from identity)

function loadAutoResponseState(stateFile = DEFAULT_STATE_FILE) {
  try {
    return JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  } catch {
    return {
      version: 1,
      lastCheck: null,
      responseCount: { hour: 0, hourStart: null },
      responded: {},
      ignored: {}
    };
  }
}

function saveAutoResponseState(state, stateFile = DEFAULT_STATE_FILE) {
  state.lastCheck = Math.floor(Date.now() / 1000);
  const dir = path.dirname(stateFile);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
}

// Get WoT (owner's follow list from agent profile)
async function getWoT() {
  // Get agent's profile to extract owner's npub
  const profile = await pool.get(RELAYS, { kinds: [0], authors: [pk] });
  let ownerPubkey = pk; // fallback to agent if no owner found
  
  if (profile?.content) {
    try {
      const profileData = JSON.parse(profile.content);
      // Look for owner's npub in profile (stored during setup)
      if (profileData.about && profileData.about.includes('nostr:npub1')) {
        const npubMatch = profileData.about.match(/nostr:(npub1[a-zA-Z0-9]+)/);
        if (npubMatch) {
          const { type, data } = nip19.decode(npubMatch[1]);
          if (type === 'npub') {
            ownerPubkey = data;
          }
        }
      }
    } catch (e) {
      console.error('Error parsing profile for owner pubkey:', e);
    }
  }
  
  // Get owner's contact list (their follows = our WoT)
  const contactList = await pool.get(RELAYS, { kinds: [3], authors: [ownerPubkey] });
  const follows = new Set(contactList?.tags?.filter(t => t[0] === 'p').map(t => t[1]) || []);
  
  // Always include owner and agent in WoT
  follows.add(ownerPubkey);
  follows.add(pk);
  
  return follows;
}

// Check if content looks like a question or needs response
function needsResponse(content) {
  // Skip very short messages (gm, gn, lol, etc.)
  if (content.trim().length < 5) return false;
  
  // Skip if just emojis
  if (/^[\p{Emoji}\s]+$/u.test(content.trim())) return false;
  
  // Question patterns
  const questionPatterns = [
    /\?/,
    /^(what|how|why|when|where|who|can|could|would|should|is|are|do|does|did|will|have|has)/i,
    /tell me|explain|describe|help|thoughts on/i
  ];
  
  if (questionPatterns.some(p => p.test(content))) return true;
  
  // Direct address patterns
  if (/@nash|nash,|hey nash/i.test(content)) return true;
  
  // Default: if it's substantial (>20 chars), consider it for response
  return content.trim().length > 20;
}

// PENDING-MENTIONS: Get unprocessed mentions from WoT
async function pendingMentions(stateFile = DEFAULT_STATE_FILE, limit = 15) {
  const state = loadAutoResponseState(stateFile);
  const wot = await getWoT();
  
  // Fetch mentions
  const events = await pool.querySync(RELAYS, { kinds: [1], '#p': [pk], limit: limit * 2 });
  events.sort((a, b) => b.created_at - a.created_at);
  
  // Filter to pending (not responded, not ignored, in WoT)
  const pending = [];
  const skipped = { notWoT: 0, alreadyHandled: 0 };
  
  for (const e of events.slice(0, limit * 2)) {
    const noteId = nip19.noteEncode(e.id);
    
    // Skip if already handled
    if (state.responded[noteId] || state.ignored[noteId]) {
      skipped.alreadyHandled++;
      continue;
    }
    
    // Skip if not in WoT
    if (!wot.has(e.pubkey)) {
      skipped.notWoT++;
      continue;
    }
    
    // Check if it needs a response
    const needs = needsResponse(e.content);
    
    pending.push({
      id: e.id,
      noteId,
      pubkey: e.pubkey,
      npub: nip19.npubEncode(e.pubkey),
      content: e.content,
      created_at: e.created_at,
      needsResponse: needs,
      isQuestion: /\?/.test(e.content)
    });
    
    if (pending.length >= limit) break;
  }
  
  // Output as JSON for easy parsing
  const output = {
    pending: pending.length,
    skipped,
    wotSize: wot.size,
    lastCheck: state.lastCheck,
    mentions: pending
  };
  
  console.log(JSON.stringify(output, null, 2));
}

// MARK-RESPONDED: Mark a mention as responded
async function markResponded(noteRef, responseNoteId = null, stateFile = DEFAULT_STATE_FILE) {
  const noteId = noteRef.startsWith('note1') ? noteRef : nip19.noteEncode(resolveEventId(noteRef));
  const state = loadAutoResponseState(stateFile);
  
  state.responded[noteId] = {
    at: Math.floor(Date.now() / 1000),
    responseId: responseNoteId
  };
  
  // Update hourly rate limit counter
  const now = Math.floor(Date.now() / 1000);
  const hourAgo = now - 3600;
  if (!state.responseCount.hourStart || state.responseCount.hourStart < hourAgo) {
    state.responseCount = { hour: 1, hourStart: now };
  } else {
    state.responseCount.hour++;
  }
  
  saveAutoResponseState(state, stateFile);
  console.log(`✅ Marked responded: ${noteId}`);
  if (responseNoteId) console.log(`   Response: ${responseNoteId}`);
}

// MARK-IGNORED: Mark a mention as ignored (no response needed)
async function markIgnored(noteRef, reason = 'no_response_needed', stateFile = DEFAULT_STATE_FILE) {
  const noteId = noteRef.startsWith('note1') ? noteRef : nip19.noteEncode(resolveEventId(noteRef));
  const state = loadAutoResponseState(stateFile);
  
  state.ignored[noteId] = {
    at: Math.floor(Date.now() / 1000),
    reason
  };
  
  saveAutoResponseState(state, stateFile);
  console.log(`✅ Marked ignored: ${noteId} (${reason})`);
}

// RATE-LIMIT-CHECK: Check if we can respond (max 10/hour)
function checkRateLimit(stateFile = DEFAULT_STATE_FILE) {
  const state = loadAutoResponseState(stateFile);
  const now = Math.floor(Date.now() / 1000);
  const hourAgo = now - 3600;
  
  if (!state.responseCount.hourStart || state.responseCount.hourStart < hourAgo) {
    console.log(JSON.stringify({ allowed: true, remaining: 10 }));
    return true;
  }
  
  const remaining = 10 - state.responseCount.hour;
  console.log(JSON.stringify({ allowed: remaining > 0, remaining: Math.max(0, remaining) }));
  return remaining > 0;
}

// AUTORESPONSE-STATUS: Show current state summary
async function autoResponseStatus(stateFile = DEFAULT_STATE_FILE) {
  const state = loadAutoResponseState(stateFile);
  const wot = await getWoT();
  
  const now = Math.floor(Date.now() / 1000);
  const hourAgo = now - 3600;
  
  let hourlyCount = 0;
  if (state.responseCount.hourStart && state.responseCount.hourStart >= hourAgo) {
    hourlyCount = state.responseCount.hour;
  }
  
  const summary = {
    lastCheck: state.lastCheck ? new Date(state.lastCheck * 1000).toISOString() : null,
    wotSize: wot.size,
    responded: Object.keys(state.responded).length,
    ignored: Object.keys(state.ignored).length,
    hourlyResponses: hourlyCount,
    hourlyLimit: 10,
    canRespond: hourlyCount < 10
  };
  
  console.log(JSON.stringify(summary, null, 2));
}

// ============ MAIN ============

const [,, cmd, ...args] = process.argv;

// Commands that don't require a key
if (cmd === 'init') {
  await init(args[0]);
  process.exit(0);
}
if (cmd === 'status') {
  status();
  process.exit(0);
}

// Check if configured for all other commands
if (!isConfigured() && cmd && cmd !== 'help') {
  console.log('❌ Nostr not configured.\n');
  console.log('Run setup:');
  console.log('  node nostr.js init              # Generate new identity');
  console.log('  node nostr.js init <nsec>       # Import existing key');
  console.log('  node nostr.js init <hex-key>    # Import hex private key');
  process.exit(1);
}

try {
  switch (cmd) {
    // Content commands support stdin: echo "message" | node nostr.js post -
    case 'post': await post(await getContent(args)); break;
    case 'reply': await reply(args[0], await getContent(args, 1)); break;
    case 'follow': await follow(args[0]); break;
    case 'unfollow': await unfollow(args[0]); break;
    case 'dm': await dm(args[0], await getContent(args, 1)); break;
    case 'dms': await readDms(parseInt(args[0]) || 10); break;
    case 'zap': await zap(args[0], parseInt(args[1]), args.slice(2).join(' ') || ''); break;
    case 'mentions': await mentions(parseInt(args[0]) || 20); break;
    case 'show': await show(args[0]); break;
    case 'feed': await feed(parseInt(args[0]) || 20); break;
    case 'profile': await profile(args[0], args.slice(1).join(' ')); break;
    case 'profile-set': await profileSet(await getContent(args)); break;
    case 'lookup': await lookup(args[0]); break;
    case 'react': await react(args[0], args[1] || '🤙'); break;
    case 'repost': await repost(args[0]); break;
    case 'delete': await deleteEvent(args[0]); break;
    case 'mute': await mute(args[0]); break;
    case 'unmute': await unmute(args[0]); break;
    case 'bookmark': await bookmark(args[0]); break;
    case 'unbookmark': await unbookmark(args[0]); break;
    case 'bookmarks': await listBookmarks(); break;
    case 'whoami': whoami(); break;
    case 'pending-mentions': await pendingMentions(args[0] || DEFAULT_STATE_FILE, parseInt(args[1]) || 15); break;
    case 'mark-responded': await markResponded(args[0], args[1], args[2] || DEFAULT_STATE_FILE); break;
    case 'mark-ignored': await markIgnored(args[0], args[1] || 'no_response_needed', args[2] || DEFAULT_STATE_FILE); break;
    case 'rate-limit': checkRateLimit(args[0] || DEFAULT_STATE_FILE); break;
    case 'autoresponse-status': await autoResponseStatus(args[0] || DEFAULT_STATE_FILE); break;
    case 'relays':
      if (args[0] === 'add') await addRelay(args[1], args[2]);
      else if (args[0] === 'remove') await removeRelay(args[1]);
      else await listRelays();
      break;
    case 'channel':
      if (args[0] === 'create') await createChannel(args[1], args[2], args[3]);
      else if (args[0] === 'post') await channelPost(args[1], await getContent(args, 2));
      else if (args[0] === 'read') await channelMessages(args[1], parseInt(args[2]) || 20);
      else console.log('Usage: channel <create|post|read> [args]');
      break;
    case 'badge':
      if (args[0] === 'create') await createBadge(args[1], args[2], args[3], args[4]);
      else if (args[0] === 'award') await awardBadge(args[1], args[2]);
      else if (args[0] === 'list') await listBadges();
      else await listBadges();
      break;
    default:
      console.log(`Nostr CLI - General Purpose

SETUP
  init [key]                  Generate new identity or import nsec/hex
  status                      Check configuration status

IDENTITY
  whoami                      Show your pubkey/npub
  profile [name] [about]      Get or set profile
  profile-set <json>          Set profile fields (JSON)

SOCIAL
  post <content>              Post a note (kind 1)
  reply <note1...> <content>  Reply to a note
  react <note1...> [emoji]    React to a note (default: 🤙)
  repost <note1...>           Repost/boost a note
  delete <note1...>           Delete your note
  mentions [limit]            Check mentions
  show <note1...>             Show full note content
  feed [limit]                View feed from follows

CONNECTIONS
  follow <npub>               Follow someone
  unfollow <npub>             Unfollow someone
  mute <npub>                 Mute someone
  unmute <npub>               Unmute someone
  lookup <user@domain>        NIP-05 lookup

BOOKMARKS
  bookmark <note1...>         Bookmark a note
  unbookmark <note1...>       Remove bookmark
  bookmarks                   List bookmarks

DMs
  dm <npub> <message>         Send encrypted DM (NIP-04)
  dms [limit]                 Read your DMs

RELAYS (NIP-65)
  relays                      List your relay list
  relays add <url> [mode]     Add relay (mode: read/write)
  relays remove <url>         Remove relay

CHANNELS (NIP-28)
  channel create <name>       Create public channel
  channel post <id> <msg>     Post to channel
  channel read <id> [limit]   Read channel messages

BADGES (NIP-58)
  badge list                  List your badges
  badge create <id> <name>    Create badge definition
  badge award <badge> <npub>  Award badge to user

ZAPS (NIP-57)
  zap <npub> <sats> [comment] Create zap invoice

AUTORESPONSE (Heartbeat Integration)
  pending-mentions [file] [limit]   Get unprocessed WoT mentions (JSON)
  mark-responded <note> [resp]      Mark mention as responded
  mark-ignored <note> [reason]      Mark mention as ignored
  rate-limit [file]                 Check hourly rate limit (10/hr)
  autoresponse-status [file]        Show autoresponse state summary

WALLET (use cocod)
  cocod init                  Initialize Cashu wallet
  cocod balance               Check balance
  cocod send bolt11 <inv>     Pay Lightning invoice
  cocod receive bolt11 <amt>  Create invoice to receive
  cocod npc address           Get your Lightning address`);
  }
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
} finally {
  pool.close(RELAYS);
}
