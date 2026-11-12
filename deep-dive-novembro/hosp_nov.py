import sys
sys.path.insert(0, '../aumento-recurso-outubro/relatorios')
from common import page
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Deep dive · Hospitais · Nov/26 · dados até 11/11</span>
  <h1>Recurso de Glosa em Novembro: Hospitais</h1>
  <p class="muted">Análise dos recursos de hospitais recebidos de 01 a 11/11, comparada com a média de ago–out. Abre por hospital e motivo, mostra a janela entre a glosa e o recurso e checa o que está acontecendo com HCor e com o grupo Américas (Nove de Julho Alphaville e Santa Paula).</p>
  <div class="scope">
    <span class="chip">Hospital · Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos até 11/11/2026</span>
    <span class="chip">Base de comparação: média de ago–out no mês inteiro e nos dias 01–11</span>
    <span class="chip">Autorização = 7DL (até jun) e 7F8 (desde jul)</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">O recurso de hospitais subiu em novembro?</span>
      <span class="pill good">Não. No total, está na média</span>
      <span class="a">R$ 478 mil · 617 itens · 92 PEGs</span>
      <p>A média dos dias 01–11 em ago–out foi de R$ 484 mil. O que mudou foi a composição: HCor e o grupo Américas subiram, enquanto Sírio, CIP Pacaembu, HAOC e Einstein vieram bem abaixo.</p>
    </div>
    <div class="v">
      <span class="q">HCor e Américas: pontual ou comportamento?</span>
      <span class="pill warn">HCor: atraso recorrente. Américas: lote de setembro</span>
      <span class="a">HCor R$ 157 mil fora do prazo · Américas R$ 159 mil</span>
      <p>O HCor recursa só depois de 60 dias pelo segundo mês seguido, e o valor deste mês está concentrado num PEG de 7EY (R$ 92 mil). No Américas, Nove de Julho Alphaville e Santa Paula estão recursando a glosa de 7F8 de setembro, que foi alta no grupo, dentro do prazo.</p>
    </div>
    <div class="v">
      <span class="q">O que vem pela frente?</span>
      <span class="pill good">Menos recurso de autorização</span>
      <span class="a">Glosa 7F8 caiu de 2,4% para 0,9% do apresentado</span>
      <p>Em outubro, a glosa por autorização em hospitais foi de R$ 383 mil, contra R$ 935 mil em agosto e setembro. Como hospitais recursam rápido e 77–80% dessa glosa vinha sendo recursada, o recurso de autorização tende a cair nas próximas semanas.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Volume por mês</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–11)</th></tr></thead>
      <tbody>
        <tr><td>Valor no mês (R$ mil)</td><td>771</td><td>897</td><td>803</td><td>956</td><td>1.374</td><td><b>478</b></td></tr>
        <tr><td>Valor nos dias 01–11 (R$ mil)</td><td>227</td><td>500</td><td>310</td><td>507</td><td>634</td><td><b>478</b></td></tr>
        <tr><td>Itens no mês</td><td>916</td><td>864</td><td>1.802</td><td>1.316</td><td>2.006</td><td><b>617</b></td></tr>
        <tr><td>PEGs no mês</td><td>185</td><td>153</td><td>165</td><td>153</td><td>195</td><td><b>92</b></td></tr>
      </tbody>
    </table>
    <p class="small muted">Novembro está 1% abaixo da média dos dias 01–11 de ago–out (R$ 484 mil). A média mensal de ago–out é de R$ 1,04 mi.</p>
  </div>
</section>

<section>
  <h2>2. Hospitais em novembro contra a própria média</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Hospital</th><th>Nov (01–11)</th><th>Itens · PEGs</th><th>Média mensal ago–out</th><th>Histórico mensal (jun → out)</th><th>Coorte e dias</th><th>Principais motivos</th></tr></thead>
      <tbody>
        <tr class="hl"><td>HCor</td><td>R$ 157 mil</td><td>187 · 14</td><td>R$ 81 mil</td><td>108 · 84 · 0 · 21 · 221</td><td class="wrap-cell">ago (77–84 dias) e set (61 dias). 100% fora do prazo</td><td class="wrap-cell">7EY R$ 110 mil, 7E1 R$ 26 mil, 7F8 R$ 20 mil</td></tr>
        <tr class="hl"><td>Nove de Julho Alphaville (Américas)</td><td>R$ 99 mil</td><td>35 · 14</td><td>R$ 23 mil</td><td>0 · 0 · 10 · 7 · 50</td><td class="wrap-cell">set (45–60 dias)</td><td class="wrap-cell">7F8 R$ 49 mil, 7EL R$ 37 mil, 7DV R$ 7 mil, 7G1 R$ 5 mil</td></tr>
        <tr class="hl"><td>Santa Paula (Américas)</td><td>R$ 57 mil</td><td>57 · 11</td><td>R$ 27 mil</td><td>9 · 4 · 0 · 48 · 32</td><td class="wrap-cell">set (53–56 dias) e out (25–29 dias)</td><td class="wrap-cell">7F8 R$ 55 mil</td></tr>
        <tr><td>HAOC</td><td>R$ 49 mil</td><td>82 · 10</td><td>R$ 100 mil</td><td>32 · 16 · 126 · 116 · 58</td><td>set</td><td class="wrap-cell">7E1 R$ 22 mil, 7G3 R$ 13 mil, 7DJ R$ 8 mil</td></tr>
        <tr><td>Sírio</td><td>R$ 27 mil</td><td>44 · 11</td><td>R$ 194 mil</td><td>55 · 64 · 121 · 307 · 155</td><td class="wrap-cell">nov (1 dia)</td><td class="wrap-cell">7F8 R$ 19 mil, 7G7 R$ 5 mil</td></tr>
        <tr><td>Einstein</td><td>R$ 23 mil</td><td>18 · 9</td><td>R$ 40 mil</td><td>82 · 37 · 3 · 0 · 118</td><td>ago–set</td><td class="wrap-cell">505 R$ 11 mil, 7DV R$ 7 mil</td></tr>
        <tr><td>Santa Marcelina</td><td>R$ 19 mil</td><td>32 · 2</td><td>R$ 30 mil</td><td>0 · 0 · 25 · 0 · 64</td><td class="wrap-cell">set (51 dias)</td><td class="wrap-cell">7F8 R$ 19 mil</td></tr>
        <tr><td>CIP Pacaembu</td><td>R$ 17 mil</td><td>4 · 2</td><td>R$ 88 mil</td><td>0 · 25 · 8 · 96 · 160</td><td>set</td><td class="wrap-cell">7F8 R$ 9 mil, 505 R$ 8 mil</td></tr>
      </tbody>
    </table>
    <p class="small muted">Por grupo: Américas R$ 159 mil (média mensal de R$ 152 mil e média dos dias 01–11 de R$ 72 mil), HCor R$ 157 mil (R$ 89 mil e R$ 60 mil). Abaixo: Sírio R$ 27 mil (média mensal de R$ 194 mil), CIP R$ 17 mil (R$ 88 mil), HAOC R$ 49 mil (R$ 100 mil).</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill bad">Comportamento</span><h3>HCor: recurso sempre depois de 60 dias</h3>
      <p>Em outubro foram R$ 221 mil e em novembro já são R$ 157 mil, tudo com mais de 60 dias. Neste mês, o valor está num PEG com 5 itens de 7EY (R$ 91,8 mil), glosados em setembro e recursados com 61 dias. Mais 7 itens de 7EY e glosas de agosto de 7F8 e 7E1 vieram com 77–84 dias. O atraso é recorrente; o valor é pontual. Do pouco já analisado, R$ 8,7 mil de R$ 10,7 mil foram acatados.</p></div>
    <div class="panel prov"><span class="pill warn">Lote dentro do prazo</span><h3>Américas: glosa de autorização de setembro voltando</h3>
      <p>O grupo Américas teve R$ 162 mil de glosa 7F8 em setembro, contra R$ 21–58 mil em julho e agosto. Esse volume está voltando agora como recurso, com 45–60 dias: Nove de Julho Alphaville (7F8 e 7EL) e Santa Paula (7F8). O grupo já passou da média mensal em 11 dias. É lote de uma coorte grande, no prazo, e não mudança de comportamento.</p></div>
  </div>
</section>

<section>
  <h2>3. Motivos</h2>
  <div class="panel tbl-wrap">
    <h3>Valor recursado por motivo e mês de recebimento (R$ mil)</h3>
    <table>
      <thead><tr><th>Motivo</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–11)</th><th>Quem em novembro</th></tr></thead>
      <tbody>
        <tr><td>7F8 · autorização</td><td>–</td><td>12</td><td>342</td><td>752</td><td>676</td><td><b>194</b></td><td class="wrap-cell">Santa Paula R$ 55 mil, Nove de Julho Alphaville R$ 49 mil, HCor R$ 20 mil, Santa Marcelina R$ 19 mil, Sírio R$ 19 mil</td></tr>
        <tr class="hl"><td>7EY · senha cancelada</td><td>–</td><td>5</td><td>15</td><td>42</td><td>13</td><td><b>111</b></td><td class="wrap-cell">HCor R$ 110 mil (um PEG)</td></tr>
        <tr><td>7E1 · valor divergente do negociado</td><td>16</td><td>20</td><td>18</td><td>26</td><td>89</td><td><b>53</b></td><td class="wrap-cell">HCor R$ 26 mil, HAOC R$ 22 mil</td></tr>
        <tr><td>7EL · código diferente do autorizado</td><td>1</td><td>1</td><td>13</td><td>20</td><td>87</td><td><b>38</b></td><td class="wrap-cell">Nove de Julho Alphaville</td></tr>
        <tr><td>505 · família bloqueada</td><td>–</td><td>–</td><td>–</td><td>–</td><td>16</td><td>19</td><td class="wrap-cell">Einstein, CIP</td></tr>
        <tr><td>7G3 · duplicidade de conta</td><td>–</td><td>49</td><td>6</td><td>36</td><td>9</td><td>17</td><td class="wrap-cell">HAOC</td></tr>
        <tr><td>7DJ · conta não localizada no capeante</td><td>212</td><td>181</td><td>82</td><td>30</td><td>289</td><td>8</td><td class="wrap-cell">HAOC</td></tr>
      </tbody>
    </table>
    <p class="small muted">O código é o primeiro motivo do item. O 7DJ, que puxou outubro (HCor e Santa Joana), quase não aparece em novembro.</p>
  </div>
</section>

<section>
  <h2>4. Janela de envio</h2>
  <div class="panel tbl-wrap">
    <h3>% do valor recebido por dias entre a glosa e o recurso</h3>
    <table>
      <thead><tr><th>Mês do recurso</th><th>0–15</th><th>16–30</th><th>31–45</th><th>46–60</th><th>Mais de 60</th></tr></thead>
      <tbody>
        <tr><td>Ago</td><td>34%</td><td>4%</td><td>21%</td><td>34%</td><td>7%</td></tr>
        <tr><td>Set</td><td>48%</td><td>12%</td><td>16%</td><td>17%</td><td>7%</td></tr>
        <tr><td>Out</td><td>13%</td><td>24%</td><td>10%</td><td>20%</td><td><b>33%</b></td></tr>
        <tr class="hl"><td>Nov (01–11)</td><td>14%</td><td>5%</td><td>6%</td><td>41%</td><td><b>34%</b></td></tr>
      </tbody>
    </table>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill bad">Fora do prazo</span><h3>Um terço do valor chega depois de 60 dias</h3>
      <p>R$ 162 mil em novembro, todo do HCor. Em outubro foram R$ 401 mil (HCor, Einstein, Santa Marcelina, SMA). Em agosto e setembro, eram 7%.</p></div>
    <div class="panel prov"><span class="pill warn">Mais lento</span><h3>Menos recurso imediato</h3>
      <p>O recurso em até 15 dias, que era 34–48% em agosto e setembro, está em 13–14% desde outubro. Sírio e HAOC, que respondiam por esse volume, estão mandando menos e mais tarde. O que cresce é a faixa de 46–60 dias (Américas).</p></div>
  </div>
</section>

<section>
  <h2>5. Glosa de hospitais: o que vai alimentar os próximos recursos</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês da glosa</th><th>Autorização (7F8)</th><th>% do apresentado</th><th>Demais motivos</th><th>Glosa total em % do apresentado</th><th>% recursado até agora (autorização · demais)</th></tr></thead>
      <tbody>
        <tr><td>Jun</td><td>R$ 536 mil</td><td>1,37%</td><td>R$ 634 mil</td><td>3,0%</td><td>71% · 60%</td></tr>
        <tr><td>Jul</td><td>R$ 738 mil</td><td>1,87%</td><td>R$ 813 mil</td><td>3,9%</td><td>55% · 43%</td></tr>
        <tr><td>Ago</td><td>R$ 945 mil</td><td>2,43%</td><td>R$ 735 mil</td><td>4,3%</td><td>80% · 55%</td></tr>
        <tr><td>Set</td><td>R$ 936 mil</td><td>2,38%</td><td>R$ 923 mil</td><td>4,7%</td><td>77% · 44%</td></tr>
        <tr class="hl"><td>Out</td><td><b>R$ 383 mil</b></td><td><b>0,92%</b></td><td>R$ 577 mil</td><td><b>2,3%</b></td><td>40% · 16% (em curso)</td></tr>
      </tbody>
    </table>
    <p class="small muted">Glosa pela data da glosa. Apresentado pelo mês da conta (outubro: R$ 41,4 mi). A glosa de outubro ainda pode crescer um pouco se houver análises lançadas com atraso.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Queda</span><h3>A glosa de autorização caiu pela metade em outubro</h3>
      <p>De R$ 935–945 mil por mês em agosto e setembro para R$ 383 mil em outubro. A glosa total de hospitais também caiu, de 4,3–4,7% para 2,3% do apresentado. Como 77–80% da glosa de autorização era recursada, a menor glosa deve reduzir o recurso de hospitais em novembro e dezembro.</p></div>
    <div class="panel prov"><span class="pill flat">Para confirmar</span><h3>Vale entender o que mudou</h3>
      <p>A queda pode ser ajuste da regra 7F8 para hospitais, mudança no faturamento ou atraso no lançamento das análises de outubro. Vale confirmar com o time de regras antes de tratar como tendência.</p></div>
  </div>
</section>

<section>
  <h2>6. O que acompanhar</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>HCor:</b> R$ 378 mil em dois meses, sempre depois de 60 dias. Definir a regra para recurso fora do prazo e alinhar o envio com o hospital.</li>
      <li><b>Grupo Américas:</b> o lote de 7F8 de setembro (R$ 162 mil glosados) está voltando. Acompanhar o acato: no histórico do grupo, 93% do 7F8 recursado foi acatado em agosto.</li>
      <li><b>Glosa 7F8 em hospitais:</b> confirmar se a queda de outubro (0,92% do apresentado) é ajuste da regra ou atraso de lançamento.</li>
      <li><b>Sírio e HAOC:</b> vieram bem abaixo da própria média. Se forem só mais lentos, o recurso deles pode chegar na segunda metade do mês.</li>
    </ol>
  </div>
  <p class="small muted">Relatórios relacionados: <a href="https://claude.ai/artifact/3FGMMQh3REyXxWpXtL1VPS" target="_blank" rel="noopener">Recurso de Glosa em Novembro (geral, até 09/11)</a> · <a href="https://claude.ai/artifact/MHdaoDwAcjZL5b8ZC7XXPY" target="_blank" rel="noopener">Deep dive de outubro: hospitais</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 11/11. Não é tempo real.</p>
</section>
"""
open('recurso-hospitais-novembro.html','w').write(page("Recurso Hospitais Novembro", body, ""))
