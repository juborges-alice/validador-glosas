CSS = r"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&display=swap">
<style>
/* Layout: relatório em uma coluna. Resposta curta, depois valor, itens, PEG, motivos, prestadores, setembro x outubro, projeção e próximos passos. */
:root {
  --bg: #fbf8f9; --surface: #ffffff; --ink: #40002d; --ink-2: #6b5a64; --ink-3: #94858d;
  --line: #eee5ea; --accent: #be0380; --accent-soft: #fbe7f3;
  --s1: #2a78d6; --s2: #eb6834;
  --good: #0f7b3f; --good-soft: #e3f4ea; --warn: #8a5a00; --warn-soft: #fbf0d9; --bad: #b3261e; --bad-soft: #fbe9e7; --neutral-soft: #f1ecef;
  --font-display: "Bricolage Grotesque", "Figtree", system-ui, sans-serif;
  --font-body: "Figtree", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #1a1418; --surface: #221a1f; --ink: #f6e9f0; --ink-2: #c7b5bf; --ink-3: #9a8891; --line: #34282f; --accent: #e0479f; --accent-soft: #3a1830;
  --s1: #3987e5; --s2: #d95926; --good: #5fd08f; --good-soft: #17301f; --warn: #f0c060; --warn-soft: #3a2e14; --bad: #ff8a80; --bad-soft: #3a1c1a; --neutral-soft: #2c2228; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #1a1418; --surface: #221a1f; --ink: #f6e9f0; --ink-2: #c7b5bf; --ink-3: #9a8891; --line: #34282f; --accent: #e0479f; --accent-soft: #3a1830;
  --s1: #3987e5; --s2: #d95926; --good: #5fd08f; --good-soft: #17301f; --warn: #f0c060; --warn-soft: #3a2e14; --bad: #ff8a80; --bad-soft: #3a1c1a; --neutral-soft: #2c2228; color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: 15px; line-height: 1.55; }
.wrap { max-width: 1040px; margin: 0 auto; padding-inline: 20px; padding-block: 32px 64px; display: flex; flex-direction: column; gap: 44px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 700; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
h1 { font-size: clamp(26px, 4vw, 36px); line-height: 1.1; }
h2 { font-size: 22px; line-height: 1.2; }
h3 { font-size: 15px; font-family: var(--font-body); font-weight: 600; }
p { margin: 0; max-width: 72ch; }
.eyebrow { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); }
.muted { color: var(--ink-2); } .small { font-size: 13px; }
header, section { display: flex; flex-direction: column; gap: 14px; }
.scope { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { font-size: 12px; padding: 3px 10px; border-radius: 999px; background: var(--neutral-soft); color: var(--ink-2); white-space: nowrap; }
a { color: var(--accent); }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 20px; min-width: 0; display: flex; flex-direction: column; gap: 10px; }
.verdict { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.v { display: flex; flex-direction: column; gap: 8px; padding: 18px; border-radius: 12px; background: var(--surface); border: 1px solid var(--line); min-width: 0; }
.v .q { font-size: 13px; color: var(--ink-2); }
.v .a { font-family: var(--font-display); font-size: 21px; font-weight: 700; line-height: 1.2; }
.v p { font-size: 14px; color: var(--ink-2); }
.pill { align-self: flex-start; display: inline-flex; align-items: center; font-size: 12px; font-weight: 600; padding: 2px 10px; border-radius: 999px; white-space: nowrap; }
.pill.good { background: var(--good-soft); color: var(--good); } .pill.warn { background: var(--warn-soft); color: var(--warn); }
.pill.bad { background: var(--bad-soft); color: var(--bad); } .pill.flat { background: var(--neutral-soft); color: var(--ink-2); }
.tbl-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { padding: 8px 10px; text-align: right; border-bottom: 1px solid var(--line); white-space: nowrap; }
th { font-size: 12px; font-weight: 600; color: var(--ink-2); text-transform: uppercase; letter-spacing: 0.04em; }
th:first-child, td:first-child { text-align: left; }
td.wrap-cell { white-space: normal; min-width: 220px; text-align: left; }
tr.hl td { background: var(--accent-soft); }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: var(--ink-2); }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
.legend i.proj { background-image: repeating-linear-gradient(135deg, var(--ink-3) 0 2px, transparent 2px 5px); border: 1px solid var(--ink-3); }
svg { display: block; width: 100%; height: auto; overflow: visible; }
svg text { fill: var(--ink-2); font-family: var(--font-body); font-size: 12px; }
svg .val { fill: var(--ink); font-weight: 600; }
svg .grid { stroke: var(--line); stroke-width: 1; }
svg .hit { fill: transparent; } svg .hit:hover { fill: var(--ink); fill-opacity: 0.05; }
#tip { position: fixed; pointer-events: none; z-index: 10; background: var(--ink); color: var(--bg); font-size: 12px; line-height: 1.45; padding: 8px 10px; border-radius: 8px; max-width: 300px; }
.grid2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.prov { display: flex; flex-direction: column; gap: 10px; }
.prov h3 { font-family: var(--font-display); font-size: 19px; }
.prov p { font-size: 14px; color: var(--ink-2); }
ol.steps { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 10px; }
ul.plain { margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 6px; font-size: 14px; color: var(--ink-2); }
code { font-size: 12.5px; background: var(--neutral-soft); padding: 1px 5px; border-radius: 5px; }
@media (max-width: 520px) { .wrap { padding-inline: 16px; } .panel { padding: 14px; } th, td { padding: 7px 8px; } }
</style>
"""

JS = r"""
<script>
const MES = {"01":"jan","02":"fev","03":"mar","04":"abr","05":"mai","06":"jun","07":"jul","08":"ago","09":"set","10":"out"};
const lab = m => MES[m.slice(5,7)];
const nf = (v, d=0) => v.toLocaleString("pt-BR", {minimumFractionDigits:d, maximumFractionDigits:d});
const brl = v => "R$ " + nf(v) + " mil";
const tip = document.getElementById("tip");
function bindTips(root) {
  root.querySelectorAll("[data-tip]").forEach(el => {
    el.addEventListener("mousemove", e => { tip.innerHTML = el.getAttribute("data-tip"); tip.hidden = false;
      tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 8) + "px"; tip.style.top = (e.clientY + 14) + "px"; });
    el.addEventListener("mouseleave", () => tip.hidden = true);
  });
}
function rpath(x, y, w, h, r) { if (h <= 0.5) return ""; r = Math.min(r, h, w/2);
  return `M${x},${y+h}V${y+r}Q${x},${y} ${x+r},${y}H${x+w-r}Q${x+w},${y} ${x+w},${y+r}V${y+h}Z`; }
function niceMax(v) { const p = Math.pow(10, Math.floor(Math.log10(v))); for (const m of [1,1.2,1.5,2,2.5,3,4,5,6,8,10]) if (m*p >= v) return m*p; return 10*p; }
// rows: [{m, a, o, pa, po}] a/o = real; pa/po = projected (only last). fmt for labels.
function stacked(id, rows, unit, fmt) {
  const W = 680, H = 270, L = 52, R = 10, T = 24, B = 30, pw = W-L-R, ph = H-T-B;
  const tot = r => r.a + r.o + (r.pa||0) + (r.po||0);
  const max = niceMax(Math.max(...rows.map(tot)) * 1.08);
  const y = v => T + ph - v/max*ph, band = pw/rows.length, bw = Math.min(44, band*0.56);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${unit} por mês, autorização e demais motivos"><defs>
    <pattern id="h${id}" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="var(--surface)"/><rect width="2.2" height="5" fill="var(--ink-3)"/></pattern></defs>`;
  for (let i=0;i<=4;i++){ const v=max*i/4; s += `<line class="grid" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${fmt(v)}</text>`; }
  rows.forEach((r,i) => {
    const x = L + band*i + band/2 - bw/2; let base = 0;
    const segs = [["o", r.o, "var(--s1)"], ["a", r.a, "var(--s2)"]];
    if (r.pa || r.po) { segs.push(["po", r.po||0, `url(#h${id})`]); segs.push(["pa", r.pa||0, `url(#h${id})`]); }
    const drawn = segs.filter(sg => sg[1] > 0);
    drawn.forEach((sg, k) => {
      const top = k === drawn.length-1; const y0 = y(base), y1 = y(base+sg[1]);
      const h = Math.max(0, y0 - y1 - (k>0 ? 2 : 0));
      s += top ? `<path d="${rpath(x, y1, bw, h, 4)}" fill="${sg[2]}"${sg[0].startsWith("p")?' stroke="var(--ink-3)" stroke-width="1"':''}/>`
               : `<rect x="${x}" y="${y1}" width="${bw}" height="${h}" fill="${sg[2]}"${sg[0].startsWith("p")?' stroke="var(--ink-3)" stroke-width="1"':''}/>`;
      base += sg[1];
    });
    s += `<text class="val" x="${x+bw/2}" y="${y(tot(r))-7}" text-anchor="middle">${fmt(tot(r))}</text>`;
    s += `<text x="${x+bw/2}" y="${H-8}" text-anchor="middle">${r.label || lab(r.m)}</text>`;
    const pct = r.a + r.o + (r.pa||0) + (r.po||0) > 0 ? 100*(r.a+(r.pa||0))/tot(r) : 0;
    let t = `<b>${r.label || lab(r.m)+'/26'}</b><br>Autorização (7DL/7F8): ${fmt(r.a)}<br>Demais motivos: ${fmt(r.o)}`;
    if (r.pa || r.po) t += `<br>Projeção 07–31/10: ${fmt((r.pa||0)+(r.po||0))} (autorização ${fmt(r.pa||0)})`;
    t += `<br>Total: ${fmt(tot(r))} · autorização ${nf(pct)}%`;
    s += `<rect class="hit" x="${L+band*i}" y="${T}" width="${band}" height="${ph}" data-tip="${t}"/>`;
  });
  s += `</svg>`;
  const el = document.getElementById(id); el.innerHTML = s; bindTips(el);
}
// simple bars: rows [{label, v, pv, tipx}]
function bars(id, rows, fmt, aria, col) {
  col = col || "var(--accent)";
  const W = 680, H = 230, L = 52, R = 10, T = 24, B = 30, pw = W-L-R, ph = H-T-B;
  const max = niceMax(Math.max(...rows.map(r => r.v + (r.pv||0))) * 1.08);
  const y = v => T + ph - v/max*ph, band = pw/rows.length, bw = Math.min(44, band*0.56);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${aria}"><defs><pattern id="h${id}" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="var(--surface)"/><rect width="2.2" height="5" fill="var(--ink-3)"/></pattern></defs>`;
  for (let i=0;i<=4;i++){ const v=max*i/4; s += `<line class="grid" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${fmt(v)}</text>`; }
  rows.forEach((r,i) => {
    const x = L + band*i + band/2 - bw/2, tot = r.v + (r.pv||0);
    if (r.pv) { s += `<rect x="${x}" y="${y(r.v)}" width="${bw}" height="${y(0)-y(r.v)}" fill="${col}"/>`;
      s += `<path d="${rpath(x, y(tot), bw, y(r.v)-y(tot)-2, 4)}" fill="url(#h${id})" stroke="var(--ink-3)" stroke-width="1"/>`; }
    else s += `<path d="${rpath(x, y(r.v), bw, y(0)-y(r.v), 4)}" fill="${col}"/>`;
    s += `<text class="val" x="${x+bw/2}" y="${y(tot)-7}" text-anchor="middle">${fmt(tot)}</text><text x="${x+bw/2}" y="${H-8}" text-anchor="middle">${r.label}</text>`;
    s += `<rect class="hit" x="${L+band*i}" y="${T}" width="${band}" height="${ph}" data-tip="${r.tipx}"/>`;
  });
  s += `</svg>`; const el = document.getElementById(id); el.innerHTML = s; bindTips(el);
}
</script>
"""

def page(title, body, data_js):
    return f"<title>{title}</title>\n{CSS}\n<div id=\"tip\" hidden></div>\n<div class=\"wrap\">\n{body}\n</div>\n{JS}\n<script>\n{data_js}\n</script>\n"
