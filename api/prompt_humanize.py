instruction_human="""Ditt jobb är att svara på en indatafråga på svenska och använda en datatabell som information för att besvara frågan. Du får en tabell i HTML-format och en fråga som tabelldata kommer att svara på. Använd inmatningsfrågan och tabellen som en referens och svara på frågan med relevanta data från tabellen.
"""

examples_human="""
Input: vad är maxfakturan som skickas ut till H&M?
Table: <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>max</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2856.0</td>
    </tr>
  </tbody>
</table>
Output: Den maximala fakturan som skickas ut till H&M är: 2856.0 SEK

Input: Hur stor vinst gjordes i December 2023 för Lidl?
Table: <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>vinst för Lidl</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
Output: För kunden Lidl i december 2023 blev vinsten 3 SEK
"""
