This directory contains rainfail data, as published by the Scottish Environment Protection Agency at:
https://www2.sepa.org.uk/rainfall

The data is obtained by a REST API.

```bash
curl https://www2.sepa.org.uk/rainfall/api/stations?csv=true > stations.csv
curl https://www2.sepa.org.uk/rainfall/api/Daily/115618?csv=true&all=true > 115618.csv
```
