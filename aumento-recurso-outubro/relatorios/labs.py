from common import page
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Laboratórios e clínicas · Out/26 · atualizado em 14/10</span>
  <h1>Recurso de Glosa em Outubro: Laboratórios e Clínicas</h1>
  <p class="muted">Atualização com os recursos recebidos até 13/10. Em 13 dias, outubro já recebeu quase o mesmo valor que agosto inteiro. Este relatório mostra o tamanho da alta em valor, itens e PEG, as causas, como fica o motivo de falta de autorização e quanto ainda deve chegar até o fim do mês.</p>
  <div class="scope">
    <span class="chip">Laboratório + Clínica · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 13/10/2026</span>
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
      <span class="pill warn">Sim. Perto do pico de julho em valor e recorde em itens</span>
      <span class="a">~R$ 865 mil · ~6,9 mil itens · ~440 PEGs</span>
      <p>Até 13/10 entraram R$ 657 mil, 4.527 itens e 276 PEGs. A projeção fecha o mês entre R$ 750 e 970 mil: perto de julho (R$ 907 mil, o maior do ano até agora) e acima de agosto (R$ 716 mil). Em itens, deve ser o maior mês do ano: julho e agosto ficaram em 5,5–5,7 mil.</p>
    </div>
    <div class="v">
      <span class="q">Quais são as causas?</span>
      <span class="pill flat">Três efeitos somados</span>
      <span class="a">Atraso da DASA, mudança no Fleury e glosa total de volta ao normal</span>
      <p>A DASA entregou a coorte de agosto em outubro, e não em setembro (R$ 249 mil). O Fleury passou a recursar mais e mais cedo: 41% da coorte de agosto em até 60 dias, contra 0–13% antes (R$ 322 mil). E a glosa total de agosto e setembro voltou ao nível de abr–mai, com novos motivos no lugar da autorização.</p>
    </div>
    <div class="v">
      <span class="q">O recurso por falta de autorização voltou a subir?</span>
      <span class="pill warn">Caiu em valor, não em itens</span>
      <span class="a">~R$ 189 mil e ~1.320 itens no mês</span>
      <p>A glosa do motivo segue baixa, em 1,4–1,5% do apresentado. Mas a coorte de agosto foi 52% recursada em até 60 dias, contra 30–34% antes. O valor fica ~29% abaixo da média de abr–ago (R$ 267 mil). Em itens, fica perto da média (~1.420), puxado pelo Femme (731 itens de baixo valor).</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Valor recebido por mês</h2>
  <p class="muted">Valor recursado (R$ mil), por mês de recebimento do recurso. A barra de outubro mostra o real de 01 a 13/10 e, hachurada, a projeção de 14 a 31/10.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 14–31/10</span></div>
    <div id="chVal"></div>
    <div class="tbl-wrap"><table id="tVal"></table></div>
  </div>
  <div class="panel tbl-wrap">
    <h3>Os primeiros 13 dias de cada mês</h3>
    <table>
      <thead><tr><th></th><th>Mar</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th></tr></thead>
      <tbody>
        <tr><td>Valor (R$ mil)</td><td>104</td><td>38</td><td>212</td><td>176</td><td>370</td><td>112</td><td>39</td><td><b>657</b></td></tr>
        <tr><td>Itens</td><td>793</td><td>409</td><td>632</td><td>1.586</td><td>1.765</td><td>1.431</td><td>633</td><td><b>4.527</b></td></tr>
        <tr><td>PEGs</td><td>110</td><td>41</td><td>99</td><td>206</td><td>171</td><td>101</td><td>44</td><td><b>276</b></td></tr>
      </tbody>
    </table>
    <p class="small muted">Outubro recebeu em 13 dias quase o dobro do melhor início de mês do ano (julho). Dois lotes grandes caíram no início do mês: DASA em 05–06/10 e Fleury em 09/10.</p>
  </div>
</section>

<section>
  <h2>2. Itens recebidos para análise</h2>
  <p class="muted">Itens recursados (itens distintos de guia), por mês de recebimento. Esta é a medida de carga de trabalho do time de análise.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--s2)"></i>Autorização (7DL/7F8)</span><span><i style="background:var(--s1)"></i>Demais motivos</span><span><i class="proj"></i>Projeção 14–31/10</span></div>
    <div id="chItem"></div>
    <div class="tbl-wrap"><table id="tItem"></table></div>
  </div>
</section>

<section>
  <h2>3. Recurso por protocolo (PEG)</h2>
  <p class="muted">PEGs distintos com recurso recebido no mês, com o tamanho médio de cada PEG.</p>
  <div class="panel">
    <div class="legend"><span><i style="background:var(--accent)"></i>PEGs recebidos</span><span><i class="proj"></i>Projeção 14–31/10</span></div>
    <div id="chPeg"></div>
    <div class="tbl-wrap"><table id="tPeg"></table></div>
    <p class="small muted">A projeção de PEGs divide os itens projetados de cada prestador pela média de itens por PEG dele em mar–set. É uma estimativa aproximada.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">157 PEGs</span><h3>DASA</h3>
      <p>R$ 249 mil e 953 itens, todos de glosas de agosto, recebidos em 05 e 06/10, entre 40 e 60 dias depois da glosa. PEGs pequenos, de ~6 itens. A coorte de setembro (R$ 505 mil glosados) ainda não chegou.</p></div>
    <div class="panel prov"><span class="pill warn">96 PEGs</span><h3>Fleury</h3>
      <p>R$ 322 mil e 2.033 itens da coorte de agosto, a maior parte em 09/10, entre 41 e 60 dias depois da glosa. Nos meses anteriores, o Fleury quase não recursava antes dos 60 dias.</p></div>
    <div class="panel prov"><span class="pill flat">20 PEGs</span><h3>Femme</h3>
      <p>R$ 72 mil e 1.483 itens da coorte de agosto, no ritmo de sempre (86% do glosado). É volume alto de itens e baixo valor, com 731 itens de 7F8.</p></div>
  </div>
</section>

<section>
  <h2>4. Causas da alta de outubro</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Causa</th><th>O que aconteceu</th><th>Impacto em outubro</th><th>Tipo</th></tr></thead>
      <tbody>
        <tr><td class="wrap-cell"><b>Atraso da DASA</b></td><td class="wrap-cell">A coorte de agosto chegou com mediana de 54 dias, contra 44 dias nos meses anteriores. Saiu de setembro e caiu inteira em outubro. A taxa (57%) não mudou.</td><td>R$ 249 mil · 953 itens · 157 PEGs</td><td class="wrap-cell"><span class="pill flat">Calendário</span></td></tr>
        <tr><td class="wrap-cell"><b>Fleury recursando mais e mais cedo</b></td><td class="wrap-cell">41% da coorte de agosto foi recursada em até 60 dias, com mediana de 51 dias. Antes eram 0–13% em 60 dias e mediana de 55–83 dias. A base também cresceu: R$ 783 mil glosados em agosto, contra R$ 513 mil em julho.</td><td>R$ 322 mil · 2.033 itens · 96 PEGs</td><td class="wrap-cell"><span class="pill warn">Mudança de comportamento</span></td></tr>
        <tr><td class="wrap-cell"><b>Glosa total de volta ao nível normal</b></td><td class="wrap-cell">A tabela nova reduziu a glosa por autorização, mas outros motivos ocuparam o espaço. Agosto (R$ 1,35 mi) e setembro (R$ 1,53 mi) voltaram a 7,7–8,6% do apresentado. Só julho tinha sido baixo.</td><td class="wrap-cell">Base maior para o recurso de outubro e novembro</td><td class="wrap-cell"><span class="pill warn">Estrutural</span></td></tr>
        <tr><td class="wrap-cell"><b>Mais recurso por real glosado</b></td><td class="wrap-cell">A coorte de agosto foi 49–52% recursada em até 60 dias, contra 23–45% nos meses anteriores. Vale para autorização e para os demais motivos.</td><td class="wrap-cell">Puxado por Fleury e Femme</td><td class="wrap-cell"><span class="pill warn">Mudança de comportamento</span></td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel tbl-wrap">
    <h3>Coortes de glosa dos três maiores laboratórios: % do glosado recursado</h3>
    <table>
      <thead><tr><th>Prestador · coorte</th><th>Glosado</th><th>Em até 60 dias</th><th>Até hoje</th><th>Mediana de dias</th></tr></thead>
      <tbody>
        <tr><td>Fleury · mai</td><td>R$ 442 mil</td><td>9%</td><td>37%</td><td>63</td></tr>
        <tr><td>Fleury · jun</td><td>R$ 1.035 mil</td><td>5%</td><td>33%</td><td>65</td></tr>
        <tr><td>Fleury · jul</td><td>R$ 513 mil</td><td>13%</td><td>22%</td><td>55</td></tr>
        <tr class="hl"><td>Fleury · ago</td><td>R$ 783 mil</td><td><b>41%</b></td><td><b>41%</b></td><td><b>51</b></td></tr>
        <tr><td>DASA · jun</td><td>R$ 508 mil</td><td>58%</td><td>64%</td><td>44</td></tr>
        <tr><td>DASA · jul</td><td>R$ 373 mil</td><td>56%</td><td>59%</td><td>44</td></tr>
        <tr class="hl"><td>DASA · ago</td><td>R$ 438 mil</td><td>57%</td><td>57%</td><td><b>54</b></td></tr>
        <tr><td>Femme · jul</td><td>R$ 62 mil</td><td>79%</td><td>79%</td><td>41</td></tr>
        <tr><td>Femme · ago</td><td>R$ 83 mil</td><td>86%</td><td>86%</td><td>49</td></tr>
      </tbody>
    </table>
    <p class="small muted">Os valores de junho do Fleury não incluem os recursos de 7F6 de jul–ago, tratados como excepcionais.</p>
  </div>
</section>

<section>
  <h2>5. Motivos: o que está sendo recursado</h2>
  <div class="panel tbl-wrap">
    <h3>Motivos mais recursados por mês de recebimento (R$ mil · itens)</h3>
    <table>
      <thead><tr><th>Mês</th><th>1º</th><th>2º</th><th>3º</th><th>4º</th><th>5º</th></tr></thead>
      <tbody>
        <tr><td>Jul</td><td>7DL 439 · 1.642</td><td>7EK 188 · 1.232</td><td>7EY 72 · 869</td><td>7DY 42 · 163</td><td>7EZ 38 · 182</td></tr>
        <tr><td>Ago</td><td>7DL 194 · 1.381</td><td>7G4 142 · 693</td><td>7EK 95 · 1.142</td><td>7DY 74 · 474</td><td>7F8 55 · 374</td></tr>
        <tr><td>Set</td><td>7EK 59 · 157</td><td>7F8 40 · 94</td><td>7G4 21 · 112</td><td>7F6 12 · 384</td><td>7G3 3 · 18</td></tr>
        <tr class="hl"><td>Out (01–13)</td><td>7G4 188 · 1.040</td><td>7EK 131 · 445</td><td>7F8 130 · 1.027</td><td>7F6 83 · 419</td><td>7G9 40 · 229</td></tr>
      </tbody>
    </table>
    <p class="small muted">7G4: cobrança em duplicidade · 7EK: procedimento sem registro de execução · 7F8: autorização · 7F6: data preenchida incorretamente · 7G9: local de atendimento inválido · 7EY: senha cancelada (902 itens em outubro, R$ 30 mil, quase todos do Fleury). O código é o primeiro motivo do item.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill warn">Maior motivo</span><h3>Duplicidade (7G4)</h3>
      <p>R$ 188 mil e 1.040 itens até 13/10: DASA R$ 93 mil, Fleury R$ 61 mil e Femme R$ 29 mil. É o motivo com acato mais alto quando o procedimento aparece 3 ou mais vezes no dia (ver o relatório Regra de Duplicidade).</p></div>
    <div class="panel prov"><span class="pill warn">Fleury</span><h3>Execução (7EK) e senha cancelada (7EY)</h3>
      <p>O Fleury puxou o 7EK (R$ 94 mil) e quase todo o 7EY (798 itens). São motivos que ele quase não recursava antes de agosto.</p></div>
    <div class="panel prov"><span class="pill warn">Em alta</span><h3>Data incorreta (7F6)</h3>
      <p>R$ 83 mil recursados até 13/10. A glosa desse motivo segue subindo: R$ 307 mil em setembro e R$ 380 mil só de 01 a 13/10. Esse recurso deve chegar em novembro e dezembro.</p></div>
  </div>
</section>

<section>
  <h2>6. Falta de autorização: glosa baixa, mas recurso alto por item</h2>
  <p class="muted">Glosa por autorização não localizada, em % do valor apresentado, por mês da glosa. Em julho, o 7DL deixou de ser usado e o motivo passou a sair como 7F8.</p>
  <div class="panel">
    <h3>Glosa de autorização em % do apresentado</h3>
    <div id="chGlA"></div>
    <div class="tbl-wrap"><table id="tGlA"></table></div>
    <p class="small muted">% do apresentado = glosado no mês da glosa ÷ apresentado no mês da conta. Outubro considera só de 01 a 13/10.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Se mantém</span><h3>A glosa do motivo segue baixa</h3>
      <p>Agosto a outubro ficaram em 1,4–1,5% do apresentado, contra 2,8–4,5% até junho. É a redução que a tabela nova trouxe.</p></div>
    <div class="panel prov"><span class="pill warn">Mudou</span><h3>Mas o motivo passou a ser mais recursado</h3>
      <p>A coorte de agosto foi 52% recursada em até 60 dias, contra 30–34% em abr–jul. Por isso o recurso de autorização em outubro (~R$ 189 mil) cai menos que a glosa: −29% em valor contra a média de abr–ago, e quase igual em itens.</p></div>
    <div class="panel prov"><span class="pill warn">Atenção</span><h3>O que é recursado é muito acatado</h3>
      <p>Do recurso de autorização analisado, 81% foi acatado em agosto e 83% no que já foi analisado em outubro. A maior parte do que ainda é glosado e recursado está sendo revertida. Vale olhar se o 7F8 está glosando itens que tinham autorização.</p></div>
  </div>
</section>

<section>
  <h2>7. Onde está o efeito da redução da glosa</h2>
  <p class="muted">Glosa de laboratórios e clínicas por tema, por mês da glosa (R$ mil e % do apresentado). Códigos antigos e novos agrupados pelo mesmo tema.</p>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Tema</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out (01–13)</th></tr></thead>
      <tbody>
        <tr><td>Autorização (7DL → 7F8)</td><td>424 · 2,8%</td><td>626 · 4,5%</td><td>519 · 3,3%</td><td>204 · 1,3%</td><td>255 · 1,5%</td><td>259 · 1,5%</td><td>159 · 1,4%</td></tr>
        <tr><td>Duplicidade (7DX/7DY → 7G4/7G3)</td><td>108 · 0,7%</td><td>98 · 0,7%</td><td>242 · 1,6%</td><td>317 · 2,1%</td><td>277 · 1,6%</td><td>243 · 1,4%</td><td>100 · 0,9%</td></tr>
        <tr><td>Local de atendimento (7EI → 7G9)</td><td>36 · 0,2%</td><td>67 · 0,5%</td><td>193 · 1,2%</td><td>248 · 1,6%</td><td>205 · 1,2%</td><td>138 · 0,8%</td><td>14 · 0,1%</td></tr>
        <tr class="hl"><td>Data incorreta (7F6)</td><td>0</td><td>0</td><td>714 · 4,6%</td><td>51 · 0,3%</td><td>141 · 0,8%</td><td>307 · 1,7%</td><td><b>380 · 3,3%</b></td></tr>
        <tr><td>Demais</td><td>689 · 4,6%</td><td>356 · 2,5%</td><td>517 · 3,3%</td><td>198 · 1,3%</td><td>474 · 2,7%</td><td>579 · 3,3%</td><td>182 · 1,6%</td></tr>
        <tr><td><b>Total</b></td><td><b>1.256 · 8,3%</b></td><td><b>1.146 · 8,2%</b></td><td><b>2.185 · 14,1%</b></td><td><b>1.017 · 6,7%</b></td><td><b>1.352 · 7,7%</b></td><td><b>1.528 · 8,6%</b></td><td><b>835 · 7,2%</b></td></tr>
      </tbody>
    </table>
    <p class="small muted">Junho inclui o pico pontual de 7F6. Cada item entra em um tema só, nesta ordem: autorização, duplicidade, local e data.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Como esperado</span><h3>Duplicidade e local caindo</h3>
      <p>Duplicidade caiu de 2,1% em julho para 0,9% em outubro, já perto do patamar de antes (0,7%). Local de atendimento quase sumiu (0,1%).</p></div>
    <div class="panel prov"><span class="pill bad">Contra o esperado</span><h3>Data incorreta (7F6) disparou</h3>
      <p>Saiu de 0,3% em julho para 3,3% do apresentado nos primeiros 13 dias de outubro. É o tema que mantém a glosa total no nível de antes e deve gerar a próxima onda de recurso.</p></div>
  </div>
</section>

<section>
  <h2>8. Setembro e outubro: o que a análise anterior previa e o que aconteceu</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Hipótese</th><th>O que aconteceu até 13/10</th><th>Leitura</th></tr></thead>
      <tbody>
        <tr><td class="wrap-cell"><b>A tabela nova reduziu a glosa por autorização</b></td><td class="wrap-cell">Agosto a outubro em 1,4–1,5% do apresentado, contra 2,8–4,5% até junho.</td><td class="wrap-cell"><span class="pill good">Se mantém</span></td></tr>
        <tr><td class="wrap-cell"><b>O % recursado do motivo não mudou</b></td><td class="wrap-cell">Subiu: a coorte de agosto foi 52% recursada em até 60 dias, contra 30–34%.</td><td class="wrap-cell"><span class="pill warn">Não se mantém</span></td></tr>
        <tr><td class="wrap-cell"><b>Julho foi recursado antes e sobrou pouco para setembro</b></td><td class="wrap-cell">28% da coorte de julho chegou em agosto. Setembro recebeu só R$ 150 mil.</td><td class="wrap-cell"><span class="pill good">Confirmada</span></td></tr>
        <tr><td class="wrap-cell"><b>Acompanhar a DASA até 01/10</b></td><td class="wrap-cell">A coorte de agosto chegou em 05–06/10, uma semana depois da janela, na taxa de sempre.</td><td class="wrap-cell"><span class="pill good">Explica parte da alta</span></td></tr>
        <tr><td class="wrap-cell"><b>Fleury e Femme só teriam leitura em outubro</b></td><td class="wrap-cell">Chegaram em 09/10. O Femme veio no padrão. O Fleury veio bem acima do padrão (41% em 60 dias).</td><td class="wrap-cell"><span class="pill warn">Explica a maior parte da alta</span></td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel">
    <h3>Conclusão</h3>
    <p>Setembro foi um vale de calendário. A coorte de julho era a única com glosa total baixa, parte dela já tinha sido recursada em agosto, e a DASA atrasou o lote de agosto.</p>
    <p>Outubro vai além de devolver o que faltou em setembro. Somam-se três efeitos: o atraso da DASA, o Fleury recursando muito mais e mais cedo, e uma glosa total que voltou ao nível normal com motivos novos, como 7G4, 7F6 e 7EY. Com isso, outubro deve ser o maior mês do ano em itens e ficar no topo da faixa em valor. O efeito da tabela nova aparece só na glosa por autorização. No recurso, ele foi compensado pela taxa maior de recurso e pelos outros motivos.</p>
  </div>
</section>

<section>
  <h2>9. Projeção de outubro e grau de confiança</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Valor</th><th>Itens</th><th>PEGs</th></tr></thead>
      <tbody>
        <tr><td>Real 01–13/10</td><td>R$ 657 mil</td><td>4.527</td><td>276</td></tr>
        <tr><td>DASA, coorte de setembro</td><td>R$ 113 mil</td><td>~730</td><td>~80</td></tr>
        <tr><td>DASA, resto de agosto</td><td>R$ 36 mil</td><td>~450</td><td>~50</td></tr>
        <tr><td>Femme, agosto e setembro</td><td>R$ 30 mil</td><td>~780</td><td>~14</td></tr>
        <tr><td>Fleury, julho e setembro</td><td>R$ 20 mil</td><td>~360</td><td>~16</td></tr>
        <tr><td>Demais prestadores</td><td>R$ 9 mil</td><td>~20</td><td>~3</td></tr>
        <tr class="hl"><td><b>Fechamento estimado</b></td><td><b>~R$ 865 mil</b></td><td><b>~6,9 mil</b></td><td><b>~440</b></td></tr>
        <tr><td>Se a DASA de setembro ficar para novembro</td><td>~R$ 750 mil</td><td>~6,1 mil</td><td>~360</td></tr>
        <tr><td>Se o Fleury começar a coorte de setembro ainda em outubro</td><td>até ~R$ 970 mil</td><td>até ~8 mil</td><td>–</td></tr>
      </tbody>
    </table>
  </div>
  <ul class="plain">
    <li><b>Método:</b> para cada prestador e motivo, uma curva do % do glosado que costuma chegar a cada dia depois da glosa, com coortes de 2026. Ela é aplicada só às glosas em aberto até setembro, porque laboratórios e clínicas não recursam no mês da glosa. Se um prestador já recursou acima da curva, nada mais é projetado para aquela coorte. Por isso o Fleury e o Femme quase não somam: a coorte de agosto deles já chegou.</li>
    <li><b>O que mudou desde a versão de 06/10:</b> a projeção anterior era de ~R$ 690 mil. O Fleury entregou R$ 322 mil da coorte de agosto, contra R$ 199 mil previstos. A curva histórica do Fleury subestimou o novo comportamento.</li>
    <li><b>Teste:</b> com o mesmo método, como se estivéssemos no dia 13 de cada mês, o real ficou entre 0,42 e 2,0 vezes o projetado (jul 1,8 · ago 2,0 · set 0,42). A incerteza agora está quase toda num lote só, a DASA de setembro. Por isso a faixa razoável vai de ~R$ 750 a ~R$ 970 mil.</li>
    <li><b>Dados:</b> data warehouse (<code>curated.totvs_procedure_invoice</code>) atualizado até 13/10. Não é tempo real.</li>
  </ul>
</section>

<section>
  <h2>10. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>DASA, do fim de outubro ao início de novembro:</b> coorte de setembro (R$ 505 mil glosados). Com o prazo de agosto (~54 dias), chega a partir de 01/11. Com o prazo antigo (~44 dias), ainda em outubro.</li>
      <li><b>Fleury em novembro:</b> a coorte de setembro tem R$ 880 mil glosados. No novo ritmo (41% em 60 dias), seriam ~R$ 360 mil de recurso na primeira quinzena de novembro. Vale confirmar com o Fleury se a mudança é permanente, por exemplo uma equipe nova de recurso.</li>
      <li><b>Data incorreta (7F6):</b> a glosa já chegou a 3,3% do apresentado em outubro. Entender o que mudou na regra ou no faturamento antes que o recurso desse motivo chegue.</li>
      <li><b>Autorização:</b> com 52% recursado e 81–83% de acato, levantar uma amostra de 7F8 acatados para ver se a autorização existia na glosa.</li>
      <li><b>Medir por coorte de glosa:</b> no dashboard, a leitura mês a mês mistura coortes e oscila com o calendário de cada prestador. O % recursado em até 60 dias por prestador é o que mostra mudança de comportamento, como a do Fleury.</li>
    </ol>
  </div>
  <p class="small muted">Análise anterior: <a href="https://claude.ai/artifact/NsmUzkeco6xeDXkmZEHZZ2" target="_blank" rel="noopener">Queda de Recurso em Setembro</a> · Dashboard: <a href="https://metabase.datalake.alice.tools/dashboard/2774" target="_blank" rel="noopener">Recurso de Glosa no Metabase</a> · Relacionados: <a href="https://claude.ai/artifact/72dEyR4iKQ9AdHxZpncSBT" target="_blank" rel="noopener">Hospitais</a> e <a href="https://claude.ai/artifact/BnYkCCrfqa5Nr7ruyfoeQA" target="_blank" rel="noopener">Regra de Duplicidade</a>.</p>
</section>
"""
data = r"""
const V = [
 {m:"2026-03",a:266.1,o:397.6},{m:"2026-04",a:175.6,o:371.4},{m:"2026-05",a:260.7,o:354.7},{m:"2026-06",a:202.2,o:257.7},
 {m:"2026-07",a:439.1,o:468.2},{m:"2026-08",a:255.6,o:460.9},{m:"2026-09",a:41.7,o:108.8},
 {m:"2026-10",label:"out*",a:131.6,o:525.2,pa:57.5,po:150.5}];
const I = [
 {m:"2026-03",a:1232,o:1468},{m:"2026-04",a:733,o:5232},{m:"2026-05",a:1080,o:1578},{m:"2026-06",a:1882,o:2414},
 {m:"2026-07",a:1644,o:3830},{m:"2026-08",a:1765,o:3890},{m:"2026-09",a:126,o:810},
 {m:"2026-10",label:"out*",a:1028,o:3499,pa:293,po:2055}];
const P = [["2026-03",313,2700,663.7],["2026-04",247,5965,547.0],["2026-05",341,2658,615.4],["2026-06",394,4296,459.9],["2026-07",432,5474,907.2],["2026-08",381,5655,716.5],["2026-09",91,936,150.5],["2026-10",276,4527,656.8]];
const AC = {"2026-03":[37,70],"2026-04":[26,23],"2026-05":[78,88],"2026-06":[14,80],"2026-07":[61,94],"2026-08":[81,79],"2026-09":[50,85]};
const G = [["2026-01",371,2053,4.13],["2026-02",387,2742,2.81],["2026-03",373,2777,2.95],["2026-04",424,3054,2.81],["2026-05",626,3762,4.46],["2026-06",519,4345,3.34],["2026-07",204,1163,1.34],["2026-08",255,1729,1.45],["2026-09",259,1772,1.47],["2026-10",159,457,1.37]];
const R60 = {"2026-04":29.8,"2026-05":33.5,"2026-06":29.9,"2026-07":32.4,"2026-08":51.6,"2026-09":"aberta","2026-10":"aberta"};
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
bars("chPeg", P.map(p => ({label: p[0]==="2026-10"?"out*":lab(p[0]), v:p[1], pv: p[0]==="2026-10"?163:0,
  tipx:`<b>${lab(p[0])}/26</b><br>PEGs: ${p[1]}${p[0]==="2026-10"?" (real 01–13) + ~163 projetados":""}<br>Itens por PEG: ${nf(p[2]/p[1],1)}<br>R$ por PEG: ${nf(p[3]/p[1],1)} mil`})), v=>nf(v), "PEGs com recurso por mês");
document.getElementById("tPeg").innerHTML = `<thead><tr><th></th>${P.map(p=>`<th>${p[0]==="2026-10"?"out (01–13)":lab(p[0])}</th>`).join("")}<th>out* proj.</th></tr></thead><tbody>
 <tr><td>PEGs</td>${P.map(p=>`<td>${p[1]}</td>`).join("")}<td>~440</td></tr>
 <tr><td>Itens por PEG</td>${P.map(p=>`<td>${nf(p[2]/p[1],1)}</td>`).join("")}<td>~16</td></tr>
 <tr><td>R$ mil por PEG</td>${P.map(p=>`<td>${nf(p[3]/p[1],1)}</td>`).join("")}<td>~2,0</td></tr></tbody>`;
bars("chGlA", G.map(g => ({label: lab(g[0]) + (g[0]==="2026-10"?"*":""), v:g[3], tipx:`<b>${lab(g[0])}/26 · ${g[0]>="2026-07"?"7F8":"7DL"}</b><br>Glosado: R$ ${g[1]} mil<br>Itens: ${nf(g[2])}<br>% do apresentado: ${nf(g[3],2)}%`})), v=>nf(v,1)+"%", "Glosa de autorização em % do apresentado", "var(--s2)");
document.getElementById("tGlA").innerHTML = `<thead><tr><th>Mês da glosa</th>${G.map(g=>`<th>${lab(g[0])}${g[0]==="2026-10"?" (01–13)":""}</th>`).join("")}</tr></thead><tbody>
 <tr><td>Código</td>${G.map(g=>`<td>${g[0]>="2026-07"?"7F8":"7DL"}</td>`).join("")}</tr>
 <tr><td>Glosado (R$ mil)</td>${G.map(g=>`<td>${g[1]}</td>`).join("")}</tr>
 <tr><td>Itens glosados</td>${G.map(g=>`<td>${nf(g[2])}</td>`).join("")}</tr>
 <tr><td>% do apresentado</td>${G.map(g=>`<td>${nf(g[3],2)}%</td>`).join("")}</tr>
 <tr><td>% recursado em até 60 dias</td>${G.map(g=>`<td>${R60[g[0]]!==undefined?(typeof R60[g[0]]==="number"?nf(R60[g[0]],1)+"%":R60[g[0]]):"–"}</td>`).join("")}</tr></tbody>`;
"""
open('recurso-labs-outubro.html','w').write(page("Recurso Laboratórios Outubro", body, data))
