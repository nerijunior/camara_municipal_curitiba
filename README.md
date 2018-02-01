<center>
    <img src="https://cmc-transparencia.herokuapp.com/static/og-image.png" >
</center>

# CMC Transparência

Project to transform the data of "Portal da Transparência" of Câmara Munipal de Curitiba into a user-friendly and anonymously data.

This project was made with `python3` and `scrapy`.

## Dependencies

`pip install Scrapy`

## EntityTypes `grupo`

    [
        { id: 1, name: 'Vereadores' },
        { id: 2, name: 'Efetivos' },
        { id: 3, name: 'Comissionados' },
        { id: 4, name: 'Inativos' },
        { id: 5, name: 'Ouvidor' },
        { id: 6, name: 'Cedido para a Câmara' },
        { id: 7, name: 'Cedido pela Câmara' },
        { id: 8, name: 'Temporário' },
        { id: 9, name: 'Estagiário' },
    ]

## Running the project

The results will be imported to MongoDB so you need to setup the MongoDB uri:

    scrapy runspider camara_municipal_curitiba/spiders/holerites.py

The data will be exported to `raw_data` collection at mongodb and use `raw_data_prepare.py` to split the data or you can choose to use the already preparated json files inside the `data` directory.

#### Help Brazil Open Data!
