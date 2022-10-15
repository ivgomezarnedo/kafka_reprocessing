# Kafka reprocessing
This repository contains all the resources used on the [article](https://medium.com/@ivangomezarnedo) 
in which we have discussed how to reprocess data from a Kafka topic. 

In this article we have seen different use cases for an event-driven architecture, 
we have reviewed the different architectures we could implement,
and we have seen, in detail, why we might need to reprocess old events
as well as a detailed example where we reprocess events 
due to a change in our odds-arbitrage algorithm.

## Resources provided
- `kafka_reprocessing` folder: contains the code for the Kafka reprocessing example
- `kafka_reprocessing/db/matches_odds`: A SQLite DB with real (anonymized) data extracted from different betting offices. This data will be used during the example to simulate a real scenario.
- `kafka_reprocessing/docker/docker-compose.yml`: A docker-compose file to start Kafka.

## Prerequisites
- Clone the repo and navigate to the `kafka_reprocessing` folder
- install [docker-compose](https://docs.docker.com/compose/install/) 
- install Python 3.7 or higher
- install [kafka-python](https://kafka-python.readthedocs.io/en/master/) library: `pip install kafka-python`


## Running the example
- run `docker-compose -f docker-compose.yml up` to start the Kafka cluster and the listener
- run `python odds_producer.py` to start the producer
- run `python odds_arbitrage.py` to start the consumer that will use v1 of the arbitrage function
- run `python odds_arbitrage.py "v2"` to start the consumer that will use v2 of the arbitrage function, reading from a certain timestamp.


## Notes
- More information about the Kafka docker used can be found in the [official repo](https://github.com/wurstmeister/kafka-docker)
- More information about Kafka listeners and why do [we need them in a Kafka docker installation](https://www.confluent.io/blog/kafka-listeners-explained/) 
