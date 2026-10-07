from common import page
body = r"""
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Hospitais · Out/26</span>
  <h1>Recurso de Glosa em Outubro: Hospitais</h1>
  <p class="muted">Em hospitais, outubro começou com R$ 564 mil de recurso em seis dias. Este relatório separa o que é pontual (poucos PEGs de valor alto e recursos fora do prazo) do que é tendência: a glosa e o recurso por falta de autorização vêm subindo desde junho, ao contrário dos laboratórios.</p>
  <div class="scope">
    <span class="chip">Hospital · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 06/10/2026</span>
    <span class="chip">Sem os recursos de 7F6 de jul–ago</span>
    <span class="chip">Autorização = 7DL (até jun) e 7F8 (desde jul)</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Outubro está fora do normal?</span>
      <span class="pill warn">Em valor, sim. Em itens, não</span>
      <span class="a">~R$ 1,34 mi · ~1,3 mil itens · ~210 PEGs</span>
      <p>Até 06/10 entraram R$ 564 mil em só 192 itens e 43 PEGs (R$ 13 mil por PEG, o dobro do habitual). A projeção fecha o mês entre R$ 1,27 e 1,47 mi, acima de jul–set (R$ 0,81–0,96 mi). O volume de itens fica dentro da faixa usual (0,9–1,8 mil).</p>
    </div>
    <div class="v">
      <span class="q">O recurso por falta de autorização está subindo?</span>
      <span class="pill bad">Sim. Tendência oposta à dos laboratórios</span>
      <span class="a">Glosa de 0,3–0,7% para 2,4% do apresentado</span>
      <p>A glosa de autorização em hospitais subiu de R$ 76–254 mil por mês (mar–mai) para R$ 936–945 mil (ago–set). Os hospitais recursam 40–70% dela e 82–92% do recursado é acatado. O recurso desse motivo foi de R$ 588 mil (ago) e R$ 768 mil (set), com ~R$ 665 mil projetados para outubro.</p>
    </div>
    <div class="v">
      <span class="q">O que puxa os primeiros dias de outubro?</span>
      <span class="pill flat">24 PEGs, ~R$ 485 mil</span>
      <span class="a">CIP Pacaembu, Einstein, HCor, Américas e Santa Marcelina</span>
      <p>Um PEG do CIP com R$ 168 mil de 7F8. HCor e Einstein recursando glosas de julho e agosto com 78 a 87 dias, fora do prazo de 60 dias. Um segundo recurso do Santa Marcelina. São R$ 266 mil de recurso chegando com mais de 60 dias da glosa.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Valor recebido por mês</h2>
  <p class="muted">Valor recursado (R$ mil), por mês de recebimento. A barra de outubro mostra o real de 01 a 06/10 e, hachurada, a projeção de 07 a 31/10.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chVal"></div>
    <div class="tbl-wrap"><table id="tVal"></table></div>
  </div>
</section>

<section>
  <h2>2. Itens recebidos para análise</h2>
  <p class="muted">Itens recursados (itens distintos de guia), por mês de recebimento. Em hospitais, o valor por item é alto e oscila muito, então valor e itens contam histórias diferentes.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chItem"></div>
    <div class="tbl-wrap"><table id="tItem"></table></div>
  </div>
</section>

<section>
  <h2>3. Recurso por protocolo (PEG)</h2>
  <p class="muted">PEGs distintos com recurso recebido no mês e o tamanho médio de cada um.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--accent)"></i>PEGs recebidos</span><span><i class="proj"></i>Projeção 07–31/10</span></div>
    <div id="chPeg"></div>
    <div class="tbl-wrap"><table id="tPeg"></table></div>
    <p class="small muted">A projeção de PEGs divide os itens projetados de cada hospital pela média de itens por PEG dele em mar–set. É uma estimativa aproximada.</p>
  </div>
  <div class="panel tbl-wrap">
    <h3>Os PEGs que concentram o valor de outubro (01–06/10)</h3>
    <table>
      <thead><tr><th>Hospital</th><th>PEGs</th><th>Itens</th><th>Valor</th><th>Dias da glosa ao recurso</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr><td>CIP Pacaembu (Fleury)</td><td>1</td><td>12</td><td>R$ 168 mil</td><td>21</td><td class="wrap-cell"><span class="pill flat">Comportamento de sempre</span> Recursa 100% em ~21 dias. A glosa de setembro foi alta: R$ 123 mil de 7F8, com um item de R$ 93 mil.</td></tr>
        <tr><td>Einstein</td><td>13</td><td>70</td><td>R$ 118 mil</td><td>45–87</td><td class="wrap-cell"><span class="pill warn">Mudou</span> Recursava 1–13% do glosado. R$ 98 mil chegaram com mais de 60 dias.</td></tr>
        <tr><td>HCor</td><td>6</td><td>39</td><td>R$ 114 mil</td><td>78–85</td><td class="wrap-cell"><span class="pill warn">Mudou</span> Recursava em 8–31 dias. Glosas de julho por 7DJ (conta não localizada no capeante), todas fora do prazo.</td></tr>
        <tr><td>Américas</td><td>3</td><td>15</td><td>R$ 50 mil</td><td>21</td><td class="wrap-cell"><span class="pill flat">No padrão</span> 7EL, glosas de 10/09.</td></tr>
        <tr><td>Santa Marcelina</td><td>1</td><td>13</td><td>R$ 35 mil</td><td>74</td><td class="wrap-cell"><span class="pill warn">2º recurso</span> 7F8 de 20/07, já recursado antes.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>4. Motivos: a autorização cresce nos hospitais</h2>
  <p class="muted">Glosa por autorização não localizada em hospitais, em % do valor apresentado, por mês da glosa. A alta começa em junho, ainda com o 7DL, e segue com o 7F8.</p>
  <div class="panel">
    <h3>Glosa de autorização em % do apresentado</h3>
    <div id="chGlA"></div>
    <div class="tbl-wrap"><table id="tGlA"></table></div>
  </div>
  <div class="panel tbl-wrap">
    <h3>Autorização por hospital: glosa de jul–set e recurso de jun–out</h3>
    <table>
      <thead><tr><th>Hospital</th><th>Glosado jul · ago · set</th><th>Recursado jun–out</th><th>Acato</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr><td>Sírio</td><td>R$ 94 · 82 · 319 mil</td><td>R$ 499 mil</td><td>74–90%</td><td class="wrap-cell">Recursa quase tudo, no mesmo mês da glosa. Pico em setembro.</td></tr>
        <tr><td>Einstein</td><td>R$ 245 · 140 · 62 mil</td><td>R$ 13 mil</td><td>–</td><td class="wrap-cell">Muita glosa, pouco recurso desse motivo.</td></tr>
        <tr><td>HAOC</td><td>R$ 9 · 225 · 41 mil</td><td>R$ 244 mil</td><td>96–98%</td><td class="wrap-cell">Glosa de agosto recursada e quase toda acatada.</td></tr>
        <tr><td>HCor</td><td>R$ 53 · 101 · 94 mil</td><td>R$ 29 mil</td><td>89%</td><td class="wrap-cell">Recurso ainda baixo. Pode chegar tarde, como os 7DJ.</td></tr>
        <tr><td>Américas</td><td>R$ 21 · 58 · 162 mil</td><td>R$ 156 mil</td><td>93% (ago)</td><td class="wrap-cell">Setembro alto. Recurso esperado ainda em outubro.</td></tr>
        <tr><td>CIP Pacaembu</td><td>R$ 0 · 96 · 123 mil</td><td>R$ 251 mil</td><td>100%</td><td class="wrap-cell">Poucos itens de valor alto, sempre recursados.</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Motivos mais recursados por mês de recebimento (R$ mil · itens)</h3>
    <table>
      <thead><tr><th>Mês</th><th>1º</th><th>2º</th><th>3º</th><th>4º</th></tr></thead>
      <tbody>
        <tr><td>Jul</td><td>7DK 224 · 225</td><td>7DJ 181 · 178</td><td>7DL 169 · 123</td><td>7DQ 74 · 46</td></tr>
        <tr><td>Ago</td><td>7F8 342 · 641</td><td>7DL 246 · 644</td><td>7DJ 82 · 109</td><td>7E1 19 · 182</td></tr>
        <tr><td>Set</td><td>7F8 758 · 968</td><td>7EY 42 · 25</td><td>7G3 36 · 34</td><td>7DJ 30 · 28</td></tr>
        <tr class="hl"><td>Out (01–06)</td><td>7F8 236 · 65</td><td>7DJ 109 · 29</td><td>7EL 86 · 13</td><td>7F7 32 · 5</td></tr>
      </tbody>
    </table>
    <p class="small muted">7DK: procedimento não autorizado · 7DJ: conta não localizada no capeante · 7DQ: negociado como pacote · 7E1: valor divergente do negociado · 7EY: senha cancelada · 7G3: duplicidade de conta · 7EL: código cobrado diferente do autorizado · 7F7: cobrança fora do prazo. O código é o primeiro motivo do item.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill bad">Hipótese principal</span><h3>A glosa de autorização está pegando itens que tinham autorização</h3>
      <p>O volume glosado por esse motivo ficou quase 6 vezes maior e o acato do recurso fica em 82–92% há meses. Se a glosa estivesse certa, o acato cairia. Uma hipótese é que a regra não encontra a autorização de itens hospitalares (por exemplo, itens cobertos pela senha da internação ou guias não vinculadas) e glosa algo que depois é revertido. Isso gera retrabalho dos dois lados.</p></div>
    <div class="panel prov"><span class="pill warn">Acompanhar</span><h3>Os demais motivos estão sendo menos recursados, ou mais tarde</h3>
      <p>O % recursado em até 60 dias dos demais motivos caiu de 52–67% (abr–jun) para 14–22% (jul–set). Parte disso pode ser atraso, como nos casos de HCor e Einstein, que estão recursando com 80+ dias. Essas coortes podem ainda gerar recurso fora do prazo.</p></div>
  </div>
</section>

<section>
  <h2>5. Setembro e outubro em hospitais</h2>
  <div class="panel">
    <p>A análise da queda de setembro olhou só laboratórios. Em hospitais, setembro não caiu: foi o maior mês do ano até então (R$ 963 mil), puxado pelo 7F8 do Sírio (R$ 299 mil). A leitura para hospitais é outra:</p>
    <ul class="plain">
      <li><b>Tendência:</b> o recurso de autorização cresce desde agosto porque a glosa desse motivo cresce desde junho. Isso continua em outubro.</li>
      <li><b>Pontual:</b> em outubro, somam-se PEGs de valor muito alto (CIP) e recursos atrasados de glosas de julho e agosto (HCor, Einstein, Santa Marcelina, SMA). São ~R$ 380 mil acima do ritmo normal.</li>
      <li><b>Comportamento:</b> HCor e Einstein mudaram. HCor passou de 8–31 para 78–85 dias. O Einstein começou a recursar mais e mais tarde.</li>
    </ul>
    <p>Sem os pontuais, outubro ficaria perto de R$ 0,95–1,0 mi, em linha com setembro e acima de mar–jun. O que eleva o patamar é o motivo de autorização.</p>
  </div>
</section>

<section>
  <h2>6. Projeção de outubro e grau de confiança</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Valor</th><th>Itens</th><th>PEGs</th></tr></thead>
      <tbody>
        <tr><td>Real 01–06/10</td><td>R$ 564 mil</td><td>192</td><td>43</td></tr>
        <tr><td>Glosas em aberto até setembro (Américas, Santa Joana, HCor, Einstein e outros)</td><td>R$ 447 mil</td><td>~790</td><td>~115</td></tr>
        <tr><td>Glosas de outubro dos hospitais que recursam no próprio mês (Sírio, HAOC, HCor, São Camilo)</td><td>R$ 332 mil</td><td>~360</td><td>~53</td></tr>
        <tr class="hl"><td><b>Fechamento estimado</b></td><td><b>~R$ 1,34 mi</b></td><td><b>~1,3 mil</b></td><td><b>~210</b></td></tr>
        <tr><td>Faixa pelo teste do método</td><td>R$ 1,27–1,47 mi</td><td>–</td><td>–</td></tr>
      </tbody>
    </table>
  </div>
  <ul class="plain">
    <li><b>Método:</b> curva por hospital e motivo do % do glosado que chega a cada dia depois da glosa (coortes de 2026). Em hospitais entram também as glosas do próprio mês: 29% do recurso de hospitais chega no mesmo mês da glosa (Sírio 93%, HCor 77%, São Camilo 64%, HAOC 51%). O que já chegou acima da curva não é projetado de novo.</li>
    <li><b>Teste:</b> como se estivéssemos no dia 06 de cada mês, o real ficou entre 0,9 e 1,16 vez o projetado (jul 0,90 · ago 1,13 · set 1,16). Em hospitais o método acerta melhor que em laboratórios.</li>
    <li><b>Autorização em outubro:</b> ~R$ 665 mil e ~730 itens, contra R$ 588 mil (ago) e R$ 768 mil (set).</li>
    <li><b>Dados:</b> data warehouse (<code>curated.totvs_procedure_invoice</code>) atualizado até 06/10. Não é tempo real.</li>
  </ul>
</section>

<section>
  <h2>7. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Regra de autorização em hospitais:</b> pegar uma amostra de 7F8 acatados de Sírio, HAOC, Américas e CIP e verificar se havia autorização (senha da internação, guia vinculada). Se a hipótese se confirmar, corrigir a regra reduz a glosa e o recurso juntos.</li>
      <li><b>Prazo de 60 dias:</b> R$ 266 mil de outubro chegaram fora do prazo (HCor, Einstein, Santa Marcelina e SMA). Definir se esses recursos serão negados por prazo e confirmar qual data vale como referência.</li>
      <li><b>HCor e Einstein:</b> conversar sobre o atraso. Os 7DJ do HCor indicam problema de capeante que vale resolver na origem.</li>
      <li><b>Segundo recurso:</b> monitorar reincidência, como o 7F8 do Santa Marcelina.</li>
    </ol>
  </div>
  <p class="small muted">Análise anterior: <a href="https://claude.ai/artifact/NsmUzkeco6xeDXkmZEHZZ2" target="_blank" rel="noopener">Queda de Recurso em Setembro</a> · Dashboard: <a href="https://metabase.datalake.alice.tools/dashboard/2774" target="_blank" rel="noopener">Recurso de Glosa no Metabase</a> (limpe o filtro de tipo de instituição para ver hospitais) · Relatório de laboratórios e clínicas publicado à parte.</p>
</section>
"""
data = r"""
const V = [
 {m:"2026-03",a:196.6,o:185.3},{m:"2026-04",a:78.5,o:630.8},{m:"2026-05",a:151.4,o:333.3},{m:"2026-06",a:202.5,o:569.0},
 {m:"2026-07",a:181.1,o:715.6},{m:"2026-08",a:587.7,o:220.8},{m:"2026-09",a:767.9,o:194.9},
 {m:"2026-10",label:"out*",a:235.9,o:328.4,pa:429,po:350}];
const I = [
 {m:"2026-03",a:464,o:237},{m:"2026-04",a:220,o:770},{m:"2026-05",a:200,o:914},{m:"2026-06",a:220,o:696},
 {m:"2026-07",a:188,o:676},{m:"2026-08",a:1285,o:524},{m:"2026-09",a:997,o:322},
 {m:"2026-10",label:"out*",a:65,o:127,pa:661,po:492}];
const P = [["2026-03",126,701,381.9],["2026-04",121,990,709.3],["2026-05",156,1114,484.7],["2026-06",183,916,771.5],["2026-07",152,864,896.7],["2026-08",165,1809,808.5],["2026-09",151,1319,962.8],["2026-10",43,192,564.3]];
const AC = {"2026-03":[92,71],"2026-04":[91,66],"2026-05":[87,45],"2026-06":[82,58],"2026-07":[82,85],"2026-08":[89,32],"2026-09":[89,46]};
const G = [["2026-01",195,281,0.71],["2026-02",179,690,0.56],["2026-03",76,124,0.26],["2026-04",157,325,0.43],["2026-05",254,336,0.70],["2026-06",536,1217,1.37],["2026-07",738,2111,1.87],["2026-08",945,2129,2.43],["2026-09",936,1457,2.38]];
const R60 = {"2026-04":72.2,"2026-05":86.1,"2026-06":69.2,"2026-07":41.2,"2026-08":56.6,"2026-09":"50,8 (aberta)"};
stacked("chVal", V, "Valor recursado", v => nf(v));
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
bars("chPeg", P.map(p => ({label: p[0]==="2026-10"?"out*":lab(p[0]), v:p[1], pv: p[0]==="2026-10"?168:0,
  tipx:`<b>${lab(p[0])}/26</b><br>PEGs: ${p[1]}${p[0]==="2026-10"?" (real 01–06) + ~168 projetados":""}<br>Itens por PEG: ${nf(p[2]/p[1],1)}<br>R$ por PEG: ${nf(p[3]/p[1],1)} mil`})), v=>nf(v), "PEGs com recurso por mês");
document.getElementById("tPeg").innerHTML = `<thead><tr><th></th>${P.map(p=>`<th>${p[0]==="2026-10"?"out (01–06)":lab(p[0])}</th>`).join("")}<th>out* proj.</th></tr></thead><tbody>
 <tr><td>PEGs</td>${P.map(p=>`<td>${p[1]}</td>`).join("")}<td>~210</td></tr>
 <tr><td>Itens por PEG</td>${P.map(p=>`<td>${nf(p[2]/p[1],1)}</td>`).join("")}<td>~6,4</td></tr>
 <tr><td>R$ mil por PEG</td>${P.map(p=>`<td>${nf(p[3]/p[1],1)}</td>`).join("")}<td>~6,4</td></tr></tbody>`;
bars("chGlA", G.map(g => ({label: lab(g[0]), v:g[3], tipx:`<b>${lab(g[0])}/26 · ${g[0]>="2026-07"?"7F8":"7DL"}</b><br>Glosado: R$ ${g[1]} mil<br>Itens: ${nf(g[2])}<br>% do apresentado: ${nf(g[3],2)}%`})), v=>nf(v,1)+"%", "Glosa de autorização em % do apresentado", "var(--s2)");
document.getElementById("tGlA").innerHTML = `<thead><tr><th>Mês da glosa</th>${G.map(g=>`<th>${lab(g[0])}</th>`).join("")}</tr></thead><tbody>
 <tr><td>Código</td>${G.map(g=>`<td>${g[0]>="2026-07"?"7F8":"7DL"}</td>`).join("")}</tr>
 <tr><td>Glosado (R$ mil)</td>${G.map(g=>`<td>${g[1]}</td>`).join("")}</tr>
 <tr><td>Itens glosados</td>${G.map(g=>`<td>${nf(g[2])}</td>`).join("")}</tr>
 <tr><td>% do apresentado</td>${G.map(g=>`<td>${nf(g[3],2)}%</td>`).join("")}</tr>
 <tr><td>% recursado em até 60 dias</td>${G.map(g=>`<td>${R60[g[0]]!==undefined?(typeof R60[g[0]]==="number"?nf(R60[g[0]],1)+"%":R60[g[0]]):"–"}</td>`).join("")}</tr></tbody>`;
"""
open('recurso-hospitais-outubro.html','w').write(page("Recurso Hospitais Outubro", body, data))
