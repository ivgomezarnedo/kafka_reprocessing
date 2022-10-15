import kafka_utils as kafka
import db_utils

rows = db_utils.select_from_sqlite("SELECT * FROM matches_odds", one=False)

for row in rows:
    print(dict(row))
    kafka.producer.send('odds_topic', value={'data': dict(row)})