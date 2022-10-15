import kafka_utils as kafka
from odds_data_classes import Odd, Match_odd
import sys


def arbitrage_v1(arbitrage_status, producer, odd_victory, odd_lose):
    # Arbitrage v1 is the first version of the arbitrage detection
    current = arbitrage_status[match_id]
    if odd_victory > current.odd_win.odd:
        alert = f"NEW: {odd_victory}. CURRENT: {current.odd_win.odd}\n"
        odd_win = Odd(betting_office=betting_office, odd=odd_victory)
        current.odd_win = odd_win
        alert += "NEW MAX ODD WIN. ARBITRAGE OPPORTUNITY\n"
        alert += current.__repr__()
        print(alert)
        print("------------------------------------")
        producer.send('arbitrage_alerts_v1', value={'alert': alert})
    if odd_lose > current.odd_lose.odd :  # 0.1 is the new arbitrage margin
        alert = f"NEW MAX ODD LOSE. ARBITRAGE OPPORTUNITY\n NEW: {odd_lose}. CURRENT: {current.odd_lose.odd}\n"
        odd_lose = Odd(betting_office=betting_office, odd=odd_lose)
        current.odd_lose = odd_lose
        alert += current.__repr__()
        print(alert)
        print("------------------------------------")
        producer.send('arbitrage_alerts_v1', value={'alert': alert})


def arbitrage_v2(arbitrage_status, producer, odd_victory, odd_lose, offset, timestamp):
    # Arbitrage v2 is the second version of the arbitrage detection (More restrictive finding arbitrage opportunities)
    current = arbitrage_status[match_id]
    if odd_victory > (current.odd_win.odd +1): # 1 is the new arbitrage margin
        alert = f"Offset: {offset}, timestamp: {timestamp }\nNEW MAX ODD WIN. TOP ARBITRAGE OPPORTUNITY\nNEW: {odd_victory}. CURRENT: {current.odd_win.odd}\n"
        odd_win = Odd(betting_office=betting_office, odd=odd_victory)
        current.odd_win = odd_win
        alert += current.__repr__()
        print(alert)
        print("------------------------------------")
        producer.send('arbitrage_alerts_v2', value={'alert': alert})
    if odd_lose > (current.odd_lose.odd +1):  # 1 is the new arbitrage margin
        alert = f"Offset: {offset}, timestamp: {timestamp }\nNEW MAX ODD LOSE. TOP ARBITRAGE OPPORTUNITY\n NEW: {odd_lose}. CURRENT: {current.odd_lose.odd}\n"
        odd_lose = Odd(betting_office=betting_office, odd=odd_lose)
        current.odd_lose = odd_lose
        alert += current.__repr__()
        print(alert)
        print("------------------------------------")
        producer.send('arbitrage_alerts_v2', value={'alert': alert})


if __name__ == "__main__":
    function_to_use = "v1"
    if sys.argv[1:]:
        if sys.argv[1] == "v2":
            function_to_use = "v2"
    print(f"Using {function_to_use} arbitrage detection")
    arbitrage_status = {}
    if function_to_use == "v2":
        kafka.assign_offset_based_on_timestamp(kafka.consumer, 1665822606110)
    for event in kafka.consumer:
        alert = None
        match_id = event.value['data']['ID']
        betting_office = event.value['data']['Betting_Office']
        odd_victory = event.value['data']['Odds_Victory']
        odd_lose = event.value['data']['Odds_Lose']
        offset = event.offset
        timestamp = event.timestamp
        if match_id in arbitrage_status:  # If the match is already in the arbitrage_status dict
            if function_to_use == "v2":
                arbitrage_v2(arbitrage_status, kafka.producer, odd_victory, odd_lose, offset = offset, timestamp = timestamp)
            else:
                arbitrage_v1(arbitrage_status, kafka.producer, odd_victory, odd_lose)
        else:  # First time we see this match
            odd_win = Odd(betting_office=betting_office, odd=odd_victory )
            odd_lose = Odd(betting_office=betting_office, odd=odd_lose )
            match_odd = Match_odd(odd_win=odd_win, odd_lose=odd_lose)
            arbitrage_status[match_id] = match_odd