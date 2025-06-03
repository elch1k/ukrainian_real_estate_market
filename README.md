# Analytical and machine learning-based price forecasting of the flat real estate market
**Preface:** This project is an upgraded version of my previous work, which related to the [analysis and ML prediction of rental prices for flats in Kharkiv city](https://github.com/elch1k/kharkiv_real_estate_rent_market). This initiative focuses on researching both rental and sales flat prices across all of Ukraine's main administrative regions. It involves [detailed analysis](https://github.com/elch1k/ukrainian_real_estate_market/blob/main/eda_and_ml/lun_real_estate_eda.ipynb) and [machine learning modeling for sales flat prices](https://github.com/elch1k/ukrainian_real_estate_market/blob/main/eda_and_ml/lun_real_estate_ml.ipynb), along with developing a data collection pipeline from the trusted source: [**Rieltor.ua**](https://rieltor.ua/).

You're welcome to use the project's data parser (located in main.py) for your own research and ML modeling. The collected data can be stored in a flat file format or your relational database.

Analytical part
--
This section focuses on data preprocessing and outlier handling for both sales and rental transactions. Following this, a detailed structural analysis of the flat real estate market is presented for both sales and rental deal types. For the full report, please visit the notebook with this [link](https://github.com/elch1k/ukrainian_real_estate_market/blob/main/eda_and_ml/lun_real_estate_eda.ipynb).
As a brief summary, this report presents all available units within the flat real estate market, broken down by city and their respective distribution by deal type. The plot below visualizes this information.
![flat_real_estate_units](https://github.com/elch1k/ukrainian_real_estate_market/blob/main/images/img_2.png)

This research also indicates that real estate sales market valuations are consistently estimated in U.S. dollars. In contrast, the rental market frequently uses the national currency for flat real estate valuations, likely reflecting the short-term duration of such deals.
![currency_distribution](https://github.com/elch1k/ukrainian_real_estate_market/blob/main/images/img_1.png)

A more crucial aspect of this research involves analyzing price distributions for both rental and sales transactions by city. This detailed examination of pricing provides a deeper understanding of the Ukrainian market structure and valuable insights.
<p align="center">
  <img src="https://github.com/elch1k/ukrainian_real_estate_market/blob/main/images/img_3.png" width="420"/>
  <img src="https://github.com/elch1k/ukrainian_real_estate_market/blob/main/images/img_4.png" width="420"/>
</p>

