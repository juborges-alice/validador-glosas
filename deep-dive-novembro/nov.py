import sys
sys.path.insert(0, '../aumento-recurso-outubro/relatorios')
from common import page
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Deep dive · Nov/26 · dados até 09/11</span>
  <h1>Recurso de Glosa em Novembro: o que está acontecendo</h1>
  <p class="muted">Análise dos recursos recebidos de 01 a 09/11, separada em laboratórios e clínicas e em hospitais. Compara com a média de ago–out, abre por prestador, unidade e motivo, e checa as hipóteses levantadas pela operação: 7F6 da DASA, 7EY do Fleury, HCor, Nove de Julho Alphaville e o motivo de autorização em laboratórios.</p>
  <div class="scope">
    <span class="chip">Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 09/11/2026</span>
    <span class="chip">Sem o lote antigo da DASA (glosas de 2025) e sem os recursos de 7F6 de jul–ago</span>
    <span class="chip">Base de comparação: média mensal de ago–out e média dos dias 01–09 de ago–out</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Onde está o excedente?</span>
      <span class="pill bad">Laboratórios. Hospitais estão no normal</span>
      <span class="a">R$ 967 mil: R$ 599 mil em laboratórios e R$ 368 mil em hospitais</span>
      <p>Nos primeiros 9 dias, laboratórios receberam 2,6 vezes a média de ago–out para o mesmo período (R$ 230 mil). Hospitais receberam 8% menos que a média (R$ 400 mil). HCor e Nove de Julho Alphaville subiram, mas HAOC, CIP e Einstein vieram abaixo.</p>
    </div>
    <div class="v">
      <span class="q">Quem recursa o 7EY (senha cancelada)?</span>
      <span class="pill warn">HCor, não o Fleury</span>
      <span class="a">R$ 110 mil dos R$ 124 mil vêm do HCor</span>
      <p>São 5 itens de R$ 91,8 mil num único PEG, glosados em setembro e recursados com 61 dias, mais 7 itens de agosto. Unidades da DASA somam R$ 12,6 mil e o Fleury só R$ 0,5 mil. A onda de 7EY do Fleury ainda não chegou: a A+ Amais (grupo Fleury) tem R$ 166 mil de 7EY glosados em setembro sem recurso até agora.</p>
    </div>
    <div class="v">
      <span class="q">Lote ou mudança de comportamento?</span>
      <span class="pill flat">Três histórias diferentes</span>
      <span class="a">Delboni SP é lote; HCor é atraso recorrente; Nove de Julho Alphaville é mudança dentro do grupo</span>
      <p>A DASA mandou a coorte de setembro inteira em 9 dias, no ritmo de sempre. O HCor recursa só depois de 60 dias pelo segundo mês seguido. O Nove de Julho Alphaville cresce desde outubro, mas o grupo Américas está abaixo da própria média.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Visão geral</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Segmento</th><th>Nov 01–09</th><th>Média ago–out (dias 01–09)</th><th>Variação</th><th>Média mensal ago–out</th><th>Out fechado</th></tr></thead>
      <tbody>
        <tr class="hl"><td>Laboratórios e clínicas</td><td>R$ 599 mil · 2.403 itens · 212 PEGs</td><td>R$ 230 mil</td><td><b>+160%</b></td><td>R$ 564 mil</td><td>R$ 826 mil · 8.682 itens · 332 PEGs</td></tr>
        <tr><td>Hospitais</td><td>R$ 368 mil · 415 itens · 71 PEGs</td><td>R$ 400 mil</td><td>−8%</td><td>R$ 1.044 mil</td><td>R$ 1.374 mil · 2.006 itens · 195 PEGs</td></tr>
        <tr><td><b>Total</b></td><td><b>R$ 967 mil</b></td><td>R$ 630 mil</td><td>+53%</td><td>R$ 1.609 mil</td><td>R$ 2.200 mil</td></tr>
      </tbody>
    </table>
    <p class="small muted">Outubro fechou em R$ 826 mil em laboratórios (projeção era ~R$ 900 mil) e R$ 1,37 mi em hospitais (projeção era ~R$ 1,43 mi).</p>
  </div>
</section>

<section>
  <h2>2. Laboratórios e clínicas</h2>
  <div class="panel tbl-wrap">
    <h3>Prestadores e unidades em novembro (01–09)</h3>
    <table>
      <thead><tr><th>Unidade</th><th>Grupo</th><th>Valor</th><th>Itens</th><th>Média mensal ago–out</th><th>Coorte e dias</th><th>Principais motivos</th></tr></thead>
      <tbody>
        <tr><td>Fleury (matriz)</td><td>Fleury</td><td>R$ 225 mil</td><td>455</td><td>R$ 153 mil</td><td class="wrap-cell">set (46–53 dias) e out (15–23 dias)</td><td class="wrap-cell">7EK R$ 115 mil, 7F6 R$ 38 mil, 7F8 R$ 36 mil</td></tr>
        <tr class="hl"><td>Delboni São Paulo</td><td>DASA</td><td>R$ 125 mil</td><td>194</td><td>R$ 49 mil</td><td class="wrap-cell">set (49–50 dias)</td><td class="wrap-cell">7F8 R$ 57 mil, 7F6 R$ 55 mil, 7G4 R$ 10 mil</td></tr>
        <tr><td>Delboni Barueri</td><td>DASA</td><td>R$ 57 mil</td><td>670</td><td>R$ 29 mil</td><td>set</td><td class="wrap-cell">7G4 R$ 27 mil, 7EY R$ 9 mil</td></tr>
        <tr><td>Salomão São Paulo</td><td>DASA</td><td>R$ 46 mil</td><td>234</td><td>R$ 31 mil</td><td>set</td><td class="wrap-cell">7G4 R$ 16 mil, 7G3, 7EY</td></tr>
        <tr><td>Alta Alphaville</td><td>DASA</td><td>R$ 32 mil</td><td>399</td><td>R$ 9 mil</td><td>set</td><td class="wrap-cell">7F6 R$ 24 mil</td></tr>
        <tr><td>Lavoisier São Paulo</td><td>DASA</td><td>R$ 26 mil</td><td>40</td><td>R$ 8 mil</td><td>set</td><td class="wrap-cell">7F8 R$ 9 mil</td></tr>
        <tr><td>Fleury Santo André, Jundiaí, Alphaville, Campinas</td><td>Fleury</td><td>R$ 50 mil</td><td>164</td><td>R$ 6 mil</td><td>set e out</td><td class="wrap-cell">7EI R$ 10 mil (Santo André), 7EK, 7G9</td></tr>
      </tbody>
    </table>
    <p class="small muted">Por grupo: DASA R$ 319 mil (média mensal de ago–out: R$ 177 mil) e Fleury R$ 279 mil (média: R$ 306 mil).</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill flat">Calendário</span><h3>DASA: a coorte de setembro chegou de uma vez</h3>
      <p>R$ 319 mil em 9 dias, tudo de glosas de setembro, com 49–50 dias. É o ritmo normal da DASA, e é o lote que a projeção de outubro já dava como provável para novembro. A glosa de setembro da DASA era maior (R$ 505 mil, contra R$ 438 mil em agosto). Até agora ela recursou 63%.</p></div>
    <div class="panel prov"><span class="pill warn">Mudança de janela</span><h3>Fleury: recursa cada vez mais rápido</h3>
      <p>O grupo está dentro da própria média mensal, mas chegou mais cedo. A coorte de setembro veio com 46–53 dias (em outubro eram 57). E R$ 102 mil já são de glosas de outubro, recursadas com 15–23 dias. Até setembro, o Fleury quase nunca recursava antes de 40 dias.</p></div>
  </div>
  <div class="panel tbl-wrap">
    <h3>Motivos em novembro (01–09)</h3>
    <table>
      <thead><tr><th>Motivo</th><th>Valor</th><th>Itens</th><th>Média mensal ago–out</th><th>Quem</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr class="hl"><td>7F6 · data incorreta</td><td>R$ 179 mil</td><td>831</td><td>R$ 36 mil</td><td class="wrap-cell">DASA R$ 136 mil (Delboni SP, Alta Alphaville e outras), Fleury R$ 43 mil</td><td class="wrap-cell"><span class="pill flat">Esperado</span> Ajuste alinhado com a DASA</td></tr>
        <tr><td>7EK · sem registro de execução</td><td>R$ 141 mil</td><td>224</td><td>R$ 101 mil</td><td class="wrap-cell">Fleury R$ 136 mil</td><td class="wrap-cell">Já era o motivo do Fleury em outubro</td></tr>
        <tr><td>7F8 · autorização</td><td>R$ 128 mil</td><td>208</td><td>R$ 77 mil</td><td class="wrap-cell">DASA R$ 82 mil (Delboni SP R$ 57 mil), Fleury R$ 46 mil</td><td class="wrap-cell">Recurso da glosa de setembro, na taxa de sempre (ver seção 4)</td></tr>
        <tr><td>7G4 · duplicidade</td><td>R$ 91 mil</td><td>449</td><td>R$ 119 mil</td><td class="wrap-cell">DASA R$ 69 mil, Fleury R$ 22 mil</td><td class="wrap-cell">Abaixo da média</td></tr>
        <tr><td>7G9 · local de atendimento</td><td>R$ 17 mil</td><td>125</td><td>R$ 58 mil</td><td class="wrap-cell">Fleury</td><td class="wrap-cell">Caindo, como a glosa do motivo</td></tr>
        <tr><td>7EY · senha cancelada</td><td>R$ 13 mil</td><td>359</td><td>R$ 27 mil</td><td class="wrap-cell">DASA R$ 12,6 mil (Delboni Barueri, Salomão), Fleury R$ 0,5 mil</td><td class="wrap-cell">Em laboratórios, abaixo da média</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Janela de envio (% do valor recebido por dias entre a glosa e o recurso)</h3>
    <table>
      <thead><tr><th>Mês do recurso</th><th>0–15</th><th>16–30</th><th>31–45</th><th>46–60</th><th>61–90</th></tr></thead>
      <tbody>
        <tr><td>Ago</td><td>1%</td><td>0%</td><td>32%</td><td>19%</td><td>48%</td></tr>
        <tr><td>Set</td><td>0%</td><td>0%</td><td>19%</td><td>35%</td><td>46%</td></tr>
        <tr><td>Out</td><td>0%</td><td>0%</td><td>22%</td><td>67%</td><td>11%</td></tr>
        <tr class="hl"><td>Nov (01–09)</td><td>6%</td><td>11%</td><td>6%</td><td>76%</td><td>1%</td></tr>
      </tbody>
    </table>
    <p class="small muted">Em laboratórios, quase nada chega mais fora do prazo de 60 dias. Os 17% com até 30 dias são o Fleury recursando glosas de outubro.</p>
  </div>
</section>

<section>
  <h2>3. 7EY (senha de autorização cancelada): quem está recursando</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês do recurso</th><th>HCor</th><th>Fleury (grupo)</th><th>DASA (grupo)</th><th>Femme</th><th>Outros hospitais</th></tr></thead>
      <tbody>
        <tr><td>Jul</td><td>–</td><td>R$ 66 mil</td><td>R$ 7 mil</td><td>–</td><td>R$ 5 mil</td></tr>
        <tr><td>Ago</td><td>–</td><td>R$ 35 mil</td><td>R$ 2 mil</td><td>R$ 5 mil</td><td>R$ 15 mil</td></tr>
        <tr><td>Set</td><td>–</td><td>R$ 3 mil</td><td>–</td><td>–</td><td>R$ 42 mil</td></tr>
        <tr><td>Out</td><td>–</td><td>R$ 30 mil</td><td>R$ 4 mil</td><td>R$ 2 mil</td><td>R$ 13 mil</td></tr>
        <tr class="hl"><td>Nov (01–09)</td><td><b>R$ 110 mil</b></td><td>R$ 0,5 mil</td><td>R$ 12,6 mil</td><td>–</td><td>R$ 1 mil</td></tr>
      </tbody>
    </table>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">Pontual</span><h3>HCor: um PEG de alto valor</h3>
      <p>5 itens de 7EY somam R$ 91,8 mil, num único PEG, glosados em setembro e recursados com 61 dias (um dia fora do prazo). Outros 7 itens de agosto (R$ 18 mil) vieram com 77 dias. É um lote de poucos itens caros, não uma mudança no volume de 7EY.</p></div>
    <div class="panel prov"><span class="pill bad">Ainda por vir</span><h3>Fleury: o 7EY está glosado, mas não recursado</h3>
      <p>O grupo Fleury teve R$ 202 mil de 7EY glosados em setembro, sendo R$ 166 mil (6,2 mil itens) só na A+ Amais. Nada disso foi recursado até 09/11. Se o problema de senhas canceladas for confirmado, esse é o lote a esperar nas próximas semanas, com volume alto de itens.</p></div>
  </div>
</section>

<section>
  <h2>4. Autorização em laboratórios: a melhoria se manteve em outubro?</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês da glosa</th><th>Glosa de autorização</th><th>% do apresentado</th><th>% da glosa do mês</th><th>Recurso da coorte (até 09/11)</th><th>% do recurso da coorte</th><th>% recursado</th></tr></thead>
      <tbody>
        <tr><td>Abr</td><td>R$ 424 mil · 3.054 itens</td><td>2,81%</td><td>34%</td><td>R$ 237 mil</td><td>42%</td><td>56%</td></tr>
        <tr><td>Mai</td><td>R$ 626 mil · 3.762 itens</td><td>4,46%</td><td>55%</td><td>R$ 373 mil</td><td>55%</td><td>60%</td></tr>
        <tr><td>Jul</td><td>R$ 204 mil · 1.163 itens</td><td>1,34%</td><td>20%</td><td>R$ 94 mil</td><td>21%</td><td>46%</td></tr>
        <tr><td>Ago</td><td>R$ 255 mil · 1.729 itens</td><td>1,45%</td><td>19%</td><td>R$ 132 mil</td><td>16%</td><td>52%</td></tr>
        <tr><td>Set</td><td>R$ 260 mil · 1.772 itens</td><td>1,47%</td><td>17%</td><td>R$ 112 mil</td><td>22%</td><td>43% (em curso)</td></tr>
        <tr class="hl"><td>Out</td><td>R$ 299 mil · 1.316 itens</td><td><b>1,74%</b></td><td>17%</td><td>R$ 21 mil</td><td>–</td><td>em aberto</td></tr>
      </tbody>
    </table>
    <p class="small muted">Junho ficou fora porque o pico pontual de 7F6 distorce a participação. Outubro em % do apresentado usa o apresentado do mês inteiro (R$ 17,2 mi).</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Se mantém</span><h3>A melhoria continua de pé</h3>
      <p>Em outubro, a glosa por autorização ficou em 1,74% do apresentado, bem abaixo de abr–jun (2,8–4,5%), e em 17% da glosa do mês, igual a agosto e setembro. Por coorte, o motivo segue em 16–22% do recurso, contra 42–55% antes da mudança. O % recursado não subiu.</p></div>
    <div class="panel prov"><span class="pill warn">Atenção</span><h3>Mas outubro subiu um pouco em valor</h3>
      <p>R$ 299 mil, contra R$ 255–260 mil em agosto e setembro, com menos itens (1.316): o valor médio por item aumentou. A alta vem da DASA (R$ 170 mil, contra R$ 132 mil em setembro). Se a DASA recursar no ritmo habitual, isso aparece no recurso de dezembro.</p></div>
  </div>
  <div class="panel">
    <p><b>O recurso de autorização de novembro</b> (R$ 128 mil em 9 dias) é a coorte de setembro chegando: Delboni São Paulo com R$ 57 mil e Fleury com R$ 46 mil. A coorte de setembro está em 43% recursada, dentro da faixa histórica (46–60%). Não há sinal de aumento do motivo por si só.</p>
  </div>
</section>

<section>
  <h2>5. Hospitais</h2>
  <div class="panel tbl-wrap">
    <h3>Hospitais em novembro (01–09) contra a própria média</h3>
    <table>
      <thead><tr><th>Hospital</th><th>Valor</th><th>Itens · PEGs</th><th>Média mensal ago–out</th><th>Coorte e dias</th><th>Principais motivos</th></tr></thead>
      <tbody>
        <tr class="hl"><td>HCor</td><td>R$ 157 mil</td><td>187 · 14</td><td>R$ 81 mil</td><td class="wrap-cell">ago (77–84 dias) e set (61 dias). 100% fora do prazo</td><td class="wrap-cell">7EY R$ 110 mil, 7E1 R$ 26 mil, 7F8 R$ 20 mil</td></tr>
        <tr class="hl"><td>Nove de Julho Alphaville</td><td>R$ 99 mil</td><td>35 · 14</td><td>R$ 23 mil</td><td class="wrap-cell">set (45–60 dias), dentro do prazo</td><td class="wrap-cell">7F8 R$ 49 mil, 7EL R$ 37 mil, 7DV R$ 7 mil, 7G1 R$ 5 mil</td></tr>
        <tr><td>HAOC</td><td>R$ 49 mil</td><td>82 · 10</td><td>R$ 100 mil</td><td>set</td><td class="wrap-cell">7E1 R$ 22 mil, 7G3 R$ 13 mil</td></tr>
        <tr><td>Einstein</td><td>R$ 23 mil</td><td>18 · 9</td><td>R$ 40 mil</td><td>ago–set</td><td class="wrap-cell">505, 7DV</td></tr>
        <tr><td>CIP Pacaembu</td><td>R$ 17 mil</td><td>4 · 2</td><td>R$ 88 mil</td><td>set</td><td class="wrap-cell">7F8, 505</td></tr>
      </tbody>
    </table>
    <p class="small muted">Hospitais somam R$ 368 mil, 8% abaixo da média dos dias 01–09 de ago–out. 44% do valor (R$ 162 mil) chegou com mais de 60 dias, todo do HCor.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill bad">Comportamento</span><h3>HCor: segundo mês só com recurso fora do prazo</h3>
      <p>Em outubro foram R$ 221 mil e em novembro R$ 157 mil, sempre com mais de 60 dias. Em novembro, o valor está concentrado num PEG de 7EY (R$ 91,8 mil). O padrão de atraso é recorrente. O valor deste mês é pontual. Até agora, quase nada do que foi analisado foi acatado.</p></div>
    <div class="panel prov"><span class="pill flat">Dentro do grupo</span><h3>Nove de Julho Alphaville: cresce, mas o grupo Américas não</h3>
      <p>A unidade passou de R$ 7–10 mil (ago–set) para R$ 50 mil em outubro e R$ 99 mil em novembro, dentro do prazo. São glosas de setembro de 7F8 e 7EL, em poucos itens caros. O grupo Américas como um todo está em R$ 102 mil, abaixo da própria média (R$ 152 mil). Parece mais uma mudança de qual unidade concentra o recurso do que um aumento do grupo.</p></div>
  </div>
  <div class="panel">
    <p><b>Autorização em hospitais (7F8):</b> R$ 97 mil em novembro, contra uma média de R$ 590 mil por mês em ago–out. O motivo que puxou o recurso de hospitais desde agosto está fraco no início de novembro.</p>
  </div>
</section>

<section>
  <h2>6. Respostas às perguntas da operação</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Pergunta</th><th>Resposta</th></tr></thead>
      <tbody>
        <tr><td class="wrap-cell"><b>O 7F6 da DASA está coerente com o ajuste alinhado?</b></td><td class="wrap-cell">Sim. R$ 136 mil de 7F6 da DASA em novembro, todo de glosas de setembro. A glosa de 7F6 da DASA em outubro foi de R$ 519 mil (contra R$ 159 mil em setembro): o recurso desse motivo deve continuar alto até dezembro.</td></tr>
        <tr><td class="wrap-cell"><b>Quem recursa o 7EY? É o Fleury?</b></td><td class="wrap-cell">Não em novembro. R$ 110 mil dos R$ 124 mil são do HCor (um PEG). O Fleury mandou R$ 0,5 mil. O lote de 7EY do Fleury (A+ Amais, R$ 166 mil e 6,2 mil itens glosados em setembro) ainda não foi recursado.</td></tr>
        <tr><td class="wrap-cell"><b>HCor, Nove de Julho Alphaville e Delboni São Paulo: lote ou mudança?</b></td><td class="wrap-cell">Delboni SP é lote da coorte de setembro da DASA, no ritmo de sempre. HCor é atraso recorrente (dois meses fora do prazo), com valor pontual de 7EY. Nove de Julho Alphaville é crescimento da unidade dentro do prazo, sem aumento do grupo Américas.</td></tr>
        <tr><td class="wrap-cell"><b>A glosa de autorização em laboratórios voltou a crescer?</b></td><td class="wrap-cell">Um pouco em valor (R$ 299 mil em outubro, 1,74% do apresentado), puxada pela DASA, mas segue bem abaixo de antes da mudança (2,8–4,5%). O peso no recurso e a taxa de recurso seguem estáveis.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <h2>7. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Fleury, A+ Amais (7EY):</b> R$ 166 mil e 6,2 mil itens glosados em setembro sem recurso. Se chegarem, pesam muito na fila de análise.</li>
      <li><b>Fleury, coorte de setembro:</b> R$ 880 mil glosados e só ~R$ 175 mil recursados até agora. Com a janela mais curta, o restante deve chegar ainda em novembro.</li>
      <li><b>DASA, 7F6 de outubro:</b> R$ 519 mil glosados. Pelo ritmo da DASA (~50 dias), o recurso chega em dezembro.</li>
      <li><b>HCor:</b> definir a regra para recurso com mais de 60 dias. São dois meses seguidos só com recurso tardio.</li>
      <li><b>Autorização em laboratórios:</b> acompanhar se a alta de outubro da DASA (R$ 170 mil) se repete em novembro.</li>
    </ol>
  </div>
  <p class="small muted">Relatórios anteriores: <a href="https://claude.ai/artifact/JvmQpkcgmthQJjsS5gF1UG" target="_blank" rel="noopener">Deep dive de outubro: laboratórios</a> · <a href="https://claude.ai/artifact/MHdaoDwAcjZL5b8ZC7XXPY" target="_blank" rel="noopener">Deep dive de outubro: hospitais</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 09/11. Não é tempo real.</p>
</section>
"""
open('deep-dive-novembro.html','w').write(page("Recurso de Glosa Novembro", body, ""))
