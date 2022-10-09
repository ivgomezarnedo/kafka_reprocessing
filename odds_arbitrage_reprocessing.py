from kafka import KafkaConsumer
from json import loads
from kafka.structs import (
    TopicPartition
)
from odds_data_classes import Odd, Match_odd

consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

topic = TopicPartition('odds_topic', 0)  # Topic-partition pair
new_pos = 3000  # New position (offset)
consumer.assign([topic])
consumer.seek_to_beginning()  # Start at the beginning of the topic
consumer.seek(topic, new_pos) # Set the new position

arbitrage_status = {}
for event in consumer:
    match_id = event.value['data']['ID']
    betting_office = event.value['data']['Betting_Office']
    odd_victory = event.value['data']['Odds_Victory']
    odd_lose = event.value['data']['Odds_Lose']
    if match_id in arbitrage_status:
        current = arbitrage_status[match_id]
        if odd_victory > (current.odd_win.odd+0.1):  # 0.1 is the new arbitrage margin
            print(f"NEW: {odd_victory}. CURRENT: {current.odd_win.odd}")
            odd_win = Odd(betting_office=betting_office, odd=odd_victory )
            current.odd_win = odd_win
            print("NEW MAX ODD WIN. ARBITRAGE OPPORTUNITY")
            print(current)
            print("------------------------------------")

    else:
        odd_win = Odd(betting_office=betting_office, odd=odd_victory )
        odd_lose = Odd(betting_office=betting_office, odd=odd_lose )
        match_odd = Match_odd(odd_win=odd_win, odd_lose=odd_lose)
        arbitrage_status[match_id] = match_odd