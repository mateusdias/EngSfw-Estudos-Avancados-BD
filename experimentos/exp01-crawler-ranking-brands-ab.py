"""
Experimento 01 - Crawler com Scrapy (Ranking The Brands)

Objetivo:
- Coletar marcas iniciadas pelas letras A e B no site rankingthebrands.com.

Como executar (exemplo):
1) Instalar Scrapy:
   pip install scrapy
2) Rodar a spider como script avulso:
   scrapy runspider experimentos/exp01-crawler-ranking-brands-ab.py -O experimentos/marcas_ab.json
"""

from urllib.parse import parse_qs, urlparse

import scrapy


class RankingBrandsABSpider(scrapy.Spider):
    name = "ranking_brands_ab"
    allowed_domains = ["rankingthebrands.com"]
    start_urls = [
        "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=A",
        "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=B",
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        # Descobre a letra filtrada (A ou B) a partir da URL.
        letter = parse_qs(urlparse(response.url).query).get("nameFilter", ["?"])[0]

        # Captura links de marcas no formato Brand-detail.aspx?brandID=...
        brand_links = response.xpath("//a[contains(@href, 'Brand-detail.aspx?brandID=')]")

        for link in brand_links:
            brand_name = link.xpath("normalize-space(.)").get()
            brand_href = link.xpath("@href").get()

            if not brand_name or not brand_href:
                continue

            yield {
                "letter": letter,
                "brand_name": brand_name,
                "brand_url": response.urljoin(brand_href),
                "source_url": response.url,
            }
