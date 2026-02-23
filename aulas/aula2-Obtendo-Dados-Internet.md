# Aula 2 - Obtendo Dados da Internet com Crawler e Scrapy

## Objetivo

Entender como funciona a obtenção de dados da web com crawler e implementar um exemplo real com Scrapy para coletar marcas iniciadas pelas letras A e B.

## 1) O que é obtenção de dados com crawler

Um **crawler** (ou web crawler) é um programa que navega automaticamente por páginas web, identifica conteúdos de interesse e extrai dados de forma estruturada.

Em termos práticos, um crawler:

1. recebe uma ou mais URLs iniciais;
2. baixa o HTML das páginas;
3. identifica os elementos desejados (links, títulos, tabelas, etc.);
4. transforma esses dados em registros (JSON, CSV, banco de dados);
5. opcionalmente segue novos links para continuar a coleta.

## 2) Por que usar Scrapy

O **Scrapy** é um framework Python para crawling e scraping que já oferece:

- sistema de requisições assíncronas;
- parser com seletores CSS/XPath;
- controle de concorrência e atraso entre requisições;
- exportação nativa para JSON/CSV;
- estrutura profissional para escalar spiders.

## 3) Estrutura mínima de uma spider Scrapy

Uma spider normalmente define:

- `name`: identificador da spider;
- `allowed_domains`: domínio permitido;
- `start_urls`: URLs iniciais;
- `parse(response)`: função que extrai os dados da página.

## 4) Exemplo prático: marcas A e B no rankingthebrands.com

### URLs de interesse

- Letra A: `https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=A`
- Letra B: `https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=B`

### Spider completa (`ranking_brands_ab.py`)

```python
import scrapy
from urllib.parse import parse_qs, urlparse


class RankingBrandsABSpider(scrapy.Spider):
    name = "ranking_brands_ab"
    allowed_domains = ["rankingthebrands.com"]
    start_urls = [
        "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=A",
        "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=B",
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "ROBOTSTXT_OBEY": True,
    }

    def parse(self, response):
        # Captura a letra (A ou B) diretamente da query string da URL
        qs = parse_qs(urlparse(response.url).query)
        letter = qs.get("nameFilter", ["?"])[0]

        # Cada marca aponta para algo como /Brand-detail.aspx?brandID=XXXX
        brand_links = response.xpath("//a[contains(@href, 'Brand-detail.aspx?brandID=')]")

        for link in brand_links:
            brand_name = link.xpath("normalize-space(.)").get()
            brand_url = response.urljoin(link.xpath("@href").get())

            if brand_name:
                yield {
                    "letter": letter,
                    "brand_name": brand_name,
                    "brand_url": brand_url,
                    "source_url": response.url,
                }
```

## 5) Como executar

Dentro de um projeto Scrapy:

```bash
scrapy crawl ranking_brands_ab -O marcas_ab.json
```

Ou em JSON Lines:

```bash
scrapy crawl ranking_brands_ab -O marcas_ab.jsonl
```

## 6) Exemplo de saída esperada

```json
[
  {
    "letter": "A",
    "brand_name": "A Brand New Day",
    "brand_url": "https://www.rankingthebrands.com/Brand-detail.aspx?brandID=6524",
    "source_url": "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=A"
  },
  {
    "letter": "B",
    "brand_name": "Bacardi",
    "brand_url": "https://www.rankingthebrands.com/Brand-detail.aspx?brandID=...",
    "source_url": "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=B"
  }
]
```

## 7) Boas práticas

- respeitar `robots.txt` e termos de uso do site;
- limitar taxa de requisições (`DOWNLOAD_DELAY`);
- registrar logs e tratar erros de rede;
- versionar o código da spider e documentar o formato de saída.
