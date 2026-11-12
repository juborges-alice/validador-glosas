import sys
sys.path.insert(0, '../aumento-recurso-outubro/relatorios')
from common import page
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Deep dive · Laboratórios e clínicas · Nov/26 · dados até 11/11</span>
  <h1>Recurso de Glosa em Novembro: Laboratórios e Clínicas</h1>
  <p class="muted">Análise dos recursos de laboratórios e clínicas recebidos de 01 a 11/11, comparada com a média de ago–out. Abre por prestador, unidade e motivo, mostra a janela entre a glosa e o recurso, responde quem está recursando o 7EY e checa se a melhoria na glosa por autorização se manteve.</p>
  <div class="scope">
    <span class="chip">Laboratório + Clínica · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 11/11/2026</span>
    <span class="chip">Sem o lote antigo da DASA (glosas de 2025) e sem os recursos de 7F6 de jul–ago</span>
    <span class="chip">Autorização = 7DL (até jun) e 7F8 (desde jul)</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Quanto subiu?</span>
      <span class="pill bad">2,8 vezes a média do início do mês</span>
      <span class="a">R$ 680 mil · 2.602 itens · 225 PEGs em 11 dias</span>
      <p>A média dos dias 01–11 em ago–out foi de R$ 240 mil. Em 11 dias, novembro já passou da média mensal de ago–out (R$ 564 mil) e deve terminar acima de R$ 900 mil, o maior mês do ano em valor.</p>
    </div>
    <div class="v">
      <span class="q">Por quê?</span>
      <span class="pill warn">Os dois grandes mandaram ao mesmo tempo</span>
      <span class="a">DASA R$ 319 mil · Fleury R$ 352 mil</span>
      <p>A DASA mandou a coorte de setembro inteira (43–64 dias), no ritmo dela. O Fleury mandou a coorte de setembro (45–56 dias) e já começou a de outubro, com 10–27 dias. Como o Fleury encurtou a janela, as entregas dos dois passaram a cair no mesmo começo de mês.</p>
    </div>
    <div class="v">
      <span class="q">Em qual motivo?</span>
      <span class="pill flat">7F6 e 7EK lideram</span>
      <span class="a">7F6 R$ 212 mil · 7EK R$ 173 mil · 7F8 R$ 137 mil</span>
      <p>O 7F6 (data incorreta) é o esperado do ajuste com a DASA (R$ 139 mil), mas o Fleury também recursa (R$ 66 mil). O 7EK é quase todo do Fleury. A autorização (7F8) vem da glosa de setembro, na taxa de sempre. O 7EY quase não aparece em laboratórios (R$ 14,5 mil).</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Volume por mês</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–11)</th></tr></thead>
      <tbody>
        <tr><td>Valor no mês (R$ mil)</td><td>460</td><td>907</td><td>716</td><td>150</td><td>826</td><td><b>680</b></td></tr>
        <tr><td>Valor nos dias 01–11 (R$ mil)</td><td>151</td><td>333</td><td>93</td><td>39</td><td>589</td><td><b>680</b></td></tr>
        <tr><td>Itens no mês</td><td>4.296</td><td>5.474</td><td>5.655</td><td>936</td><td>8.682</td><td><b>2.602</b></td></tr>
        <tr><td>PEGs no mês</td><td>420</td><td>436</td><td>387</td><td>97</td><td>332</td><td><b>225</b></td></tr>
      </tbody>
    </table>
    <p class="small muted">Em itens, novembro está bem abaixo de outubro: os lotes deste mês têm menos itens e valor maior por item (R$ 261 por item, contra R$ 95 em outubro). Outubro teve muitos itens de baixo valor do Fleury (7G9) e do Femme.</p>
  </div>
</section>

<section>
  <h2>2. Prestadores e unidades</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Grupo</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–11)</th><th>Coorte e dias em novembro</th></tr></thead>
      <tbody>
        <tr class="hl"><td>DASA</td><td>376</td><td>501</td><td>250</td><td>15</td><td>266</td><td><b>319</b></td><td class="wrap-cell">set, 43–64 dias</td></tr>
        <tr class="hl"><td>Fleury</td><td>1</td><td>345</td><td>342</td><td>119</td><td>458</td><td><b>352</b></td><td class="wrap-cell">set (R$ 199 mil, 45–56 dias) e out (R$ 149 mil, 10–27 dias)</td></tr>
        <tr><td>Femme</td><td>75</td><td>14</td><td>89</td><td>10</td><td>72</td><td><b>0</b></td><td class="wrap-cell">coorte de setembro ainda não chegou</td></tr>
      </tbody>
    </table>
    <p class="small muted">Valores em R$ mil, por mês de recebimento.</p>
  </div>
  <div class="panel tbl-wrap">
    <h3>Unidades em novembro (01–11)</h3>
    <table>
      <thead><tr><th>Unidade</th><th>Valor</th><th>Itens · PEGs</th><th>Média mensal ago–out</th><th>Principais motivos</th><th>Acato (analisado)</th></tr></thead>
      <tbody>
        <tr><td>Fleury (matriz)</td><td>R$ 296 mil</td><td>614 · 137</td><td>R$ 153 mil</td><td class="wrap-cell">7EK, 7F6, 7F8</td><td>R$ 23 mil de R$ 70 mil (33%)</td></tr>
        <tr class="hl"><td>Delboni São Paulo (DASA)</td><td>R$ 125 mil</td><td>194 · 86</td><td>R$ 49 mil</td><td class="wrap-cell">7F8 R$ 57 mil, 7F6 R$ 55 mil, 7G4 R$ 10 mil</td><td>R$ 71 mil de R$ 119 mil (60%)</td></tr>
        <tr><td>Delboni Barueri (DASA)</td><td>R$ 57 mil</td><td>670 · 118</td><td>R$ 29 mil</td><td class="wrap-cell">7G4 R$ 27 mil, 7EY R$ 9 mil</td><td>R$ 39 mil de R$ 49 mil</td></tr>
        <tr><td>Salomão São Paulo (DASA)</td><td>R$ 46 mil</td><td>234 · 76</td><td>R$ 31 mil</td><td class="wrap-cell">7G4, 7G3, 7EY</td><td>R$ 32 mil de R$ 46 mil</td></tr>
        <tr><td>Alta Alphaville (DASA)</td><td>R$ 32 mil</td><td>399 · 11</td><td>R$ 9 mil</td><td class="wrap-cell">7F6 R$ 24 mil</td><td>R$ 14 mil de R$ 21 mil</td></tr>
        <tr><td>Lavoisier São Paulo (DASA)</td><td>R$ 26 mil</td><td>40 · 24</td><td>R$ 8 mil</td><td class="wrap-cell">7F8 R$ 9 mil</td><td>R$ 9 mil de R$ 25 mil</td></tr>
        <tr><td>Fleury Santo André, Jundiaí, Alphaville</td><td>R$ 43 mil</td><td>157 · 33</td><td>R$ 4 mil</td><td class="wrap-cell">7EI R$ 10 mil (Santo André), 7EK, 7G9</td><td>–</td></tr>
      </tbody>
    </table>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill flat">Lote no calendário</span><h3>DASA: coorte de setembro inteira</h3>
      <p>R$ 319 mil, todos de glosas de setembro, com 43–64 dias, que é o ritmo da DASA. Representa 63% do que ela glosou em setembro (R$ 505 mil), dentro da faixa histórica. Nada novo da DASA entre 09 e 11/11.</p></div>
    <div class="panel prov"><span class="pill warn">Mudança de janela</span><h3>Fleury: recursa em 10–27 dias</h3>
      <p>A coorte de setembro chegou com 45–56 dias (em outubro eram 57 e, em agosto, 65–79). E já são R$ 149 mil de glosas de outubro recursadas com 10–27 dias. O Fleury passou de recursar fora do prazo para recursar logo depois da glosa. Até agora, só 33% do analisado foi acatado.</p></div>
  </div>
</section>

<section>
  <h2>3. Motivos</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Motivo</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–11)</th><th>Quem em novembro</th></tr></thead>
      <tbody>
        <tr class="hl"><td>7F6 · data incorreta</td><td>–</td><td>–</td><td>–</td><td>12</td><td>95</td><td><b>212</b></td><td class="wrap-cell">DASA R$ 139 mil (esperado), Fleury R$ 66 mil, Centro Diagnóstico R$ 7 mil</td></tr>
        <tr><td>7EK · sem registro de execução</td><td>113</td><td>188</td><td>95</td><td>59</td><td>149</td><td><b>173</b></td><td class="wrap-cell">Fleury R$ 169 mil</td></tr>
        <tr><td>7F8 · autorização</td><td>–</td><td>–</td><td>55</td><td>40</td><td>135</td><td><b>137</b></td><td class="wrap-cell">DASA R$ 80 mil (Delboni SP R$ 57 mil), Fleury R$ 57 mil</td></tr>
        <tr><td>7G4 · duplicidade</td><td>–</td><td>–</td><td>142</td><td>21</td><td>194</td><td><b>94</b></td><td class="wrap-cell">DASA R$ 68 mil, Fleury R$ 24 mil</td></tr>
        <tr><td>7G9 · local de atendimento</td><td>–</td><td>–</td><td>10</td><td>3</td><td>163</td><td>18</td><td class="wrap-cell">Fleury</td></tr>
        <tr><td>7EY · senha cancelada</td><td>3</td><td>72</td><td>42</td><td>3</td><td>36</td><td>15</td><td class="wrap-cell">DASA R$ 12,6 mil (Delboni Barueri, Salomão), Fleury R$ 1,9 mil</td></tr>
        <tr><td>7EI · unidade divergente da autorizada</td><td>18</td><td>6</td><td>–</td><td>–</td><td>–</td><td>10</td><td class="wrap-cell">Fleury Santo André</td></tr>
      </tbody>
    </table>
    <p class="small muted">Valores em R$ mil, por mês de recebimento. O código é o primeiro motivo do item.</p>
  </div>
</section>

<section>
  <h2>4. 7EY (senha cancelada) em laboratórios</h2>
  <div class="panel tbl-wrap">
    <h3>Glosa de 7EY por unidade e mês da glosa (glosado · recursado até 11/11)</h3>
    <table>
      <thead><tr><th>Unidade</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th></tr></thead>
      <tbody>
        <tr class="hl"><td>A+ Amais (Fleury)</td><td>19 · 10</td><td>19 · 3</td><td>48 · 27</td><td><b>166 · 0</b> (6.227 itens)</td><td>20 · 0</td></tr>
        <tr><td>Fleury (matriz)</td><td>23 · 18</td><td>15 · 0</td><td>36 · 0</td><td>24 · 2</td><td>22 · 0</td></tr>
        <tr><td>Delboni Barueri (DASA)</td><td>3 · 0</td><td>–</td><td>34 · 2</td><td>33 · 9</td><td>15 · 0</td></tr>
        <tr><td>Salomão São Paulo (DASA)</td><td>3 · 2</td><td>4 · 0</td><td>10 · 0</td><td>21 · 2</td><td>6 · 0</td></tr>
      </tbody>
    </table>
    <p class="small muted">Valores em R$ mil. Em novembro, o recurso de 7EY em laboratórios foi de R$ 14,5 mil, quase todo da DASA. O 7EY de R$ 124 mil citado no indicador de novembro é, na maior parte, do HCor (R$ 110 mil), que é hospital.</p>
  </div>
  <div class="panel">
    <p><b>O problema de senhas do Fleury está na A+ Amais.</b> Foram R$ 166 mil e 6,2 mil itens de 7EY glosados em setembro, contra R$ 19–48 mil nos meses anteriores. Nada foi recursado até 11/11. O Fleury já recursou a coorte de setembro de outros motivos (7EK, 7F6, 7F8), mas não esse lote. Se ele vier, é o maior volume de itens a entrar na fila de uma vez.</p>
  </div>
</section>

<section>
  <h2>5. Janela de envio</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês do recurso</th><th>0–15</th><th>16–30</th><th>31–45</th><th>46–60</th><th>Mais de 60</th></tr></thead>
      <tbody>
        <tr><td>Ago</td><td>1%</td><td>0%</td><td>32%</td><td>19%</td><td>48%</td></tr>
        <tr><td>Set</td><td>0%</td><td>0%</td><td>19%</td><td>35%</td><td>46%</td></tr>
        <tr><td>Out</td><td>0%</td><td>0%</td><td>22%</td><td>67%</td><td>11%</td></tr>
        <tr class="hl"><td>Nov (01–11)</td><td>5%</td><td>17%</td><td>4%</td><td>73%</td><td>1%</td></tr>
      </tbody>
    </table>
    <p class="small muted">% do valor recebido por dias entre a glosa e o recurso. Os 22% com até 30 dias são o Fleury recursando glosas de outubro.</p>
  </div>
</section>

<section>
  <h2>6. Autorização: a melhoria se manteve?</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês da glosa</th><th>Glosa de autorização</th><th>% do apresentado</th><th>% da glosa do mês</th><th>Recurso da coorte (até 11/11)</th><th>% do recurso da coorte</th><th>% recursado</th></tr></thead>
      <tbody>
        <tr><td>Abr</td><td>R$ 424 mil · 3.054 itens</td><td>2,81%</td><td>34%</td><td>R$ 237 mil</td><td>42%</td><td>56%</td></tr>
        <tr><td>Mai</td><td>R$ 626 mil · 3.762 itens</td><td>4,46%</td><td>55%</td><td>R$ 373 mil</td><td>55%</td><td>60%</td></tr>
        <tr><td>Jul</td><td>R$ 204 mil · 1.163 itens</td><td>1,34%</td><td>20%</td><td>R$ 94 mil</td><td>21%</td><td>46%</td></tr>
        <tr><td>Ago</td><td>R$ 255 mil · 1.729 itens</td><td>1,45%</td><td>19%</td><td>R$ 132 mil</td><td>16%</td><td>52%</td></tr>
        <tr><td>Set</td><td>R$ 260 mil · 1.772 itens</td><td>1,47%</td><td>17%</td><td>R$ 117 mil</td><td>21%</td><td>45%</td></tr>
        <tr class="hl"><td>Out</td><td>R$ 299 mil · 1.316 itens</td><td><b>1,74%</b></td><td>17%</td><td>R$ 26 mil</td><td>–</td><td>em aberto</td></tr>
      </tbody>
    </table>
    <p class="small muted">Junho fica fora porque o pico pontual de 7F6 distorce a participação. Novembro ainda está parcial: R$ 60 mil de glosa de autorização até 11/11 (0,47% do apresentado lançado até agora).</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Se mantém</span><h3>Glosa e peso no recurso seguem baixos</h3>
      <p>A glosa por autorização segue em 17% da glosa total, e o motivo responde por 16–21% do recurso das coortes de julho a setembro, contra 42–55% antes da mudança. O % recursado segue em 45–52%, dentro do histórico.</p></div>
    <div class="panel prov"><span class="pill warn">Atenção</span><h3>Outubro subiu em valor, puxado pela DASA</h3>
      <p>R$ 299 mil em outubro (1,74% do apresentado), contra R$ 255–260 mil em agosto e setembro. A DASA passou de R$ 132 mil para R$ 170 mil, com menos itens e valor maior por item. Se a DASA recursar no ritmo habitual (~60%), isso aparece como ~R$ 100 mil de recurso de autorização em dezembro.</p></div>
  </div>
</section>

<section>
  <h2>7. O que vem pela frente</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Origem</th><th>Glosado</th><th>Recursado até 11/11</th><th>Quando deve chegar</th></tr></thead>
      <tbody>
        <tr><td>Fleury, coorte de setembro</td><td>R$ 880 mil</td><td>R$ 199 mil (23%)</td><td class="wrap-cell">Restante ainda em novembro, se mantiver os 40–55% habituais</td></tr>
        <tr class="hl"><td>A+ Amais (Fleury), 7EY de setembro</td><td>R$ 166 mil · 6,2 mil itens</td><td>R$ 0</td><td class="wrap-cell">Sem data. Depende de o Fleury tratar o problema de senhas</td></tr>
        <tr><td>Femme, coorte de setembro</td><td>R$ 74 mil</td><td>R$ 0</td><td class="wrap-cell">Fim de novembro (Femme recursa ~85%)</td></tr>
        <tr class="hl"><td>DASA, 7F6 de outubro e novembro</td><td>R$ 480 mil (out) + R$ 229 mil (nov até 11/11)</td><td>–</td><td class="wrap-cell">Dezembro em diante, pelo ritmo da DASA (~50 dias)</td></tr>
        <tr><td>DASA e Fleury, glosas de outubro</td><td>Glosa total de R$ 1,75 mi em outubro (10,2% do apresentado)</td><td>Fleury já começou</td><td class="wrap-cell">Fleury em novembro; DASA em dezembro</td></tr>
      </tbody>
    </table>
    <p class="small muted">7F6 pelo primeiro motivo do item. A glosa de 7F6 da DASA continua alta em novembro: R$ 229 mil em 11 dias.</p>
  </div>
  <div class="panel">
    <ol class="steps">
      <li><b>Novembro deve passar de R$ 900 mil</b> em laboratórios, com o restante do Fleury de setembro e o Femme. Se a A+ Amais mandar o 7EY, passa de R$ 1 mi e de 8 mil itens.</li>
      <li><b>Fleury:</b> a janela encurtou para 10–27 dias nas glosas de outubro. A fila de análise vai receber o Fleury todo mês, logo depois da glosa, em vez de dois meses depois.</li>
      <li><b>DASA, 7F6:</b> a glosa segue subindo (R$ 480 mil em outubro e R$ 229 mil em 11 dias de novembro). O recurso desse motivo vai crescer em dezembro, como alinhado.</li>
      <li><b>Autorização:</b> confirmar em novembro se a alta de outubro da DASA (R$ 170 mil) se repete.</li>
    </ol>
  </div>
  <p class="small muted">Relatórios relacionados: <a href="https://claude.ai/artifact/MUhd7cHLZUAcVqrXjbUwqh" target="_blank" rel="noopener">Recurso de Glosa em Novembro: Hospitais</a> · <a href="https://claude.ai/artifact/3FGMMQh3REyXxWpXtL1VPS" target="_blank" rel="noopener">Recurso de Glosa em Novembro (geral, até 09/11)</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 11/11. Não é tempo real.</p>
</section>
"""
open('recurso-laboratorios-novembro.html','w').write(page("Recurso Laboratórios Novembro", body, ""))
