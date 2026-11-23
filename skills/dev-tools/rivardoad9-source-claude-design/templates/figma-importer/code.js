// Figma importer skeleton: draws a mobile screen natively from a locked spec.
// Usage: edit W/H, the palette, and main(); zip manifest.json + code.js; user imports
// via Plugins → Development → Import plugin from manifest.
const W = 390, H = 844;
const C = { bg: "#F5F6FF", ink: "#0A1F44", brand: "#123D9B", muted: "#7B86A2", line: "#EAEDF9", white: "#FFFFFF" };

const rgb = h => { h = h.replace("#", ""); return { r: parseInt(h.slice(0,2),16)/255, g: parseInt(h.slice(2,4),16)/255, b: parseInt(h.slice(4,6),16)/255 }; };
const solid = h => [{ type: "SOLID", color: rgb(h) }];

let FAMILY = "Plus Jakarta Sans";
let FONT = { r: "Regular", m: "Medium", sb: "SemiBold", b: "Bold", eb: "ExtraBold" };

async function loadFonts() {
  const fam = "Plus Jakarta Sans";
  const map = { r: "Regular", m: "Medium", sb: "SemiBold", b: "Bold", eb: "ExtraBold" };
  try {
    for (const k in map) await figma.loadFontAsync({ family: fam, style: map[k] });
    FAMILY = fam; FONT = map;
  } catch (e) {
    // A missing family throws once and aborts the whole run — always fall back.
    FAMILY = "Inter";
    const im = { r: "Regular", m: "Medium", sb: "SemiBold", b: "Bold", eb: "ExtraBold" };
    for (const k in im) await figma.loadFontAsync({ family: FAMILY, style: im[k] });
    FONT = im;
    figma.notify("Font target tidak ada di mesin ini — pakai Inter sementara.", { timeout: 6000 });
  }
}

function frame(parent, name, x, y, w, h, fill, radius, stroke) {
  const n = figma.createFrame();
  n.name = name; n.x = x; n.y = y; n.resize(w, h);
  n.fills = fill ? (Array.isArray(fill) ? fill : solid(fill)) : [];
  n.cornerRadius = radius || 0;
  if (stroke) { n.strokes = solid(stroke); n.strokeWeight = 1; n.strokeAlign = "INSIDE"; }
  parent.appendChild(n);
  return n;
}

function txt(parent, s, x, y, size, style, color, w) {
  const t = figma.createText();
  t.fontName = { family: FAMILY, style: FONT[style] || "Regular" };
  t.characters = s; t.fontSize = size; t.fills = solid(color);
  t.x = x; t.y = y;
  if (w) { t.resize(w, t.height); t.textAutoResize = "HEIGHT"; }
  parent.appendChild(t);
  return t;
}

function svgIcon(parent, path, x, y, color, size) {
  const s = `<svg xmlns="http://www.w3.org/2000/svg" width="${size||24}" height="${size||24}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
  const n = figma.createNodeFromSvg(s); // colour must be baked in; currentColor is not inherited
  n.x = x; n.y = y;
  parent.appendChild(n);
  return n;
}

function gradient(fill, from, mid, to, angle) {
  return [{
    type: "GRADIENT_LINEAR",
    gradientTransform: angle || [[0.9, 0.42, -0.15], [-0.42, 0.9, 0.35]],
    gradientStops: [
      { position: 0, color: { ...rgb(from), a: 1 } },
      { position: 0.55, color: { ...rgb(mid || from), a: 1 } },
      { position: 1, color: { ...rgb(to || from), a: 1 } }
    ]
  }];
}

async function main() {
  await loadFonts();
  const root = frame(figma.currentPage, `Screen — ${W}x${H}`, 0, 0, W, H, C.bg, 0);
  root.clipsContent = true;

  // ---- build the screen here; coordinates explicit so it matches the HTML 1:1 ----
  const hero = frame(root, "hero", 20, 104, 350, 136, null, 16);
  hero.fills = gradient(null, "#0B2A6B", "#123D9B", "#2F6BFF");
  hero.clipsContent = true;
  txt(hero, "Title", 18, 18, 18, "sb", C.white);

  // ---- bottom nav pinned to bottom ----
  const nav = frame(root, "bottom-nav", 0, H - 80, W, 80, C.white, 0);
  nav.strokes = solid("#EDEFFA"); nav.strokeWeight = 1;

  figma.currentPage.selection = [root];
  figma.viewport.scrollAndZoomIntoView([root]);
  figma.notify("Frame siap.");
  figma.closePlugin();
}

main().catch(e => { figma.notify("Gagal: " + e.message, { error: true }); figma.closePlugin(); });
