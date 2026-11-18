import sys
sys.path.insert(0, '../aumento-recurso-outubro/relatorios')
from common import page
body = r"""
<style>.v .pill, .chip { white-space: normal; }</style>
<header>
  <span class="eyebrow">Projeto Recurso de Glosa · Indicador · Nov/26 · dados até 17/11</span>
  <h1>Indicador de Recurso de Glosa: Novembro</h1>
  <p class="muted">Responde se o recurso subiu em relação a outubro, qual motivo puxa, como está a janela entre glosa e recurso, se há desvio e se o volume é coerente com o que foi glosado, incluindo o % recursado das coortes maduras.</p>
  <div class="scope">
    <span class="chip">Health Institution · totvs-alice · fases 1 a 4</span>
    <span class="chip">Recursos de 01 a 17/11/2026, comparados com 01 a 17 dos meses anteriores</span>
    <span class="chip">Sem o lote antigo da DASA (glosas de 2025) e sem os recursos de 7F6 de jul–ago</span>
  </div>
</header>

<section>
  <h2>Resposta curta</h2>
  <div class="verdict">
    <div class="v">
      <span class="q">Aumentou contra outubro?</span>
      <span class="pill flat">No total, não</span>
      <span class="a">R$ 1,49 mi (01–17/11) × R$ 1,60 mi (01–17/10): −7%</span>
      <p>Laboratórios subiram 48% (R$ 985 mil × R$ 668 mil) e já passaram do mês de outubro inteiro. Hospitais caíram 46% (R$ 506 mil × R$ 937 mil). Contra a média de 01–17 de ago–out (R$ 979 mil), o total está 52% acima, tudo por causa de laboratórios.</p>
    </div>
    <div class="v">
      <span class="q">É coerente com a glosa?</span>
      <span class="pill good">Sim, acompanha a glosa</span>
      <span class="a">Glosa de laboratórios: R$ 1,02 mi (jul) → 1,35 (ago) → 1,53 (set) → 1,75 (out)</span>
      <p>O recurso de novembro vem da glosa de setembro, a maior até então. A glosa subiu de 6,7% para 10,2% do apresentado em laboratórios, puxada pelo 7F6. Em hospitais, a glosa de outubro caiu pela metade (R$ 960 mil), e o recurso caiu junto.</p>
    </div>
    <div class="v">
      <span class="q">O % recursado mudou?</span>
      <span class="pill flat">Estável no total, menor sem o 7F6</span>
      <span class="a">Coortes maduras: abr 65% · mai 64% · ago 65% · set 58% (ainda amadurecendo)</span>
      <p>Sem o 7F6, setembro está em 55% contra 65% em agosto. Em hospitais, o % segue estável ou um pouco menor (62% em set contra 69% em ago). Em laboratórios, ele subiu de ago em diante porque o Fleury passou a recursar mais. O único desvio de comportamento é o Fleury, que antecipou o envio.</p>
    </div>
  </div>
</section>

<section>
  <h2>1. Novembro contra outubro</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th></th><th>Ago</th><th>Set</th><th>Out</th><th>Nov</th><th>Nov × Out</th></tr></thead>
      <tbody>
        <tr><td colspan="6"><b>Valor recebido nos dias 01–17 (R$ mil)</b></td></tr>
        <tr><td>Laboratórios e clínicas</td><td>112</td><td>140</td><td>668</td><td><b>985</b></td><td>+48%</td></tr>
        <tr><td>Hospitais</td><td>410</td><td>668</td><td>937</td><td><b>506</b></td><td>−46%</td></tr>
        <tr class="hl"><td>Total</td><td>522</td><td>808</td><td>1.605</td><td><b>1.491</b></td><td>−7%</td></tr>
        <tr><td colspan="6"><b>Valor recebido no mês inteiro (R$ mil)</b></td></tr>
        <tr><td>Laboratórios e clínicas</td><td>716</td><td>150</td><td>824</td><td>985 (até 17)</td><td>já passou</td></tr>
        <tr><td>Hospitais</td><td>803</td><td>956</td><td>1.374</td><td>506 (até 17)</td><td></td></tr>
        <tr><td colspan="6"><b>Itens e PEGs nos dias 01–17</b></td></tr>
        <tr><td>Laboratórios: itens · PEGs</td><td>1.433 · 101</td><td>907 · 76</td><td>4.746 · 280</td><td><b>5.284 · 374</b></td><td>+11% · +34%</td></tr>
        <tr><td>Hospitais: itens · PEGs</td><td>888 · 79</td><td>638 · 83</td><td>908 · 110</td><td><b>655 · 109</b></td><td>−28% · −1%</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel">
    <p><b>Como novembro deve fechar:</b> laboratórios entre R$ 1,1 e 1,4 mi. Ainda faltam o Femme de setembro (~R$ 60 mil), o restante do Fleury de outubro e o início da DASA de outubro, que tem 50 dias de janela e começa a vencer a partir de 20/11. Hospitais devem ficar entre R$ 0,8 e 1,0 mi. O total deve fechar perto de outubro (R$ 2,2 mi), com mais laboratório e menos hospital.</p>
  </div>
</section>

<section>
  <h2>2. Principal motivo</h2>
  <div class="grid2">
    <div class="panel tbl-wrap">
      <h3>Laboratórios: recebido por motivo (R$ mil)</h3>
      <table>
        <thead><tr><th>Motivo</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–17)</th></tr></thead>
        <tbody>
          <tr class="hl"><td>7F6 · data incorreta</td><td>0</td><td>12</td><td>91</td><td><b>290</b></td></tr>
          <tr class="hl"><td>7EK · sem registro de execução</td><td>95</td><td>59</td><td>148</td><td><b>282</b></td></tr>
          <tr><td>7F8 · autorização</td><td>55</td><td>40</td><td>135</td><td><b>191</b></td></tr>
          <tr><td>7G4 · duplicidade</td><td>142</td><td>21</td><td>194</td><td><b>148</b></td></tr>
          <tr><td>7G9 · local de atendimento</td><td>10</td><td>3</td><td>163</td><td>18</td></tr>
          <tr><td>7EY · senha cancelada</td><td>42</td><td>3</td><td>36</td><td>15</td></tr>
        </tbody>
      </table>
      <p class="small muted">7F6: DASA (esperado, pelo ajuste combinado) e Fleury. 7EK: quase todo do Fleury.</p>
    </div>
    <div class="panel tbl-wrap">
      <h3>Hospitais: recebido por motivo (R$ mil)</h3>
      <table>
        <thead><tr><th>Motivo</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (01–17)</th></tr></thead>
        <tbody>
          <tr class="hl"><td>7F8 · autorização</td><td>342</td><td>752</td><td>672</td><td><b>208</b></td></tr>
          <tr><td>7EY · senha cancelada</td><td>15</td><td>42</td><td>13</td><td><b>111</b></td></tr>
          <tr><td>7E1 · preço</td><td>18</td><td>26</td><td>93</td><td>52</td></tr>
          <tr><td>7EL</td><td>13</td><td>20</td><td>87</td><td>37</td></tr>
          <tr><td>7DJ</td><td>82</td><td>30</td><td>289</td><td>8</td></tr>
        </tbody>
      </table>
      <p class="small muted">7F8: Américas, da glosa de setembro. 7EY: HCor (lote da glosa de setembro).</p>
    </div>
  </div>
</section>

<section>
  <h2>3. Janela entre glosa e recurso</h2>
  <div class="grid2">
    <div class="panel tbl-wrap">
      <h3>Laboratórios (% do valor recebido)</h3>
      <table>
        <thead><tr><th>Mês</th><th>0–30</th><th>31–45</th><th>46–60</th><th>Mais de 60</th></tr></thead>
        <tbody>
          <tr><td>Ago</td><td>1%</td><td>32%</td><td>19%</td><td>48%</td></tr>
          <tr><td>Set</td><td>0%</td><td>19%</td><td>35%</td><td>46%</td></tr>
          <tr><td>Out</td><td>0%</td><td>21%</td><td>68%</td><td>11%</td></tr>
          <tr class="hl"><td>Nov (01–17)</td><td><b>18%</b></td><td>2%</td><td>75%</td><td>4%</td></tr>
        </tbody>
      </table>
      <p class="small muted">Dentro do prazo de 60 dias em 96% do valor. Os 18% com até 30 dias são o Fleury, que já mandou R$ 182 mil de glosas de outubro (mediana de 22 dias). DASA e Fleury de setembro chegaram com mediana de 52–53 dias.</p>
    </div>
    <div class="panel tbl-wrap">
      <h3>Hospitais (% do valor recebido)</h3>
      <table>
        <thead><tr><th>Mês</th><th>0–30</th><th>31–45</th><th>46–60</th><th>Mais de 60</th></tr></thead>
        <tbody>
          <tr><td>Ago</td><td>38%</td><td>21%</td><td>34%</td><td>7%</td></tr>
          <tr><td>Set</td><td>60%</td><td>16%</td><td>17%</td><td>7%</td></tr>
          <tr><td>Out</td><td>37%</td><td>10%</td><td>20%</td><td>33%</td></tr>
          <tr class="hl"><td>Nov (01–17)</td><td>19%</td><td>7%</td><td>40%</td><td><b>35%</b></td></tr>
        </tbody>
      </table>
      <p class="small muted">A janela dos hospitais ficou mais longa. Os 35% acima de 60 dias são, na maior parte, o HCor, com mediana de 61 dias na glosa de setembro e de 82 dias na de agosto (R$ 52 mil). Américas: 55 dias.</p>
    </div>
  </div>
</section>

<section>
  <h2>4. O volume de recurso acompanha a glosa?</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês da glosa</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set</th><th>Out</th><th>Nov (até 17)</th></tr></thead>
      <tbody>
        <tr><td>Glosa de laboratórios (R$ mil)</td><td>1.256</td><td>1.146</td><td>2.185</td><td>1.017</td><td>1.352</td><td>1.532</td><td><b>1.754</b></td><td>959</td></tr>
        <tr><td>% do apresentado</td><td>8,3%</td><td>8,2%</td><td>14,1%</td><td>6,7%</td><td>7,7%</td><td>8,7%</td><td><b>10,2%</b></td><td>7,2%</td></tr>
        <tr><td>dos quais 7F6 (R$ mil)</td><td>–</td><td>–</td><td>700</td><td>51</td><td>138</td><td>309</td><td><b>595</b></td><td>425</td></tr>
        <tr><td>Glosa de hospitais (R$ mil)</td><td>1.226</td><td>1.310</td><td>1.171</td><td>1.550</td><td>1.681</td><td>1.859</td><td><b>960</b></td><td>1.085</td></tr>
        <tr><td>% do apresentado</td><td>3,4%</td><td>3,6%</td><td>3,0%</td><td>3,9%</td><td>4,3%</td><td>4,7%</td><td><b>2,3%</b></td><td>3,4%</td></tr>
      </tbody>
    </table>
    <p class="small muted">Laboratórios recursam em 45–60 dias, então o recurso de novembro é a glosa de setembro (R$ 776 mil) mais o Fleury de outubro (R$ 182 mil). Hospitais recursam mais rápido, por isso a glosa baixa de outubro já reduziu o recurso de novembro.</p>
  </div>
  <div class="grid2">
    <div class="panel prov"><span class="pill good">Coerente</span><h3>Laboratórios: subiu a glosa, subiu o recurso</h3>
      <p>Não há mais recurso por real glosado. O recurso cresce porque a glosa cresceu, principalmente o 7F6 da DASA (R$ 51 mil em jul, R$ 595 mil em out). A DASA dobrou a glosa em outubro (R$ 1,03 mi contra R$ 506 mil em setembro). Com o ~60% habitual da DASA, isso vira cerca de R$ 600 mil de recurso entre o fim de novembro e dezembro.</p></div>
    <div class="panel prov"><span class="pill warn">Atenção à frente</span><h3>Hospitais: novembro já tem R$ 1,1 mi de glosa</h3>
      <p>Em 17 dias, a glosa de hospitais de novembro já passou do mês de outubro. São R$ 704 mil em 7DJ, a maior parte do HCor (R$ 646 mil). O HCor recursa 57–94% e costuma passar de 60 dias, então isso deve aparecer em janeiro.</p></div>
  </div>
</section>

<section>
  <h2>5. % recursado das glosas maduras</h2>
  <div class="panel tbl-wrap">
    <table>
      <thead><tr><th>Mês da glosa</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set*</th></tr></thead>
      <tbody>
        <tr><td colspan="7"><b>Total recursado até 17/11 ÷ glosado</b></td></tr>
        <tr class="hl"><td>Total</td><td>65%</td><td>64%</td><td>45%</td><td>45%</td><td>65%</td><td>58%</td></tr>
        <tr><td>Total sem 7F6</td><td>65%</td><td>64%</td><td>57%</td><td>46%</td><td>65%</td><td>55%</td></tr>
        <tr><td>Laboratórios</td><td>45%</td><td>59%</td><td>35%</td><td>40%</td><td>60%</td><td>53%</td></tr>
        <tr><td>Laboratórios sem 7F6</td><td>45%</td><td>59%</td><td>51%</td><td>41%</td><td>60%</td><td>44%</td></tr>
        <tr><td>Hospitais</td><td>87%</td><td>69%</td><td>65%</td><td>49%</td><td>69%</td><td>62%</td></tr>
        <tr><td colspan="7"><b>Recursado em até 45 dias da glosa (mesma régua para todas as coortes)</b></td></tr>
        <tr><td>Total</td><td>28%</td><td>35%</td><td>22%</td><td>21%</td><td>25%</td><td>25%</td></tr>
        <tr><td>Hospitais</td><td>47%</td><td>49%</td><td>40%</td><td>18%</td><td>36%</td><td>43%</td></tr>
      </tbody>
    </table>
    <p class="small muted">* Setembro ainda amadurece: as glosas da segunda quinzena não completaram 60 dias. Faltam o Femme (R$ 74 mil glosados, recursa ~85%) e o 7EY da A+ Amais (R$ 166 mil, nada recursado). Em junho, os recursos de 7F6 de jul–ago foram excluídos, e por isso a taxa com 7F6 fica artificialmente baixa. Laboratórios ficam fora da régua de 45 dias porque recursam em 46–60.</p>
  </div>
  <div class="panel tbl-wrap">
    <h3>Laboratórios por grupo: % recursado da coorte</h3>
    <table>
      <thead><tr><th>Grupo</th><th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th><th>Ago</th><th>Set*</th><th>Out (parcial)</th></tr></thead>
      <tbody>
        <tr><td>DASA</td><td>56%</td><td>71%</td><td>52%</td><td>55%</td><td>57%</td><td>66%</td><td>0%</td></tr>
        <tr class="hl"><td>Fleury</td><td>30%</td><td>37%</td><td>24%</td><td>22%</td><td><b>59%</b></td><td><b>52%</b></td><td><b>27%</b></td></tr>
        <tr><td>Femme</td><td>100%</td><td>100%</td><td>88%</td><td>70%</td><td>86%</td><td>0%</td><td>0%</td></tr>
      </tbody>
    </table>
  </div>
  <div class="panel">
    <p><b>Sua leitura se confirma no total e em hospitais.</b> Nas coortes maduras, o % recursado fica em 64–65% em abr, mai e ago. Setembro está em 58% (55% sem 7F6) e deve terminar entre 60% e 63% quando o Femme e o restante chegarem. Ou seja, estável ou levemente menor. Em hospitais, a tendência é de leve queda: 87% e 69% em abr–mai, 69% em ago e 62% em set.</p>
    <p><b>Em laboratórios, a exceção é o Fleury.</b> O grupo passou de recursar 22–37% da glosa (abr–jul) para 52–59% (ago–set). DASA e Femme seguem no padrão. Em laboratórios sem 7F6, setembro está em 44%, abaixo de agosto.</p>
  </div>
</section>

<section>
  <h2>6. Há desvio?</h2>
  <div class="panel">
    <ol class="steps">
      <li><b>Fleury: mudou o comportamento.</b> Passou a recursar mais (52–59% da glosa, contra 22–37%) e mais rápido. A glosa de outubro está chegando com mediana de 22 dias, quando antes chegava com 45–60. Em novembro, ele mandou duas coortes ao mesmo tempo: R$ 455 mil de setembro e R$ 182 mil de outubro, total de R$ 638 mil. É o único desvio real. Parte do aumento de laboratórios é antecipação, não volume novo.</li>
      <li><b>DASA, 7F6: esperado.</b> A glosa de 7F6 dobrou de novo em outubro (R$ 595 mil) e segue alta em novembro (R$ 425 mil em 17 dias). O recurso acompanha.</li>
      <li><b>HCor: atraso recorrente.</b> Recursa com mais de 60 dias (82 dias na glosa de agosto) e tem R$ 646 mil de glosa em novembro, que deve virar recurso em janeiro.</li>
      <li><b>Hospitais: queda coerente.</b> A glosa de outubro foi a menor do ano (2,3% do apresentado), com o 7F8 caindo de R$ 935 mil para R$ 364 mil.</li>
    </ol>
  </div>
  <p class="small muted">Relatórios relacionados: <a href="https://claude.ai/artifact/YcSrkgMkt79RWSpu5G56j6" target="_blank" rel="noopener">Laboratórios, até 11/11</a> · <a href="https://claude.ai/artifact/MUhd7cHLZUAcVqrXjbUwqh" target="_blank" rel="noopener">Hospitais, até 11/11</a>. Fonte: <code>curated.totvs_procedure_invoice</code>, atualizada até 17/11. Não é tempo real.</p>
</section>
"""
open('indicador-recurso-novembro.html','w').write(page("Indicador Recurso Novembro", body, ""))
