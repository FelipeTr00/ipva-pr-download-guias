# IPVA/PR 2025 - Download Automatizado de Guias (v2)

<p align="center">
  <h3 align="center">IPVA/PR - Versão 2.0</h3>

  <p align="center">
    Um script Python para automatizar o download das guias de IPVA/PR em 2025.
    <br/>
    Esta versão é baseada no projeto original criado por <a href="https://github.com/lfeabreu/">Luís Filipe de Abreu</a>.
    <br/>
    <a href="https://github.com/FelipeTr00/ipva-pr-download-guias/issues">Reportar um Bug</a>
    .
  </p>
</p>

---

## Sobre o Projeto

Este projeto é continuação do trabalho iniciado por <a href="https://github.com/lfeabreu">Luís Filipe de Abreu</a>, que desenvolveu uma excelente solução automatizada para baixar guias de IPVA. Sendo extremamente importante para a execusão da tarefa de baixar mais de 2100 guias de IPVA. Do qual deixo meu total agradecimento por disponibilizar esse código.

Com este script, é possível automatizar o download das guias de IPVA de vários veículos, economizando tempo e reduzindo a possibilidade de erros manuais.

### Considerações da Versão 2.0:
- Suporte para configurações via arquivo `config.json`.
- Sem necessidade de automatizar a resolução de Captchas
---

## Configuração do `config.json`

Antes de rodar o script, configure o arquivo `config.json`. Este arquivo é utilizado para centralizar todas as informações necessárias para a execução do projeto.

### Exemplo de `config.json`:
```json
{
  "url_base": "https://www.contribuinte.fazenda.pr.gov.br/ipva/faces",
  "file_path": <pasta_arquivo_excel>,
  "sheet": "Dados",
  "download_folder": <pasta_downloads>,

  "element_ids": {
    "renavam_input": "pt1:r1:0:r2:0:ig1:it1::content",
    "consultar_button": "pt1:r1:0:r2:0:ig1:b11",
    "download_button": "pt1:r1:0:tbCu:0:lnkCu"
  }
}
```
### Descrição dos Campos:

- **`url_base`**: URL da página inicial do site para acesso.
- **`file_path`**: Caminho do arquivo Excel contendo os dados dos veículos.
- **`sheet`**: Nome da aba do Excel que contém os dados.
- **`download_folder`**: Diretório onde os arquivos baixados serão salvos.
- **`element_ids`**:
  - **`renavam_input`**: ID do campo de entrada para o Renavam.
  - **`consultar_button`**: ID do botão para iniciar a consulta.
  - **`download_button`**: ID do botão para baixar as guias.
---

### Instalar Dependencias:
```
pip install -r requirements.txt
```
---
### Rodar/Run:

```
py main.py
```
---
### Licença

### Distribuído sob a ["MIT License"](/LICENSE.txt).

---

### Enjoy 🎵

### Joe Bonamassa - "Taxman" - Live at The Cavern Club<br>
### https://www.youtube.com/watch?v=dgaM43KCqT4

---
