from common import page
body = r"""
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Laboratórios e clínicas · Out/26</span>
  <h1>Recurso de Glosa em Outubro: Laboratórios e Clínicas</h1>
  <p class="muted">Em outubro, o recurso de laboratórios voltou a subir logo nos primeiros dias, depois do vale de setembro. Este relatório mostra o tamanho da alta em valor, itens e PEG, de onde ela vem, como fica o motivo de falta de autorização e o que mudou desde a análise da queda de setembro.</p>
  <div class="scope">
    <span class="chip">Laboratório + Clínica · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 06/10/2026</span>
    <span class="chip">Sem o lote antigo da DASA (glosas de 2025, recebidas 22–30/09)</span>
    <span class="chip">Sem os recursos de 7F6 de jul–ago</span>
    <span class="chip">Autorização = 7DL (até jun) e 7F8 (desde jul)</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Outubro está fora do normal?</span>
      <span class="pill good">Não. Volta ao patamar de jul–ago</span>
      <span class="a">~R$ 690 mil · ~5,1 mil itens · ~390 PEGs</span>
      <p>Até 06/10 entraram R$ 262 mil, 978 itens e 160 PEGs. Pela projeção, o mês fecha perto de julho e agosto (R$ 717–907 mil, 5,5–5,7 mil itens, 381–432 PEGs). O pico dos primeiros dias é a DASA entregando de uma vez as glosas de agosto.</p>
    </div>
    <div class="v">
      <span class="q">O recurso por falta de autorização voltou a subir?</span>
      <span class="pill good">Não. Segue em queda</span>
      <span class="a">~R$ 153 mil no mês, contra ~R$ 267 mil (média de abr–ago)</span>
      <p>A glosa desse motivo caiu de 2,8–4,5% para 1,3–1,5% do apresentado desde julho, e ficou nesse nível. O % recursado não mudou (30–34% em até 60 dias). Com a base menor, entra menos recurso: ~22% do recurso de outubro, contra 32–48% antes.</p>
    </div>
    <div class="v">
      <span class="q">Por que setembro caiu e outubro subiu?</span>
      <span class="pill flat">Calendário de entrega</span>
      <span class="a">A coorte de agosto caiu em outubro</span>
      <p>A DASA costumava recursar em 42–44 dias. As glosas de agosto, feitas em sua maioria entre 11 e 20/08, eram esperadas de 22/09 a 01/10, mas chegaram em 05–06/10 (mediana de 54 dias), na taxa de sempre (57% do glosado). Setembro ficou sem esse lote e outubro recebeu tudo junto.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Valor recebido por mês</h2>
  <p class="muted">Valor recursado (R$ mil), por mês de recebimento do recurso. A barra de outubro mostra o real de 01 a 06/10 e, hachurada, a projeção de 07 a 31/10.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chVal"></div>
    <div class="tbl-wrap"><table id="tVal"></table></div>
  </div>
</section>

<section>
  <h2>2. Itens recebidos para análise</h2>
  <p class="muted">Itens recursados (itens distintos de guia), por mês de recebimento. Esta é a medida de carga de trabalho do time de análise.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chItem"></div>
    <div class="tbl-wrap"><table id="tItem"></table></div>
  </div>
</section>

<section>
  <h2>3. Recurso por protocolo (PEG)</h2>
  <p class="muted">PEGs distintos com recurso recebido no mês, com o tamanho médio de cada PEG. Outubro teve PEGs pequenos: a DASA abre um PEG por protocolo original, com cerca de 6 itens cada.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--accent)"></i>PEGs recebidos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chPeg"></div>
    <div class="tbl-wrap"><table id="tPeg"></table></div>
    <p class="small muted">A projeção de PEGs divide os itens projetados de cada prestador pela média de itens por PEG dele em mar–set (DASA ~8, Fleury ~20, Femme ~40). É uma estimativa aproximada.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">156 de 160 PEGs</span><h3>DASA</h3>
      <p>R$ 249 mil e 952 itens em 05–06/10, todos de glosas de 06 a 26/08. São PEGs de 1 a 58 itens. O maior é o 00103281 (58 itens, R$ 13 mil, motivo 7G9).</p></div>
    <div class="panel prov"><span class="pill flat">4 PEGs</span><h3>Fleury</h3>
      <p>R$ 13 mil e 26 itens de glosas de agosto. A coorte de agosto do Fleury (R$ 783 mil glosados) entra na janela dele de meados de outubro ao início de novembro.</p></div>
    <div class="panel prov"><span class="pill flat">0 PEG até 06/10</span><h3>Femme</h3>
      <p>Recursa ~80% do que é glosado, em PEGs grandes (~40 itens). As coortes de agosto e setembro ainda não chegaram e devem trazer ~1.250 itens de baixo valor.</p></div>
  </div>
</section>

<section>
  <h2>4. Motivos: falta de autorização segue em queda</h2>
  <p class="muted">Glosa por autorização não localizada, em % do valor apresentado, por mês da glosa. Em julho, o 7DL deixou de ser usado e o motivo passou a sair como 7F8.</p>
  <div class="panel">
    <h3>Glosa de autorização em % do apresentado</h3>
    <div id="chGlA"></div>
    <div class="tbl-wrap"><table id="tGlA"></table></div>
    <p class="small muted">% do apresentado = glosado no mês da glosa ÷ apresentado no mês da conta. Coortes de agosto e setembro ainda abertas para recurso.</p>
  </div>
  <div class="panel tbl-wrap">
    <h3>Motivos mais recursados por mês de recebimento (R$ mil · itens)</h3>
    <table>
      <thead><tr><th>Mês</th><th>1º</th><th>2º</th><th>3º</th><th>4º</th></tr></thead>
      <tbody>
        <tr><td>Jul</td><td>7DL 439 · 1.642</td><td>7EK 188 · 1.232</td><td>7EY 72 · 869</td><td>7DY 42 · 163</td></tr>
        <tr><td>Ago</td><td>7DL 194 · 1.381</td><td>7G4 142 · 693</td><td>7EK 95 · 1.142</td><td>7DY 74 · 474</td></tr>
        <tr><td>Set</td><td>7EK 59 · 157</td><td>7F8 40 · 94</td><td>7G4 21 · 112</td><td>7F6 12 · 384</td></tr>
        <tr class="hl"><td>Out (01–06)</td><td>7G4 93 · 369</td><td>7F8 42 · 101</td><td>7F6 41 · 105</td><td>7EK 37 · 87</td></tr>
      </tbody>
    </table>
    <p class="small muted">7EK: procedimento sem registro de execução · 7EY: senha cancelada · 7DY: item redundante na guia · 7G4: cobrança em duplicidade · 7F6: data preenchida incorretamente. O código é o primeiro motivo do item.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Queda estrutural</span><h3>Menos glosa, mesma taxa de recurso</h3>
      <p>O % recursado em até 60 dias ficou em 30% (abr), 34% (mai), 30% (jun) e 32% (jul). A coorte de agosto está em 17% e ainda não fechou. Nada indica que os laboratórios passaram a recursar mais esse motivo. Volta menos recurso porque a base glosada é 50–60% menor.</p></div>
    <div class="panel prov"><span class="pill warn">Atenção</span><h3>O que ainda é recursado é muito acatado</h3>
      <p>Do recurso de autorização analisado em agosto, 81% foi acatado (61% em julho). A glosa caiu, mas a maior parte do que ainda é glosado e recursado está sendo revertida. Vale olhar se o 7F8 está glosando itens que tinham autorização.</p></div>
    <div class="panel prov"><span class="pill flat">Os demais motivos</span><h3>7G4, 7F6, 7EK e 7G9 puxam outubro</h3>
      <p>Os demais motivos voltam ao nível de jul–ago (~R$ 540 mil e ~4,2 mil itens projetados). A duplicidade (7G4), código novo da tabela de julho, já é o motivo mais recursado da DASA.</p></div>
  </div>
</section>

<section>
  <h2>5. Setembro e outubro: o que a análise anterior previa e o que aconteceu</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Hipótese da análise de setembro</th><th>O que aconteceu em outubro</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr><td class="wrap-cell"><b>A tabela nova reduziu a glosa por autorização não localizada</b></td><td class="wrap-cell">Agosto e setembro ficaram em 1,5% do apresentado (R$ 255–259 mil), contra 2,8–4,5% até junho.</td><td class="wrap-cell"><span class="pill good">Se mantém</span></td></tr>
        <tr><td class="wrap-cell"><b>O % recursado do motivo não mudou; o volume caiu</b></td><td class="wrap-cell">Julho fechou em 32% em até 60 dias. O recurso de autorização em outubro deve ficar ~43% abaixo da média de abr–ago.</td><td class="wrap-cell"><span class="pill good">Se mantém</span></td></tr>
        <tr><td class="wrap-cell"><b>Julho foi recursado antes, em agosto, e sobrou pouco para setembro</b></td><td class="wrap-cell">28% da coorte de julho chegou já em agosto. Setembro recebeu só R$ 150 mil e 936 itens.</td><td class="wrap-cell"><span class="pill good">Confirmada</span></td></tr>
        <tr><td class="wrap-cell"><b>Agosto foi glosado tarde no mês. Acompanhar a DASA até 01/10</b></td><td class="wrap-cell">A DASA recursou toda a coorte de agosto em 05–06/10, uma semana depois da janela. Recursou 57% do glosado, dentro da faixa histórica de 48–65%. O mix de motivos é parecido com o de julho.</td><td class="wrap-cell"><span class="pill good">Explica a alta</span> Atraso de calendário, sem mudança de comportamento</td></tr>
        <tr><td class="wrap-cell"><b>Fleury e Femme só teriam leitura em outubro</b></td><td class="wrap-cell">Ainda não chegaram. As coortes de agosto deles são o maior volume previsto para o resto do mês.</td><td class="wrap-cell"><span class="pill flat">Em aberto</span></td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel">
    <h3>Conclusão</h3>
    <p>Setembro não marcou uma queda de comportamento. Foi um vale de calendário, com três causas:</p>
    <ul class="plain">
      <li>A base que alimentava o mês era menor: a glosa de julho caiu com a tabela nova.</li>
      <li>Parte dessa base já tinha sido recursada em agosto.</li>
      <li>A DASA atrasou em uma semana o lote de agosto, que saiu de setembro e caiu em outubro.</li>
    </ul>
    <p>Outubro não é uma alta nova. É o mesmo comportamento voltando a aparecer no mês. O nível de recurso de laboratórios volta ao de julho e agosto. A exceção é o motivo de autorização, que fica num patamar mais baixo e estável por causa da redução da glosa.</p>
  </div>
</section>

<section>
  <h2>6. Projeção de outubro e grau de confiança</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Valor</th><th>Itens</th><th>PEGs</th></tr></thead>
      <tbody>
        <tr><td>Real 01–06/10</td><td>R$ 262 mil</td><td>978</td><td>160</td></tr>
        <tr><td>Fleury, coorte de agosto</td><td>R$ 199 mil</td><td>~1.530</td><td>~75</td></tr>
        <tr><td>DASA, resto de agosto e coorte de setembro</td><td>R$ 160 mil</td><td>~1.240</td><td>~150</td></tr>
        <tr><td>Femme, agosto e setembro</td><td>R$ 54 mil</td><td>~1.260</td><td>~30</td></tr>
        <tr><td>Demais prestadores</td><td>R$ 17 mil</td><td>~70</td><td>–</td></tr>
        <tr class="hl"><td><b>Fechamento estimado</b></td><td><b>~R$ 690 mil</b></td><td><b>~5,1 mil</b></td><td><b>~390</b></td></tr>
        <tr><td>Se a DASA de setembro ficar para novembro</td><td>~R$ 575 mil</td><td>~4,4 mil</td><td>~300</td></tr>
      </tbody>
    </table>
  </div>
  <ul class="plain">
    <li><b>Método:</b> para cada prestador e motivo, uma curva do % do glosado que costuma chegar a cada dia depois da glosa, com coortes de 2026. Ela é aplicada só às glosas em aberto até setembro, porque laboratórios e clínicas não recursam no mês da glosa (0% no histórico). Se um prestador já recursou acima da curva, nada mais é projetado para aquela coorte.</li>
    <li><b>Teste:</b> com o mesmo método, como se estivéssemos no dia 06 de cada mês, o real ficou entre 0,34 e 2,1 vezes o projetado (jul 2,1 · ago 1,4 · set 0,34). O valor do mês depende de quando cada prestador manda o lote. Por isso, a faixa razoável vai de ~R$ 575 a ~R$ 880 mil.</li>
    <li><b>Dados:</b> data warehouse (<code>curated.totvs_procedure_invoice</code>) atualizado até 06/10. Não é tempo real.</li>
  </ul>
</section>

<section>
  <h2>7. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Fleury, de meados de outubro ao início de novembro:</b> chegada da coorte de agosto (R$ 783 mil glosados), o maior volume previsto.</li>
      <li><b>DASA, do fim de outubro ao início de novembro:</b> coorte de setembro (R$ 505 mil glosados). Se chegar com mais de 50 dias de novo, o prazo dela passou de ~42 para ~54 dias e vale ajustar o planejamento.</li>
      <li><b>Motivo de autorização:</b> com 81% de acato em agosto, levantar uma amostra de 7F8 acatados para ver se a autorização existia na glosa.</li>
      <li><b>Medir por coorte de glosa:</b> no dashboard, a leitura mês a mês mistura coortes e oscila com o calendário de cada prestador. O % recursado em até 60 dias é a métrica estável.</li>
    </ol>
  </div>
  <p class="small muted">Análise anterior: <a href="https://claude.ai/artifact/NsmUzkeco6xeDXkmZEHZZ2" target="_blank" rel="noopener">Queda de Recurso em Setembro</a> · Dashboard: <a href="https://metabase.datalake.alice.tools/dashboard/2774" target="_blank" rel="noopener">Recurso de Glosa no Metabase</a> · Relatório de hospitais publicado à parte.</p>
</section>
"""
data = r"""
const V = [
 {m:"2026-03",a:266.1,o:397.6},{m:"2026-04",a:175.6,o:371.4},{m:"2026-05",a:260.7,o:354.7},{m:"2026-06",a:202.2,o:257.7},
 {m:"2026-07",a:439.1,o:468.2},{m:"2026-08",a:255.6,o:460.9},{m:"2026-09",a:41.7,o:108.8},
 {m:"2026-10",label:"out*",a:43.5,o:218.6,pa:109,po:321}];
const I = [
 {m:"2026-03",a:1232,o:1468},{m:"2026-04",a:733,o:5232},{m:"2026-05",a:1080,o:1578},{m:"2026-06",a:1882,o:2414},
 {m:"2026-07",a:1644,o:3830},{m:"2026-08",a:1765,o:3890},{m:"2026-09",a:126,o:810},
 {m:"2026-10",label:"out*",a:102,o:876,pa:729,po:3359}];
const P = [["2026-03",313,2700,663.7],["2026-04",247,5965,547.0],["2026-05",341,2658,615.4],["2026-06",394,4296,459.9],["2026-07",432,5474,907.2],["2026-08",381,5655,716.5],["2026-09",91,936,150.5],["2026-10",160,978,262.1]];
const AC = {"2026-03":[37,70],"2026-04":[26,23],"2026-05":[78,88],"2026-06":[14,80],"2026-07":[61,94],"2026-08":[81,79],"2026-09":[50,85]};
const G = [["2026-01",371,2053,4.13],["2026-02",387,2742,2.81],["2026-03",373,2777,2.95],["2026-04",424,3054,2.81],["2026-05",626,3762,4.46],["2026-06",519,4345,3.34],["2026-07",204,1163,1.34],["2026-08",255,1729,1.45],["2026-09",259,1772,1.47]];
const R60 = {"2026-04":29.8,"2026-05":33.5,"2026-06":29.9,"2026-07":32.4,"2026-08":"17,1 (aberta)","2026-09":"aberta"};
const fk = v => nf(v);
stacked("chVal", V, "Valor recursado", fk);
stacked("chItem", I, "Itens recursados", v => nf(v));
const head = rows => `<thead><tr><th></th>${rows.map(r=>`<th>${r.label||lab(r.m)}</th>`).join("")}</tr></thead>`;
const sh = r => 100*(r.a+(r.pa||0))/(r.a+r.o+(r.pa||0)+(r.po||0));
document.getElementById("tVal").innerHTML = head(V) + `<tbody>
 <tr><td>Autorização (R$ mil)</td>${V.map(r=>`<td>${nf(r.a+(r.pa||0))}</td>`).join("")}</tr>
 <tr><td>Demais (R$ mil)</td>${V.map(r=>`<td>${nf(r.o+(r.po||0))}</td>`).join("")}</tr>
 <tr><td><b>Total (R$ mil)</b></td>${V.map(r=>`<td><b>${nf(r.a+r.o+(r.pa||0)+(r.po||0))}</b></td>`).join("")}</tr>
 <tr><td>% autorização</td>${V.map(r=>`<td>${nf(sh(r))}%</td>`).join("")}</tr>
 <tr><td>Acato autorização · demais</td>${V.map(r=>`<td>${AC[r.m]?AC[r.m][0]+"% · "+AC[r.m][1]+"%":"em análise"}</td>`).join("")}</tr></tbody>`;
document.getElementById("tItem").innerHTML = head(I) + `<tbody>
 <tr><td>Autorização</td>${I.map(r=>`<td>${nf(r.a+(r.pa||0))}</td>`).join("")}</tr>
 <tr><td>Demais</td>${I.map(r=>`<td>${nf(r.o+(r.po||0))}</td>`).join("")}</tr>
 <tr><td><b>Total</b></td>${I.map(r=>`<td><b>${nf(r.a+r.o+(r.pa||0)+(r.po||0))}</b></td>`).join("")}</tr></tbody>`;
bars("chPeg", P.map(p => ({label: p[0]==="2026-10"?"out*":lab(p[0]), v:p[1], pv: p[0]==="2026-10"?234:0,
  tipx:`<b>${lab(p[0])}/26</b><br>PEGs: ${p[1]}${p[0]==="2026-10"?" (real 01–06) + ~234 projetados":""}<br>Itens por PEG: ${nf(p[2]/p[1],1)}<br>R$ por PEG: ${nf(p[3]/p[1],1)} mil`})), v=>nf(v), "PEGs com recurso por mês");
document.getElementById("tPeg").innerHTML = `<thead><tr><th></th>${P.map(p=>`<th>${p[0]==="2026-10"?"out (01–06)":lab(p[0])}</th>`).join("")}<th>out* proj.</th></tr></thead><tbody>
 <tr><td>PEGs</td>${P.map(p=>`<td>${p[1]}</td>`).join("")}<td>~390</td></tr>
 <tr><td>Itens por PEG</td>${P.map(p=>`<td>${nf(p[2]/p[1],1)}</td>`).join("")}<td>~13</td></tr>
 <tr><td>R$ mil por PEG</td>${P.map(p=>`<td>${nf(p[3]/p[1],1)}</td>`).join("")}<td>~1,8</td></tr></tbody>`;
bars("chGlA", G.map(g => ({label: lab(g[0]), v:g[3], tipx:`<b>${lab(g[0])}/26 · ${g[0]>="2026-07"?"7F8":"7DL"}</b><br>Glosado: R$ ${g[1]} mil<br>Itens: ${nf(g[2])}<br>% do apresentado: ${nf(g[3],2)}%`})), v=>nf(v,1)+"%", "Glosa de autorização em % do apresentado", "var(--s2)");
document.getElementById("tGlA").innerHTML = `<thead><tr><th>Mês da glosa</th>${G.map(g=>`<th>${lab(g[0])}</th>`).join("")}</tr></thead><tbody>
 <tr><td>Código</td>${G.map(g=>`<td>${g[0]>="2026-07"?"7F8":"7DL"}</td>`).join("")}</tr>
 <tr><td>Glosado (R$ mil)</td>${G.map(g=>`<td>${g[1]}</td>`).join("")}</tr>
 <tr><td>Itens glosados</td>${G.map(g=>`<td>${nf(g[2])}</td>`).join("")}</tr>
 <tr><td>% do apresentado</td>${G.map(g=>`<td>${nf(g[3],2)}%</td>`).join("")}</tr>
 <tr><td>% recursado em até 60 dias</td>${G.map(g=>`<td>${R60[g[0]]!==undefined?(typeof R60[g[0]]==="number"?nf(R60[g[0]],1)+"%":R60[g[0]]):"–"}</td>`).join("")}</tr></tbody>`;
"""
open('recurso-labs-outubro.html','w').write(page("Recurso Laboratórios Outubro", body, data))
