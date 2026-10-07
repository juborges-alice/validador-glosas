import sys, json
sys.path.insert(0, '../../aumento-recurso-outubro/relatorios')
from common import page
procs = json.load(open('procsD.json'))
rows = "\n".join(
    f"<tr><td>{p['cod']}</td><td class=\"wrap-cell\">{p['nome'].title()}</td><td>{', '.join(g.title() for g in p['grupos']) or 'Outros'}</td>"
    f"<td>{p['itens']}</td><td>{p['glosa']/1e3:.1f}</td><td>{p['acato']}%</td><td>{p['teto']}</td><td>{p['deixa']/1e3:.1f}</td><td><b>{p['perdido']/1e3:.1f}</b></td></tr>"
    for p in procs).replace('.', ',').replace('class=\"wrap-cell\"', 'class="wrap-cell"')
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Regra de duplicidade · Laboratórios e clínicas</span>
  <h1>Regra de Duplicidade: vale flexibilizar?</h1>
  <p class="muted">A glosa por duplicidade (7G4 desde julho, 7DX e 7DY antes) gera muito recurso, e a maior parte dele é acatada. Este relatório mede quanto a regra rende de fato e simula quanto se perderia ao deixar de glosar os casos que hoje quase sempre voltam, contando também o que nunca foi recursado.</p>
  <div class="scope">
    <span class="chip">Laboratório + Clínica · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Coortes de glosa de mai, jun e jul/26 (maduras)</span>
    <span class="chip">Dados até 06/10/2026</span>
    <span class="chip">Execuções (N) = quantidade do procedimento para o mesmo membro no mesmo dia</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">A regra funciona?</span>
      <span class="pill warn">Quando o procedimento aparece 2 vezes, sim. A partir de 3, quase nunca</span>
      <span class="a">Acato de 4% com N = 2, de 95–100% com N ≥ 3</span>
      <p>Com duas execuções no dia, a glosa quase sempre se sustenta: 288 recursos negados e 12 acatados. A partir de três, são procedimentos cobrados por unidade (IgE por alérgeno, marcadores tumorais, RM por articulação) e o recurso volta acatado em quase todos os casos.</p>
    </div>
    <div class="v">
      <span class="q">Quanto a regra rende hoje?</span>
      <span class="pill flat">Saving real de ~R$ 101 mil por mês</span>
      <span class="a">R$ 610 mil glosados, R$ 304 mil de saving em 3 meses</span>
      <p>Metade do que é glosado por duplicidade volta acatado. De mai a jul, R$ 307 mil foram devolvidos e 1.846 itens passaram pela análise de recurso.</p>
    </div>
    <div class="v">
      <span class="q">Quanto custaria flexibilizar?</span>
      <span class="pill good">Pouco, com a regra certa</span>
      <span class="a">~R$ 16–32 mil de saving por mês</span>
      <p>Deixar de glosar N ≥ 3 nos 42 procedimentos com acato alto (cenário D) custaria R$ 48 mil em três meses, 16% do saving. Em troca, sairiam ~1.050 recursos da fila e R$ 208 mil que hoje são glosados e devolvidos.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. O acato depende de quantas vezes o procedimento aparece</h2>
  <p class="muted">% acatado do recurso analisado, por número de execuções do procedimento para o mesmo membro no mesmo dia. Coortes de mai a jul.</p>
  <div class="panel">
    <div id="chN"></div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>N no dia</th><th>Itens glosados</th><th>Glosado</th><th>Acatados</th><th>Negados</th><th>Acato</th></tr></thead>
      <tbody>
        <tr class="hl"><td>2</td><td>1.923</td><td>R$ 195 mil</td><td>12</td><td>288</td><td><b>4%</b></td></tr>
        <tr><td>3</td><td>783</td><td>R$ 161 mil</td><td>583</td><td>13</td><td>98%</td></tr>
        <tr><td>4</td><td>302</td><td>R$ 60 mil</td><td>208</td><td>3</td><td>99%</td></tr>
        <tr><td>5</td><td>221</td><td>R$ 25 mil</td><td>127</td><td>7</td><td>95%</td></tr>
        <tr><td>6</td><td>249</td><td>R$ 58 mil</td><td>159</td><td>1</td><td>99%</td></tr>
        <tr><td>7 a 9</td><td>265</td><td>R$ 48 mil</td><td>154</td><td>0</td><td>100%</td></tr>
        <tr><td>10 ou mais</td><td>377</td><td>R$ 56 mil</td><td>242</td><td>9</td><td>96%</td></tr>
      </tbody>
    </table></div>
    <p class="small muted">Itens com N = 1 (76, R$ 9 mil) ficaram de fora do gráfico: são casos em que a repetição está fora do mesmo dia.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Duplicidade real</span><h3>Dois itens iguais no mesmo dia</h3>
      <p>1.017 itens e R$ 139 mil. Pouco recursado (248) e quase sempre negado (238). Também entra aqui a quantidade 2 dentro do próprio item: 982 itens, R$ 65 mil, 88 de 92 recursos negados.</p></div>
    <div class="panel prov"><span class="pill bad">Glosa que volta</span><h3>Três ou mais itens no mesmo dia</h3>
      <p>2.114 itens e R$ 369 mil. 1.504 foram recursados e 1.473 acatados (98%). É aqui que está o retrabalho da regra.</p></div>
    <div class="panel prov"><span class="pill flat">Exceção</span><h3>Quantidade alta dentro de um item só</h3>
      <p>83 itens com N ≥ 3 em um único item (R$ 39 mil). Só 2 foram recursados, e os dois foram negados. A glosa se sustenta.</p></div>
  </div>
</section>

<section>
  <h2>2. Cenários de flexibilização</h2>
  <p class="muted">Em cada cenário, o item deixa de ser glosado. O saving perdido inclui tudo: o que nunca foi recursado, o que foi negado e a parte esperada dos recursos ainda em análise. O que hoje volta acatado não é perda.</p>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Cenário (mai–jul)</th><th>Deixa de glosar</th><th>Já voltava acatado</th><th>Saving perdido</th><th>Por mês</th><th>% do saving</th><th>Recursos evitados</th></tr></thead>
      <tbody>
        <tr class="hl"><td class="wrap-cell"><b>D) Não glosar N ≥ 3 nos 42 procedimentos com acato ≥ 80% (mín. 5 analisados)</b></td><td>R$ 256 mil</td><td>R$ 208 mil</td><td><b>R$ 48 mil</b></td><td>~R$ 16 mil</td><td>16%</td><td>1.046 de 1.846</td></tr>
        <tr><td class="wrap-cell">B) Teto por procedimento: não glosar de N = 3 até o maior N já acatado</td><td>R$ 371 mil</td><td>R$ 307 mil</td><td>R$ 64 mil</td><td>~R$ 21 mil</td><td>21%</td><td>1.506 de 1.846</td></tr>
        <tr><td class="wrap-cell">Não glosar nenhum N ≥ 3</td><td>R$ 408 mil</td><td>R$ 307 mil</td><td>R$ 101 mil</td><td>~R$ 34 mil</td><td>33%</td><td>1.506 de 1.846</td></tr>
        <tr><td class="wrap-cell">Teto por procedimento incluindo N = 2 (proposta inicial)</td><td colspan="6" class="wrap-cell">Perde 64% do saving de julho: o teto de quase todo procedimento fica em 3 ou mais, então a regra deixa de pegar também a duplicidade real.</td></tr>
      </tbody>
    </table>
    <p class="small muted">Não glosar nenhum N ≥ 3 libera casos que hoje estão corretos, como sessões de psicologia e consultas de nutrição (R$ 23 mil de um único prestador) e TC de crânio.</p>
  </div>
</section>

<section>
  <h2>3. Cenário D mês a mês</h2>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s1)"></i>Já voltava acatado</span><span><i style="background:var(--s2)"></i>Saving perdido</span></div>
    <div id="chD"></div>
    <div class="tbl-wrap"><table>
      <thead><tr><th>Mês da glosa</th><th>Deixa de glosar</th><th>Já voltava acatado</th><th>Não recursado</th><th>Saving perdido</th><th>Saving do mês</th><th>Recursos evitados</th></tr></thead>
      <tbody>
        <tr><td>Mai (7DX/7DY)</td><td>87 itens · R$ 23,6 mil</td><td>R$ 20,0 mil</td><td>6 itens · R$ 2,2 mil</td><td><b>R$ 3,6 mil</b></td><td>R$ 64,9 mil (6%)</td><td>81 de 269</td></tr>
        <tr><td>Jun (7DX/7DY)</td><td>454 itens · R$ 82,1 mil</td><td>R$ 69,5 mil</td><td>64 itens · R$ 11,4 mil</td><td><b>R$ 12,6 mil</b></td><td>R$ 126,4 mil (10%)</td><td>390 de 767</td></tr>
        <tr class="hl"><td>Jul (7G4)</td><td>662 itens · R$ 150,6 mil</td><td>R$ 118,7 mil</td><td>87 itens · R$ 31,0 mil</td><td><b>R$ 31,9 mil</b></td><td>R$ 112,4 mil (28%)</td><td>575 de 810</td></tr>
        <tr><td><b>Total</b></td><td><b>1.203 itens · R$ 256 mil</b></td><td><b>R$ 208 mil</b></td><td><b>157 itens · R$ 44,7 mil</b></td><td><b>R$ 48,1 mil</b></td><td><b>R$ 303,7 mil (16%)</b></td><td><b>1.046 de 1.846</b></td></tr>
      </tbody>
    </table></div>
  </div>
  <div class="panel">
    <h3>Previsão</h3>
    <p>Julho é o único mês já com a regra 7G4, que tem o dobro do volume dos códigos antigos. Com o 7G4 glosando R$ 200–270 mil por mês (jul–set), o cenário D deve custar <b>R$ 25–32 mil de saving por mês</b>. Em troca, tira <b>~550–600 itens por mês</b> da fila de recurso e deixa de glosar ~R$ 115 mil por mês que hoje voltam acatados.</p>
  </div>
</section>

<section>
  <h2>4. Onde está o impacto</h2>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">Maior impacto</span><h3>DASA</h3><p>R$ 340 mil glosados por duplicidade e R$ 143 mil de saving em mai–jul. No cenário D, perderia R$ 37,8 mil de saving.</p></div>
    <div class="panel prov"><span class="pill flat">Impacto menor</span><h3>Fleury</h3><p>R$ 181 mil glosados e R$ 117 mil de saving. No cenário D, perderia R$ 10,1 mil.</p></div>
    <div class="panel prov"><span class="pill good">Quase nada a perder</span><h3>Femme</h3><p>R$ 41 mil glosados, mas só R$ 3,7 mil de saving: recursa e tem acato em quase tudo. No cenário D, perderia R$ 0,2 mil.</p></div>
  </div>
</section>

<section>
  <h2>5. Os 42 procedimentos do cenário D</h2>
  <p class="muted">Procedimentos com acato de pelo menos 80% em pelo menos 5 recursos analisados, em mai–jul. "Teto" é o maior N já acatado; serve de referência para o cenário B. Ordenados pelo valor que deixaria de ser glosado.</p>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Código</th><th>Procedimento</th><th>Prestadores</th><th>Itens glosados</th><th>Glosado (R$ mil)</th><th>Acato</th><th>Teto (N)</th><th>Deixa de glosar (R$ mil)</th><th>Saving perdido (R$ mil)</th></tr></thead>
      <tbody>
""" + rows + r"""
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>6. Cuidados antes de mudar a regra</h2>
  <div class="panel">
    <ul class="plain">
      <li><b>Mesma base para definir e testar.</b> A lista de procedimentos e os tetos saem dos mesmos dados usados na simulação. O número de recursos evitados tende a ser otimista.</li>
      <li><b>Adaptação dos prestadores.</b> Com a regra mais flexível, a cobrança pode subir até o limite. Vale acompanhar o N médio por procedimento depois da mudança.</li>
      <li><b>Prazo de recurso.</b> As coortes de mai a jul têm de 69 a 150 dias. Alguns prestadores ainda recursam tarde, então o "não recursado" pode diminuir um pouco e a perda seria menor.</li>
      <li><b>Premissas da conta.</b> Parcialmente acatado conta como acatado. Recursos ainda em análise entram com 89% de acato, a taxa do período. Hospitais e o 7G3 (duplicidade de conta parcial) ficaram de fora.</li>
    </ul>
  </div>
</section>

<section>
  <h2>7. Próximos passos sugeridos</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Validar a lista com o time de regras:</b> confirmar que os 42 procedimentos são cobrados por unidade (alérgeno, marcador, articulação, segmento).</li>
      <li><b>Implementar o cenário D,</b> mantendo a glosa para N = 2 e para quantidade alta dentro de um item só.</li>
      <li><b>Medir por 2–3 meses</b> o saving, a glosa e o volume de recurso de duplicidade, comparando com esta linha de base (~R$ 101 mil de saving e ~615 recursos por mês).</li>
    </ol>
  </div>
  <p class="small muted">Relatórios relacionados: <a href="https://claude.ai/artifact/9mDGecRHioDCKkpKHeFFhc" target="_blank" rel="noopener">Recurso de Glosa em Outubro: Laboratórios e Clínicas</a> · <a href="https://claude.ai/artifact/72dEyR4iKQ9AdHxZpncSBT" target="_blank" rel="noopener">Recurso de Glosa em Outubro: Hospitais</a>. Fonte: <code>curated.totvs_procedure_invoice</code>.</p>
</section>
"""
data = r"""
const N = [["2",4,12,288],["3",98,583,13],["4",99,208,3],["5",95,127,7],["6",99,159,1],["7–9",100,154,0],["10+",96,242,9]];
bars("chN", N.map(n => ({label: "N = " + n[0], v: n[1], tipx: `<b>N = ${n[0]}</b><br>Acatados: ${n[2]}<br>Negados: ${n[3]}<br>Acato: ${n[1]}%`})), v => nf(v) + "%", "Acato do recurso por número de execuções no dia", "var(--s2)");
(function(){
  const M = [["mai",20.0,3.6],["jun",69.5,12.6],["jul",118.7,31.9]];
  const W = 680, H = 230, L = 52, R = 10, T = 24, B = 30, pw = W-L-R, ph = H-T-B, max = 160;
  const y = v => T + ph - v/max*ph, band = pw/M.length, bw = Math.min(64, band*0.5);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Cenário D por mês: acatado e saving perdido">`;
  for (let i=0;i<=4;i++){ const v=max*i/4; s += `<line class="grid" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text x="${L-8}" y="${y(v)+4}" text-anchor="end">${nf(v)}</text>`; }
  M.forEach((m,i) => {
    const x = L + band*i + band/2 - bw/2, t = m[1]+m[2];
    s += `<rect x="${x}" y="${y(m[1])}" width="${bw}" height="${y(0)-y(m[1])}" fill="var(--s1)"/>`;
    s += `<path d="${rpath(x, y(t), bw, y(m[1])-y(t)-2, 4)}" fill="var(--s2)"/>`;
    s += `<text class="val" x="${x+bw/2}" y="${y(t)-7}" text-anchor="middle">R$ ${nf(m[2],1)} mil perdido</text><text x="${x+bw/2}" y="${H-8}" text-anchor="middle">${m[0]}</text>`;
    s += `<rect class="hit" x="${L+band*i}" y="${T}" width="${band}" height="${ph}" data-tip="<b>${m[0]}/26</b><br>Deixa de glosar: R$ ${nf(t,1)} mil<br>Já voltava acatado: R$ ${nf(m[1],1)} mil<br>Saving perdido: R$ ${nf(m[2],1)} mil"/>`;
  });
  s += `</svg>`; const el = document.getElementById("chD"); el.innerHTML = s; bindTips(el);
})();
"""
open('regra-duplicidade.html','w').write(page("Regra de Duplicidade", body, data))
