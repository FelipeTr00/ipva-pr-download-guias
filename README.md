<br/>
<p align="center">
  <h3 align="center">IPVA/PR - Download automatizado de guias</h3>

  <p align="center">
    Um incrível script Python para download das guias de IPVA/PR.
    <br/>
    <br/>
    <a href="https://github.com/lfeabreu/ipva-pr-download-guias/issues">Reportar um Bug</a>
    .
  </p>
</p>



## Sobre o Projeto

Estes dias me deparei com um problema para nossa área: baixar todas as guias de pagamento dos IPVAs de quase 2.000 veículos.

Infelizmente, não encontrei nenhuma forma "oficial" (fornecidas pelo orgão responsável) de baixar todas estas guias.

Meus colegas de trabalho teriam grande labuta para baixar todas elas manualmente, estando sujeitos ao erro humano (duplicidade ou deixar alguma para trás).

Foi aí que me veio a ideia de criar um "robô" em Python para automatizar esta atividade, ganhar tempo e diminuir falhas humanas.

Então, usando uma API de OCR para passar o CAPTCHA, a biblioteca Selenium e outras bibliotecas no Python, criei este "robozinho". 🤖

O resultado: baixamos todas as guias em 2 dias (isso porque a API demorava um pouco para dar o retorno do OCR e, muitas vezes ainda errava).


## Licença

Distribuído sob a "MIT License". Veja [LICENSE](https://github.com/lfeabreu/ipva-pr-download-guias/blob/main/LICENSE.md) para mais informações.

## Autores

* **Luís Filipe de Abreu** - *Dados | BI | SQL | ETL | Software Developer/Engineer* - [Luís Filipe de Abreu](https://github.com/lfeabreu/)
