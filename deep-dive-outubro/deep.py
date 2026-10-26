import sys, csv, json, collections
sys.path.insert(0, '../aumento-recurso-outubro/relatorios')
from common import page
f = lambda x: float(x) if x not in ('', None) else 0.0
M = ['2026-03','2026-04','2026-05','2026-06','2026-07','2026-08','2026-09','2026-10']
F = ['00-15','16-30','31-45','46-60','61-90','91+']
def series(seg, proj):
    b = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in csv.DictReader(open('b.csv')):
        if r['seg'] == seg:
            x = b[r['mes'][:7]]; x[0] += int(r['pegs']); x[1] += int(r['itens']); x[2] += f(r['vlr'])
    w = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in csv.DictReader(open('w1.csv')):
        if r['seg'] == seg: w[r['mes'][:7]][r['faixa']] += f(r['vlr'])
    vol = [dict(m=m, v=round(b[m][2]/1e3, 1), i=b[m][1], p=b[m][0]) for m in M]
    vol[-1].update(pv=proj[0], pi=proj[1], pp=proj[2])
    win = [dict(m=m, s=[round(100*w[m][k]/sum(w[m].values()), 1) for k in F]) for m in M]
    return json.dumps(dict(vol=vol, win=win))

EXTRA_CSS = r"""<style>.v .pill, .chip { white-space: normal; }
:root { --w1:#cfe0f6; --w2:#9ec2ee; --w3:#5f9ae0; --w4:#2a6fc8; --w5:#f0a37c; --w6:#c8501e; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --w1:#1e3555; --w2:#2b4f80; --w3:#3c6fb3; --w4:#5b93dd; --w5:#c8693c; --w6:#ef8a58; } }
:root[data-theme="dark"] { --w1:#1e3555; --w2:#2b4f80; --w3:#3c6fb3; --w4:#5b93dd; --w5:#c8693c; --w6:#ef8a58; }
</style>"""
CHART_JS = r"""
const D = __DATA__;
bars("chVol", D.vol.map(r => ({label: r.m==="2026-10" ? "out*" : lab(r.m), v: r.v, pv: r.pv||0,
  tipx: `<b>${lab(r.m)}/26</b><br>Valor: R$ ${nf(r.v)} mil${r.pv?` (real até 22/10) + R$ ${nf(r.pv)} mil projetados`:""}<br>Itens: ${nf(r.i)}${r.pi?` + ~${nf(r.pi)}`:""}<br>PEGs: ${r.p}${r.pp?` + ~${r.pp}`:""}`})), v => nf(v), "Valor recursado por mês (R$ mil)", "var(--accent)");
document.getElementById("tVol").innerHTML = `<thead><tr><th></th>${D.vol.map(r=>`<th>${r.m==="2026-10"?"out (01–22)":lab(r.m)}</th>`).join("")}<th>out* proj.</th></tr></thead><tbody>
 <tr><td>Valor (R$ mil)</td>${D.vol.map(r=>`<td>${nf(r.v)}</td>`).join("")}<td><b>~${nf(D.vol[7].v+D.vol[7].pv)}</b></td></tr>
 <tr><td>Itens</td>${D.vol.map(r=>`<td>${nf(r.i)}</td>`).join("")}<td><b>~${nf(D.vol[7].i+D.vol[7].pi)}</b></td></tr>
 <tr><td>PEGs</td>${D.vol.map(r=>`<td>${nf(r.p)}</td>`).join("")}<td><b>~${nf(D.vol[7].p+D.vol[7].pp)}</b></td></tr>
 <tr><td>R$ mil por PEG</td>${D.vol.map(r=>`<td>${nf(r.v/r.p,1)}</td>`).join("")}<td>–</td></tr></tbody>`;
(function(){
  const K = ["0–15 dias","16–30","31–45","46–60","61–90",">90"], C = ["var(--w1)","var(--w2)","var(--w3)","var(--w4)","var(--w5)","var(--w6)"];
  const W = 680, H = 250, L = 44, R = 10, T = 14, B = 30, pw = W-L-R, ph = H-T-B, rows = D.win;
  const band = pw/rows.length, bw = Math.min(46, band*0.6), y = v => T + ph - v/100*ph;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Distribuição do valor recursado por dias entre a glosa e o recurso">`;
  [0,25,50,75,100].forEach(v => s += `<line class="grid" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${v}%</text>`);
  rows.forEach((r,i) => {
    const x = L + band*i + band/2 - bw/2; let base = 0;
    r.s.forEach((p,k) => { if (p <= 0) return; const y1 = y(base+p), h = Math.max(0, y(base)-y1-1); s += `<rect x="${x}" y="${y1}" width="${bw}" height="${h}" fill="${C[k]}"/>`; base += p; });
    const late = r.s[4]+r.s[5];
    s += `<text x="${x+bw/2}" y="${H-8}" text-anchor="middle">${r.m==="2026-10"?"out*":lab(r.m)}</text>`;
    s += `<rect class="hit" x="${L+band*i}" y="${T}" width="${band}" height="${ph}" data-tip="<b>${lab(r.m)}/26</b><br>${K.map((k,j)=>`${k}: ${nf(r.s[j])}%`).join("<br>")}<br><b>Mais de 60 dias: ${nf(late)}%</b>"/>`;
  });
  s += `<line x1="${L}" x2="${W-R}" y1="${T}" y2="${T}" stroke="var(--line)"/></svg>`;
  const el = document.getElementById("chWin"); el.innerHTML = s; bindTips(el);
  document.getElementById("lgWin").innerHTML = K.map((k,j)=>`<span><i style="background:${C[j]}"></i>${k}</span>`).join("");
  document.getElementById("tWin").innerHTML = `<thead><tr><th>Dias da glosa ao recurso</th>${rows.map(r=>`<th>${r.m==="2026-10"?"out (01–22)":lab(r.m)}</th>`).join("")}</tr></thead><tbody>` +
    K.map((k,j)=>`<tr${j>=4?' class="hl"':''}><td>${k}</td>${rows.map(r=>`<td>${nf(r.s[j])}%</td>`).join("")}</tr>`).join("") +
    `<tr><td><b>Mais de 60 dias</b></td>${rows.map(r=>`<td><b>${nf(r.s[4]+r.s[5])}%</b></td>`).join("")}</tr></tbody>`;
})();
"""
def build(seg, title, body, proj, out):
    js = CHART_JS.replace('__DATA__', series(seg, proj))
    open(out, 'w').write(page(title, EXTRA_CSS + body, js))

SCOPE = """<span class="chip">Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 22/10/2026</span>
    <span class="chip">Sem o lote antigo da DASA (glosas de 2025) e sem os recursos de 7F6 de jul–ago</span>
    <span class="chip">Janela = dias entre a data da glosa e a data do recurso</span>"""

LABS = r"""
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Deep dive · Laboratórios e clínicas · Out/26</span>
  <h1>Por que o recurso de laboratórios subiu em outubro</h1>
  <p class="muted">Leitura do mês com dados até 22/10: quanto subiu, quais prestadores puxaram, em quais motivos e como mudou a janela entre a glosa e o recurso.</p>
  <div class="scope">""" + SCOPE + r"""</div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Quanto subiu?</span>
      <span class="pill warn">Recorde de itens; valor no pico de julho</span>
      <span class="a">R$ 761 mil · 7.155 itens até 22/10</span>
      <p>A projeção fecha o mês em ~R$ 900 mil (faixa de R$ 780 mil a 1,1 mi), ~8,6 mil itens e ~410 PEGs. Em itens, é o maior mês do ano com folga: o recorde anterior era 6,0 mil (abril). Em valor, fica no nível de julho (R$ 907 mil).</p>
    </div>
    <div class="v">
      <span class="q">Quem puxou?</span>
      <span class="pill bad">Fleury: 55% do valor e 64% dos itens</span>
      <span class="a">Fleury R$ 419 mil · DASA R$ 254 mil</span>
      <p>O Fleury recursou 54% da glosa de agosto, contra 22–37% nas coortes anteriores, e mandou tudo dentro do prazo de 60 dias. A DASA trouxe a coorte de agosto com atraso (mediana de 53 dias, contra 44–46). O Femme veio no padrão.</p>
    </div>
    <div class="v">
      <span class="q">Em qual motivo?</span>
      <span class="pill warn">74% em códigos da tabela nova</span>
      <span class="a">7G4, 7F8, 7G9 e 7F6</span>
      <p>Duplicidade 7G4 (R$ 193 mil), autorização 7F8 (R$ 133 mil), local de atendimento 7G9 (R$ 123 mil e 2.596 itens, R$ 103 mil do Fleury) e data incorreta 7F6 (R$ 85 mil). Somados ao 7EK (R$ 136 mil), explicam 88% do mês.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Volume por mês</h2>
  <p class="muted">Valor recursado por mês de recebimento. A barra de outubro mostra o real até 22/10 e, hachurada, a projeção de 23 a 31/10.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--accent)"></i>Valor recebido (R$ mil)</span><span><i class="proj"></i>Projeção 23–31/10</span></div>
    <div id="chVol"></div>
    <div class="tbl-wrap"><table id="tVol"></table></div>
  </div>
</section>

<section>
  <h2>2. Prestadores</h2>
  <div class="panel tbl-wrap">
    <h3>Outubro até 22/10</h3>
    <table>
      <thead><tr><th>Prestador</th><th>Valor</th><th>Itens</th><th>PEGs</th><th>Coorte de glosa</th><th>Dias até o recurso</th><th>Mais de 60 dias</th><th>Acato (analisado)</th></tr></thead>
      <tbody>
        <tr class="hl"><td>Fleury</td><td>R$ 419 mil</td><td>4.605</td><td>120</td><td>agosto</td><td>41–69</td><td>R$ 56 mil</td><td>50%</td></tr>
        <tr><td>DASA</td><td>R$ 254 mil</td><td>965</td><td>161</td><td>agosto (e início de setembro)</td><td>38–60</td><td>–</td><td>86%</td></tr>
        <tr><td>Femme</td><td>R$ 72 mil</td><td>1.483</td><td>20</td><td>agosto</td><td>44–55</td><td>–</td><td>47%</td></tr>
        <tr><td>Centro Diagnóstico (CDDAPDGL)</td><td>R$ 14 mil</td><td>59</td><td>3</td><td>agosto</td><td>41–53</td><td>–</td><td>95%</td></tr>
        <tr><td>Demais</td><td>R$ 1 mil</td><td>43</td><td>5</td><td>setembro</td><td>21–31</td><td>–</td><td>–</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Como cada um recursa: mediana de dias e % do valor que chega depois de 60 dias, por mês de recebimento</h3>
    <table>
      <thead><tr><th>Prestador</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th></tr></thead>
      <tbody>
        <tr class="hl"><td>Fleury</td><td>86 dias</td><td>79 dias · 88% &gt;60</td><td>65 dias · 86% &gt;60</td><td>56 dias · 46% &gt;60</td><td><b>57 dias · 13% &gt;60</b></td></tr>
        <tr><td>DASA</td><td>49 dias</td><td>44 dias · 22% &gt;60</td><td>46 dias · 17% &gt;60</td><td>(só lote antigo)</td><td><b>53 dias · 0% &gt;60</b></td></tr>
        <tr><td>Femme</td><td>37 dias</td><td>62 dias</td><td>50 dias</td><td>45 dias</td><td>49 dias</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Coortes de glosa do Fleury: quanto foi recursado</h3>
    <table>
      <thead><tr><th>Coorte</th><th>Glosado</th><th>Recursado até hoje</th><th>%</th><th>Recebido principalmente em</th></tr></thead>
      <tbody>
        <tr><td>Mai</td><td>R$ 442 mil</td><td>R$ 163 mil</td><td>37%</td><td>jul</td></tr>
        <tr><td>Jun</td><td>R$ 1.035 mil</td><td>R$ 342 mil</td><td>33%</td><td>ago</td></tr>
        <tr><td>Jul</td><td>R$ 513 mil</td><td>R$ 115 mil</td><td>22%</td><td>set</td></tr>
        <tr class="hl"><td>Ago</td><td>R$ 783 mil</td><td><b>R$ 419 mil</b></td><td><b>54%</b></td><td>out</td></tr>
        <tr><td>Set</td><td>R$ 880 mil</td><td>–</td><td>–</td><td>esperado em nov</td></tr>
      </tbody>
    </table>
    <p class="small muted">Junho sem os recursos de 7F6 de jul–ago. A coorte de agosto do Fleury foi a maior em valor e a mais recursada em %: os dois efeitos se somaram em outubro.</p>
  </div>
</section>

<section>
  <h2>3. Janela de envio: os recursos passaram a chegar dentro do prazo</h2>
  <p class="muted">Distribuição do valor recebido no mês pelos dias entre a glosa e o recurso. Laranja = mais de 60 dias.</p>
  <div class="panel">
    <div class="legend" id="lgWin"></div>
    <div id="chWin"></div>
    <div class="tbl-wrap"><table id="tWin"></table></div>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">O que mudou</span><h3>Fora do prazo caiu de 46–48% para 7%</h3>
      <p>De julho a setembro, quase metade do valor chegava depois de 60 dias, quase todo do Fleury. Em outubro, 72% chegou entre 46 e 60 dias e só 7% depois. O Fleury encurtou a mediana de 65–79 para 57 dias.</p></div>
    <div class="panel prov"><span class="pill flat">Efeito no mês</span><h3>A coorte inteira cabe num mês só</h3>
      <p>Com a janela em 46–60 dias, a glosa de um mês é recursada inteira no mês M+2. Antes, parte escorria para M+3. Em outubro, isso juntou a coorte de agosto do Fleury, que já era grande, em um único mês.</p></div>
    <div class="panel prov"><span class="pill good">Lado bom</span><h3>Menos recurso fora do prazo</h3>
      <p>Com o recurso chegando dentro dos 60 dias, cai o volume que poderia ser negado por prazo. O lado ruim é que ele deixa de ser contestável por esse critério.</p></div>
  </div>
</section>

<section>
  <h2>4. Motivos</h2>
  <div class="panel tbl-wrap">
    <h3>Valor recursado por motivo e mês de recebimento (R$ mil · itens)</h3>
    <table>
      <thead><tr><th>Motivo</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out (01–22)</th><th>Quem puxa em outubro</th></tr></thead>
      <tbody>
        <tr><td>7G4 · duplicidade</td><td>–</td><td>–</td><td>142 · 693</td><td>21 · 112</td><td><b>193 · 1.074</b></td><td class="wrap-cell">DASA, Fleury e Femme</td></tr>
        <tr><td>7EK · sem registro de execução</td><td>114 · 965</td><td>188 · 1.232</td><td>95 · 1.142</td><td>59 · 157</td><td><b>136 · 507</b></td><td class="wrap-cell">Fleury (R$ 99 mil)</td></tr>
        <tr><td>7F8 · autorização</td><td>–</td><td>–</td><td>55 · 374</td><td>40 · 94</td><td><b>133 · 1.042</b></td><td class="wrap-cell">Fleury, DASA e Femme (731 itens de baixo valor)</td></tr>
        <tr class="hl"><td>7G9 · local de atendimento</td><td>–</td><td>–</td><td>10 · 37</td><td>3 · 5</td><td><b>123 · 2.596</b></td><td class="wrap-cell">Fleury R$ 103 mil, DASA R$ 20 mil. Antes, só 5–10% desse motivo era recursado</td></tr>
        <tr><td>7F6 · data incorreta</td><td>–</td><td>–</td><td>–</td><td>12 · 384</td><td><b>85 · 422</b></td><td class="wrap-cell">DASA e Fleury</td></tr>
        <tr><td>7EY · senha cancelada</td><td>3 · 66</td><td>72 · 869</td><td>42 · 680</td><td>3 · 59</td><td>35 · 1.021</td><td class="wrap-cell">Fleury</td></tr>
        <tr><td>7G3 · duplicidade de conta</td><td>–</td><td>–</td><td>13 · 113</td><td>3 · 18</td><td>32 · 200</td><td class="wrap-cell">DASA e Fleury</td></tr>
      </tbody>
    </table>
    <p class="small muted">Em junho e julho, o motivo principal era o 7DL (autorização, tabela antiga): R$ 202 mil e R$ 439 mil. O código é o primeiro motivo do item.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">Tabela nova</span><h3>Os códigos novos viraram o grosso do recurso</h3>
      <p>7G4, 7F8, 7G9, 7F6 e 7G3 somam R$ 566 mil, 74% do recebido em outubro. Em agosto, eram R$ 220 mil.</p></div>
    <div class="panel prov"><span class="pill bad">Novidade</span><h3>7G9 passou a ser recursado</h3>
      <p>Local de atendimento inválido quase não voltava como recurso. Em outubro, vieram 2,6 mil itens (R$ 123 mil), R$ 103 mil do Fleury. É o motivo que mais explica o recorde de itens.</p></div>
    <div class="panel prov"><span class="pill flat">Acato</span><h3>Autorização com acato menor</h3>
      <p>Do recurso de autorização já analisado em outubro, 31% foi acatado, contra 81% em agosto. Nos demais motivos, 72%. A amostra ainda é pequena (R$ 134 mil analisados).</p></div>
  </div>
</section>

<section>
  <h2>5. Falta de autorização por coorte de glosa: o peso do motivo caiu</h2>
  <p class="muted">Para cada mês de glosa: quanto da glosa e quanto do recurso daquela coorte vem do motivo de autorização (7DL até junho, 7F8 desde julho). A regra mudou em julho.</p>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Coorte de glosa</th><th>Glosa de autorização</th><th>% da glosa da coorte</th><th>Recurso de autorização</th><th>% do recurso da coorte (valor)</th><th>% do recurso da coorte (itens)</th><th>% recursado: autorização · demais</th></tr></thead>
      <tbody>
        <tr><td>Abr</td><td>R$ 424 mil · 3.054 itens</td><td>34%</td><td>R$ 237 mil · 1.422 itens</td><td>42%</td><td>37%</td><td>56% · 39%</td></tr>
        <tr><td>Mai</td><td>R$ 626 mil · 3.762 itens</td><td>55%</td><td>R$ 373 mil · 1.680 itens</td><td>55%</td><td>35%</td><td>60% · 58%</td></tr>
        <tr><td>Jun</td><td>R$ 519 mil · 4.345 itens</td><td>31%</td><td>R$ 306 mil · 1.998 itens</td><td>40%</td><td>33%</td><td>59% · 39%</td></tr>
        <tr class="hl"><td>Jul</td><td>R$ 204 mil · 1.163 itens</td><td>21%</td><td>R$ 94 mil · 465 itens</td><td><b>23%</b></td><td><b>17%</b></td><td>46% · 40%</td></tr>
        <tr class="hl"><td>Ago</td><td>R$ 255 mil · 1.729 itens</td><td>19%</td><td>R$ 132 mil · 1.039 itens</td><td><b>17%</b></td><td><b>15%</b></td><td>52% · 58%</td></tr>
        <tr><td>Set (aberta)</td><td>R$ 260 mil · 1.772 itens</td><td>17%</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>
      </tbody>
    </table>
    <p class="small muted">% recursado = recursado até 22/10 ÷ glosado da coorte. A coorte de agosto já tem de 57 a 77 dias e está praticamente fechada.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Confirmado</span><h3>A autorização perdeu peso no recurso</h3>
      <p>Nas coortes de abr–jun, a autorização era 40–55% do valor recursado e 33–37% dos itens. Nas coortes de julho e agosto, caiu para 17–23% do valor e 15–17% dos itens, acompanhando a queda da glosa do motivo (de 31–55% para 19–21% da glosa).</p></div>
    <div class="panel prov"><span class="pill flat">Sem mudança</span><h3>A taxa de recurso do motivo não subiu</h3>
      <p>A autorização segue sendo recursada em 46–60% do glosado, como antes. O que parecia alta no recurso em até 60 dias era efeito da janela: o Fleury passou a recursar dentro do prazo.</p></div>
    <div class="panel prov"><span class="pill flat">Por prestador</span><h3>Fleury mais, DASA menos</h3>
      <p>Na coorte de agosto, o Fleury recursou 62% da autorização glosada (33–56% antes). A DASA recursou 34% (55–69% antes). O Femme recursa quase tudo, mas em itens de baixo valor: 731 dos 1.039 itens recursados de autorização da coorte de agosto.</p></div>
  </div>
  <div class="panel">
    <p><b>No mês de recebimento:</b> outubro recebeu R$ 135 mil e 1.043 itens de autorização até 22/10. São 18% do valor e 15% dos itens do mês, contra 32–48% do valor de março a agosto. O motivo deixou de puxar o recurso de laboratórios. O aumento de outubro vem dos demais motivos.</p>
  </div>
</section>

<section>
  <h2>6. O que vem pela frente: a glosa de outubro está alta</h2>
  <div class="panel">
    <p>A glosa de laboratórios e clínicas de 01 a 22/10 já soma <b>R$ 1,75 mi, 10,5% do apresentado</b>, contra 7,7–8,7% em agosto e setembro. O maior motivo é data incorreta (7F6): <b>R$ 631 mil, 3,8% do apresentado</b>, o dobro de setembro. Com o Fleury e a DASA recursando 55–60% e dentro de 60 dias, essa glosa deve virar recurso em dezembro.</p>
  </div>
</section>

<section>
  <h2>7. Projeção de fechamento</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Valor</th><th>Itens</th><th>PEGs</th></tr></thead>
      <tbody>
        <tr><td>Real 01–22/10</td><td>R$ 761 mil</td><td>7.155</td><td>309</td></tr>
        <tr><td>DASA, coorte de setembro e resto de agosto</td><td>R$ 97 mil</td><td>~710</td><td>~80</td></tr>
        <tr><td>Femme e Fleury, coorte de setembro</td><td>R$ 34 mil</td><td>~740</td><td>~15</td></tr>
        <tr><td>Demais</td><td>R$ 4 mil</td><td>~10</td><td>~4</td></tr>
        <tr class="hl"><td><b>Fechamento estimado</b></td><td><b>~R$ 900 mil</b></td><td><b>~8,6 mil</b></td><td><b>~410</b></td></tr>
        <tr><td>Se a DASA de setembro ficar para novembro</td><td>~R$ 810 mil</td><td>~8,1 mil</td><td>~350</td></tr>
      </tbody>
    </table>
  </div>
  <ul class="plain">
    <li><b>Método:</b> curvas por prestador e motivo do % do glosado que chega a cada dia depois da glosa, aplicadas só às glosas em aberto até setembro. O que já chegou acima da curva não é projetado de novo.</li>
    <li><b>Teste:</b> no dia 22 de cada mês, o real ficou entre 0 e 2,5 vezes o projetado (jul 2,5 · ago 2,0 · set 0). Em nove dias, quase tudo depende de a DASA mandar ou não a coorte de setembro. Com a mediana atual dela (53 dias), o lote cai entre 31/10 e meados de novembro.</li>
  </ul>
</section>

<section>
  <h2>8. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Fleury em novembro:</b> a coorte de setembro tem R$ 880 mil glosados. No ritmo de agosto (54%), seriam ~R$ 475 mil de recurso entre 10 e 20/11. Vale entender com o Fleury o que mudou (equipe, sistema, prioridade) e se 7G9 e 7EY vão seguir sendo recursados.</li>
      <li><b>DASA:</b> coorte de setembro (R$ 505 mil glosados) deve chegar entre 31/10 e meados de novembro.</li>
      <li><b>Data incorreta (7F6):</b> R$ 631 mil glosados em 22 dias de outubro. Entender o que mudou na regra ou no faturamento antes que o recurso chegue.</li>
      <li><b>Capacidade de análise:</b> com ~8,6 mil itens em outubro e uma onda maior prevista para novembro, vale dimensionar o time de análise com antecedência.</li>
    </ol>
  </div>
  <p class="small muted">Relatórios anteriores: <a href="https://claude.ai/artifact/9mDGecRHioDCKkpKHeFFhc" target="_blank" rel="noopener">Recurso de Glosa em Outubro: Laboratórios e Clínicas</a> · <a href="https://claude.ai/artifact/BnYkCCrfqa5Nr7ruyfoeQA" target="_blank" rel="noopener">Regra de Duplicidade</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 22/10. Não é tempo real.</p>
</section>
"""

HOSP = r"""
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Deep dive · Hospitais · Out/26</span>
  <h1>Por que o recurso de hospitais subiu em outubro</h1>
  <p class="muted">Leitura do mês com dados até 22/10: quanto subiu, quais hospitais puxaram, em quais motivos e como mudou a janela entre a glosa e o recurso.</p>
  <div class="scope">""" + SCOPE + r"""</div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Quanto subiu?</span>
      <span class="pill bad">Já é o maior mês do ano</span>
      <span class="a">R$ 1,19 mi · 1.429 itens · 153 PEGs até 22/10</span>
      <p>A projeção fecha o mês em ~R$ 1,43 mi (faixa de R$ 1,33 a 1,48 mi), ~1,8 mil itens e ~200 PEGs. O maior mês até então era setembro (R$ 960 mil). Em itens, outubro fica no nível de agosto; os PEGs ficam um pouco acima. O que mais sobe é o valor por PEG.</p>
    </div>
    <div class="v">
      <span class="q">Em qual motivo?</span>
      <span class="pill warn">Autorização (esperado) e conta não localizada no capeante</span>
      <span class="a">7F8 R$ 557 mil · 7DJ R$ 263 mil</span>
      <p>O 7F8 segue no patamar alto de agosto e setembro, como esperado. O que é novo é o 7DJ: de R$ 30 mil em setembro para R$ 263 mil (HCor R$ 109 mil, Santa Joana R$ 95 mil e Américas R$ 43 mil).</p>
    </div>
    <div class="v">
      <span class="q">Como ficou a janela?</span>
      <span class="pill bad">33% do valor fora do prazo</span>
      <span class="a">R$ 401 mil com mais de 60 dias</span>
      <p>Em agosto e setembro, eram 7%. HCor (R$ 201 mil, 62–89 dias), Einstein (R$ 98 mil), Santa Marcelina, SMA e Albert Sabin mandaram glosas de julho e agosto. Ao mesmo tempo, o recurso em até 15 dias da glosa caiu de 34–48% para 12%: Sírio e HAOC ficaram mais lentos.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Volume por mês</h2>
  <p class="muted">Valor recursado por mês de recebimento. A barra de outubro mostra o real até 22/10 e, hachurada, a projeção de 23 a 31/10.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--accent)"></i>Valor recebido (R$ mil)</span><span><i class="proj"></i>Projeção 23–31/10</span></div>
    <div id="chVol"></div>
    <div class="tbl-wrap"><table id="tVol"></table></div>
  </div>
</section>

<section>
  <h2>2. Hospitais</h2>
  <div class="panel tbl-wrap">
    <h3>Outubro até 22/10</h3>
    <table>
      <thead><tr><th>Hospital</th><th>Valor</th><th>Itens</th><th>PEGs</th><th>Coortes</th><th>Dias até o recurso</th><th>Mais de 60 dias</th><th>Acato (analisado)</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr class="hl"><td>HCor</td><td>R$ 201 mil</td><td>372</td><td>23</td><td>jul, ago</td><td>62–89</td><td>R$ 201 mil</td><td>13%</td><td class="wrap-cell">Tudo fora do prazo. 7DJ de julho (R$ 109 mil), 7E1 e 7F8 de agosto</td></tr>
        <tr><td>Américas</td><td>R$ 172 mil</td><td>89</td><td>12</td><td>ago, set</td><td>21–58</td><td>–</td><td>47%</td><td class="wrap-cell">No padrão dele. 7EL (R$ 50 mil), 7DJ (R$ 43 mil) e 7F8</td></tr>
        <tr><td>CIP Pacaembu</td><td>R$ 168 mil</td><td>12</td><td>1</td><td>set</td><td>21</td><td>–</td><td>95%</td><td class="wrap-cell">Um PEG de valor alto (7F8), comportamento de sempre</td></tr>
        <tr><td>Sírio</td><td>R$ 122 mil</td><td>208</td><td>9</td><td>out</td><td>3–14</td><td>–</td><td>–</td><td class="wrap-cell">No próprio mês, mas mais devagar (mediana de 10 dias, contra 3–5)</td></tr>
        <tr class="hl"><td>Einstein</td><td>R$ 118 mil</td><td>70</td><td>13</td><td>jul, ago</td><td>45–87</td><td>R$ 98 mil</td><td>21%</td><td class="wrap-cell">Recursava pouco. Agora recursa tarde</td></tr>
        <tr class="hl"><td>Santa Joana</td><td>R$ 95 mil</td><td>137</td><td>2</td><td>ago</td><td>54–62</td><td>R$ 11 mil</td><td>0%</td><td class="wrap-cell">Todo 7DJ (conta não localizada no capeante). Tudo negado até agora</td></tr>
        <tr><td>HAOC</td><td>R$ 66 mil</td><td>68</td><td>9</td><td>ago, set</td><td>21–53</td><td>–</td><td>21%</td><td class="wrap-cell">Mais lento que antes (mediana de 25 dias, contra 5–6)</td></tr>
        <tr><td>Santa Marcelina</td><td>R$ 64 mil</td><td>43</td><td>4</td><td>jul, ago</td><td>49–74</td><td>R$ 35 mil</td><td>100%</td><td class="wrap-cell">7F8, incluindo segundo recurso de julho</td></tr>
        <tr><td>SAHA · SMA · Albert Sabin</td><td>R$ 81 mil</td><td>59</td><td>~15</td><td>jul–set</td><td>28–82</td><td>R$ 40 mil</td><td>–</td><td class="wrap-cell">SMA e Albert Sabin fora do prazo</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Como cada um recursa: mediana de dias por mês de recebimento</h3>
    <table>
      <thead><tr><th>Hospital</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th></tr></thead>
      <tbody>
        <tr><td>Sírio</td><td>3</td><td>0</td><td>3</td><td>5</td><td><b>10</b></td></tr>
        <tr><td>HAOC</td><td>6</td><td>0</td><td>6</td><td>5</td><td><b>25</b></td></tr>
        <tr><td>Américas</td><td>31</td><td>44</td><td>50</td><td>56</td><td>56</td></tr>
        <tr class="hl"><td>HCor</td><td>58</td><td>31</td><td>65</td><td>81</td><td><b>64 · 100% &gt;60</b></td></tr>
        <tr class="hl"><td>Einstein</td><td>48</td><td>42</td><td>29</td><td>–</td><td><b>61 · 83% &gt;60</b></td></tr>
        <tr><td>CIP Pacaembu</td><td>–</td><td>41</td><td>56</td><td>21</td><td>21</td></tr>
        <tr><td>Santa Joana</td><td>32</td><td>46</td><td>56</td><td>97</td><td>54</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>3. Janela de envio: mais recurso tardio, menos recurso imediato</h2>
  <p class="muted">Distribuição do valor recebido no mês pelos dias entre a glosa e o recurso. Laranja = mais de 60 dias.</p>
  <div class="panel">
    <div class="legend" id="lgWin"></div>
    <div id="chWin"></div>
    <div class="tbl-wrap"><table id="tWin"></table></div>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill bad">Fora do prazo</span><h3>33% do valor chegou depois de 60 dias</h3>
      <p>R$ 401 mil e 596 itens, contra 3–7% em agosto e setembro. Só julho teve algo parecido (37%), com o Santa Catarina e o GSH.</p></div>
    <div class="panel prov"><span class="pill warn">Mais lento</span><h3>Recurso em até 15 dias caiu para 12%</h3>
      <p>Em agosto e setembro, 34–48% do valor chegava em até 15 dias da glosa, puxado por Sírio e HAOC. Em outubro, os dois levaram mais tempo (mediana de 10 e 25 dias).</p></div>
    <div class="panel prov"><span class="pill good">Sinal positivo</span><h3>O tardio está sendo negado</h3>
      <p>Nos demais motivos (sem autorização), só 24% do valor analisado em outubro foi acatado, contra 32–46% em agosto e setembro. HCor (13%), Santa Joana (0%) e Einstein (21%) puxam a queda. A autorização segue com 84%.</p></div>
  </div>
</section>

<section>
  <h2>4. Motivos</h2>
  <div class="panel tbl-wrap">
    <h3>Valor recursado por motivo e mês de recebimento (R$ mil · itens)</h3>
    <table>
      <thead><tr><th>Motivo</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out (01–22)</th><th>Quem puxa em outubro</th></tr></thead>
      <tbody>
        <tr><td>7F8 · autorização</td><td>–</td><td>12 · 65</td><td>342 · 641</td><td>755 · 967</td><td><b>557 · 791</b></td><td class="wrap-cell">CIP, Sírio, Américas, Santa Marcelina, HCor</td></tr>
        <tr class="hl"><td>7DJ · conta não localizada no capeante</td><td>212 · 83</td><td>181 · 178</td><td>82 · 109</td><td>30 · 28</td><td><b>263 · 191</b></td><td class="wrap-cell">HCor R$ 109 mil, Santa Joana R$ 95 mil, Américas R$ 43 mil</td></tr>
        <tr><td>7EL · código diferente do autorizado</td><td>1 · 1</td><td>1 · 1</td><td>13 · 4</td><td>20 · 2</td><td><b>87 · 14</b></td><td class="wrap-cell">Américas e CIP</td></tr>
        <tr><td>7E1 · valor divergente do negociado</td><td>16 · 96</td><td>20 · 60</td><td>18 · 180</td><td>26 · 37</td><td><b>70 · 241</b></td><td class="wrap-cell">HCor e GNDI</td></tr>
        <tr><td>7F7 · fora do prazo contratual</td><td>–</td><td>–</td><td>–</td><td>–</td><td>32 · 5</td><td class="wrap-cell">Einstein</td></tr>
        <tr><td>7G1 · sem cobertura do plano</td><td>–</td><td>–</td><td>–</td><td>–</td><td>30 · 23</td><td class="wrap-cell">Einstein</td></tr>
      </tbody>
    </table>
    <p class="small muted">Em agosto, o 7DL (autorização, tabela antiga) ainda somava R$ 246 mil. O código é o primeiro motivo do item.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill flat">Esperado</span><h3>Autorização segue no patamar alto</h3>
      <p>R$ 557 mil até 22/10 e ~R$ 680 mil projetados no mês, entre agosto (R$ 588 mil) e setembro (R$ 755 mil). O acato continua em 84%.</p></div>
    <div class="panel prov"><span class="pill bad">Novo</span><h3>7DJ voltou com força, e tarde</h3>
      <p>Conta não localizada no capeante saltou para R$ 263 mil. HCor e Santa Joana recursaram glosas de julho e agosto, a maior parte fora do prazo, e até agora quase tudo foi negado. Vale olhar se o capeante está chegando incompleto na origem.</p></div>
  </div>
</section>

<section>
  <h2>5. Projeção de fechamento</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Valor</th><th>Itens</th><th>PEGs</th></tr></thead>
      <tbody>
        <tr><td>Real 01–22/10</td><td>R$ 1.191 mil</td><td>1.429</td><td>153</td></tr>
        <tr><td>Glosas em aberto até setembro (CIP, Américas, HCor e outros)</td><td>R$ 148 mil</td><td>~190</td><td>~30</td></tr>
        <tr><td>Glosas de outubro de quem recursa no próprio mês (Sírio, HAOC, HCor)</td><td>R$ 92 mil</td><td>~160</td><td>~19</td></tr>
        <tr class="hl"><td><b>Fechamento estimado</b></td><td><b>~R$ 1,43 mi</b></td><td><b>~1,8 mil</b></td><td><b>~200</b></td></tr>
        <tr><td>Faixa pelo teste do método</td><td>R$ 1,33–1,48 mi</td><td>–</td><td>–</td></tr>
      </tbody>
    </table>
  </div>
  <ul class="plain">
    <li><b>Método:</b> curvas por hospital e motivo do % do glosado que chega a cada dia depois da glosa, incluindo as glosas do próprio mês (29% do recurso de hospitais costuma chegar no mesmo mês).</li>
    <li><b>Teste:</b> no dia 22 de cada mês, o real ficou entre 0,57 e 1,21 vez o projetado (jul 0,57 · ago 1,21 · set 0,83).</li>
  </ul>
</section>

<section>
  <h2>6. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Prazo de 60 dias:</b> R$ 401 mil de outubro chegaram fora do prazo. Confirmar que estão sendo negados por prazo, e não só por mérito, e registrar o critério.</li>
      <li><b>HCor:</b> R$ 201 mil fora do prazo, glosas de julho e agosto. Conversar sobre o atraso e sobre o 7DJ (capeante).</li>
      <li><b>Santa Joana:</b> 137 itens de 7DJ, todos negados até agora. Entender se há falha recorrente no envio do capeante.</li>
      <li><b>Sírio e HAOC mais lentos:</b> se mantiverem 10–25 dias, parte do recurso que chegava no próprio mês passa para o mês seguinte.</li>
      <li><b>Autorização (7F8):</b> segue alto e muito acatado (84%). O aumento era esperado, mas o acato alto indica retrabalho dos dois lados.</li>
    </ol>
  </div>
  <p class="small muted">Relatório anterior: <a href="https://claude.ai/artifact/72dEyR4iKQ9AdHxZpncSBT" target="_blank" rel="noopener">Recurso de Glosa em Outubro: Hospitais</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 22/10. Não é tempo real.</p>
</section>
"""
build('L', 'Deep Dive Recurso Laboratórios', LABS, (135, 1464, 99), 'deep-dive-laboratorios.html')
build('H', 'Deep Dive Recurso Hospitais', HOSP, (240, 345, 49), 'deep-dive-hospitais.html')
