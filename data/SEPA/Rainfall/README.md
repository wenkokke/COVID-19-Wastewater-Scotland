This directory contains rainfail data, as published by the Scottish Environment Protection Agency at:
https://www2.sepa.org.uk/rainfall

The data is obtained by a REST API.
The script `get_data.py` downloads the most recent year of daily averages.

The precipitation data is provided in milimeters. I've sent a request for clarification to SEPA, but I assume this is milimeters of precipitation per square meter surface.
