import scrapy
from scrapy.selector import Selector
import json

class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["www.centris.ca"]
    # start_urls = ["https://www.centris.ca/en"]

    position = {
        'startPosition': 0
    }

    def start_requests(self):
        query = {
            "query": {
                "UseGeographyShapes": 0,
                "Filters": [

                ],
                "FieldsValues": [
                    {
                        "fieldId": "PropertyType",
                        "value": "SingleFamilyHome",
                        "fieldConditionId": "",
                        "valueConditionId": "IsResidential"
                    },
                    {
                        "fieldId": "Pool",
                        "value": "Pool",
                        "fieldConditionId": "IsResidentialNotLot",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "Category",
                        "value": "Residential",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "SellingType",
                        "value": "Rent",
                        "fieldConditionId": "",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "LandArea",
                        "value": "SquareFeet",
                        "fieldConditionId": "IsLandArea",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 0,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    },
                    {
                        "fieldId": "RentPrice",
                        "value": 3000,
                        "fieldConditionId": "ForRent",
                        "valueConditionId": ""
                    }
                ]
            },
            "isHomePage": True
        }

        yield scrapy.Request(
            url="https://www.centris.ca/property/UpdateQuery",
            method="POST",
            body=json.dumps(query),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.update_query
        )

    def update_query(self, response):
        yield scrapy.Request(
            url="https://www.centris.ca/Property/GetInscriptions",
            method="POST",
            body=json.dumps(self.position),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')

        with open("index.html", "w") as f:
            f.write(html)
