import scrapy
import re

class HoleritesSpider(scrapy.Spider):
    name = 'holerites'
    allowed_domains = ['cmc.pr.gov.br']
    start_urls = ['https://www.cmc.pr.gov.br/portal-transparencia/holerite/']

    def parse(self, response):
        cargos = response.css('select[name=grupo] option')
        anos = response.css('select[name=mesano] option')

        for ano in reversed(anos):
            anoValue = ano.css('::attr(value)').extract_first()
            for cargo in reversed(cargos):
                cargoValue = cargo.css('::attr(value)').extract_first()

                data = {
                    'mesano': str(anoValue),
                    'grupo': str(cargoValue),
                    'tipo': '1',
                    'acao':'reload'
                }

                # Skip ouvidor, cedido pela camara and temporario
                if str(cargoValue) is '5' or str(cargoValue) is '7' or str(cargoValue) is '8':
                    continue

                yield scrapy.FormRequest.from_response(
                        response,
                        formdata=data,
                        callback=self.parse_cargo_table,
                        meta={'mesano':str(anoValue), 'grupo':str(cargoValue)}
                        )

    def parse_cargo_table(self, response):

        for row in response.css('#beneficiarios tr'):
            if row.css('th').extract_first() is not None:
                continue

            # Vereador
            if response.meta['grupo'] is '1':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                lotacao = row.css('td:nth-child(3)::text').extract_first()
                admissao = row.css('td:nth-child(4)::text').extract_first()
                href = row.css('td:nth-child(5) a::attr(href)').extract_first()
            # Efetivo
            elif response.meta['grupo'] is '2':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                funcao = row.css('td:nth-child(3)::text').extract_first()
                lotacao = row.css('td:nth-child(4)::text').extract_first()
                admissao = row.css('td:nth-child(5)::text').extract_first()
                horario = row.css('td:nth-child(6)::text').extract_first()
                href = row.css('td:nth-child(7) a::attr(href)').extract_first()
            # Comissionado
            elif response.meta['grupo'] is '3':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                lotacao = row.css('td:nth-child(3)::text').extract_first()
                admissao = row.css('td:nth-child(4)::text').extract_first()
                horario = row.css('td:nth-child(5)::text').extract_first()
                href = row.css('td:nth-child(6) a::attr(href)').extract_first()
            # Inativo
            elif response.meta['grupo'] is '4':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                href = row.css('td:nth-child(3) a::attr(href)').extract_first()
            # Ouvidor
            # elif response.meta['grupo'] is '5':
            # Cedido Para Camara
            elif response.meta['grupo'] is '6':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                lotacao = row.css('td:nth-child(3)::text').extract_first()
                origem = row.css('td:nth-child(4)::text').extract_first()
                cargo_origem = row.css('td:nth-child(5)::text').extract_first()
                admissao = row.css('td:nth-child(6)::text').extract_first()
                horario = row.css('td:nth-child(7)::text').extract_first()
                onus = row.css('td:nth-child(8)::text').extract_first()
                href = row.css('td:nth-child(9) a::attr(href)').extract_first()
            # Cedido pela Câmara
            # elif response.meta['grupo'] is '7':
            # Temporário
            # elif response.meta['grupo'] is '8':
            elif response.meta['grupo'] is '9':
                nome = row.css('td:nth-child(1)::text').extract_first()
                cargo = row.css('td:nth-child(2)::text').extract_first()
                lotacao = row.css('td:nth-child(3)::text').extract_first()
                admissao = row.css('td:nth-child(4)::text').extract_first()
                terminoContrato = row.css('td:nth-child(5)::text').extract_first()
                horario = row.css('td:nth-child(6)::text').extract_first()
                href = row.css('td:nth-child(7) a::attr(href)').extract_first()

            entity_id = re.search("pesquisa\((.*)\)", str(href)).group(1)

            meta = {
                'mesano': response.meta['mesano'],
                'grupo': response.meta['grupo'],
                'nome': nome, 
                'cargo': cargo, 
                # 'lotacao': lotacao,
                # 'admissao': admissao,
                'id': entity_id
            }

            data = {
                'hol_ben_id': entity_id,
                'hol_mesano': response.meta['mesano'],
                'hol_grupo': response.meta['grupo'],
                'hol_tipo': '1',
                'hol_observacao': '-nada-',
                'hol_historico': '-nada-',
            }

            yield scrapy.FormRequest(url="https://www.cmc.pr.gov.br/portal-transparencia/holerite/consulta_beneficiario.html",
                    formdata=data,
                    meta=meta,
                    callback=self.parse_consulta_beneficiario)
    
    def parse_consulta_beneficiario(self, response):
        table = response.xpath('//*[@id="holerite"]')

        headers = table.xpath('//tr[@class="holerite_descricao"]/td/text()').extract()
        values = table.xpath('//tr[@class="holerite_valor"]/td/text()').extract()
        
        if len(headers) <= 0:
            return

        item = {}

        for idx, header in enumerate(headers):
            item[header] = values[idx]

        item['mesano'] = response.meta['mesano']
        item['grupo'] = response.meta['grupo']
        item['nome'] = response.meta['nome']
        item['cargo'] = response.meta['cargo']
        item['id'] = response.meta['id']

        yield item

