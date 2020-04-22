import random

from models import Rank, Suit, Card
from models import StraightFlush, FourOfAKind, FullHouse
from models import Flush, Straight, ThreeOfAKind, TwoPair
from models import Pair, HighCard


HAND_SIZE = 2
BOARD_SIZE = 5
NUM_CARDS_IN_FLUSH = 5
NUM_CARDS_IN_STRAIGHT = 5
NUM_CARDS_IN_FINAL_HAND = 5


def generate_deck():
    for rank in Rank:
        for suit in Suit:
            yield Card(rank, suit)


def deal_x_cards(deck, x):
    for _ in range(x):
        yield deck.pop()


def deal_hand(deck):
    return list(deal_x_cards(deck, HAND_SIZE))


def deal_board(deck):
    return list(deal_x_cards(deck, BOARD_SIZE))


def find_straights(cards):
    enriched_cards = _ace_enrich_for_straight_search(cards)
    straight_rank_ordering = [Rank.Ace] + [rank for rank in Rank]

    sequential_card_count = 0
    current_rank_index = 0

    for card in enriched_cards:
        if card.rank != straight_rank_ordering[current_rank_index]:
            sequential_card_count = 0
            while current_rank_index < len(straight_rank_ordering) and card.rank != straight_rank_ordering[current_rank_index]:
                current_rank_index += 1
        
        sequential_card_count += 1
        if sequential_card_count >= NUM_CARDS_IN_STRAIGHT:
            yield Straight(cards, straight_rank_ordering[current_rank_index])

        current_rank_index += 1

        if current_rank_index >= len(straight_rank_ordering):
            break


def _ace_enrich_for_straight_search(cards):
    if any(card.rank == Rank.Ace for card in cards):
        return [Card(Rank.Ace, None)] + cards
    return cards


def find_x_highest_card_sets(card_sets, x):
    num_card_sets = len(card_sets)
    
    if x > num_card_sets:
        raise Exception(f'Cannot find top {x} card sets from only {num_card_sets} card sets!')
    
    return sorted(card_sets, key=lambda cards: [card.rank.value for card in cards])[-1:-(x+1):-1]


def find_highest_card_set(card_sets):
    return find_x_highest_card_sets(card_sets, 1)[0]


def find_highest_flush(cards):
    cards_by_suit = { suit: [] for suit in Suit }

    for card in cards:
        cards_by_suit[card.suit].append(card)

    flush_sets = [ cards for cards in cards_by_suit.values() if len(cards) >= NUM_CARDS_IN_FLUSH ]

    if not flush_sets:
        return None

    highest_flush_set = find_highest_card_set(flush_sets)
    highest_flush = highest_flush_set[-NUM_CARDS_IN_FLUSH:]
    highest_flush_suit = highest_flush[0].suit

    return Flush(highest_flush, highest_flush_suit)


def build_rank_histogram(cards):
    rank_histogram = { rank: [] for rank in Rank }

    for card in cards:
        rank_histogram[card.rank].append(card)

    return rank_histogram


def find_straight_flush(straights):
    straight_flush_search_results = [find_highest_flush(straight.cards) for straight in straights]
    straight_flushes = [result for result in straight_flush_search_results if result]

    if not straight_flushes:
        return None
    
    straight_flush = find_highest_card_set([sf.cards for sf in straight_flushes])
    high_card = straight_flush[-1]
    return StraightFlush(straight_flush, high_card.suit, high_card)


def pick_top_x_other_than(cards_by_rank, x, *ranks_to_skip):
    reverse_sorted_filtered_cards = [card for rank, rank_set in cards_by_rank.items() for card in rank_set if rank not in ranks_to_skip]

    card_count_remaining = len(reverse_sorted_filtered_cards)

    if x > card_count_remaining:
        raise Exception(f'Cannot pick top {x} from card set with only {card_count_remaining} cards left!')

    return reverse_sorted_filtered_cards[-1:-(x+1):-1]


def find_x_of_a_kind(cards_by_rank, x):
    matching_sets = [cards for cards in cards_by_rank.values() if len(cards) == x]

    if not matching_sets:
        return None

    matching_set = find_highest_card_set(matching_sets)
    matching_set_rank = matching_set[0].rank

    num_kickers = NUM_CARDS_IN_FINAL_HAND - x
    kickers = pick_top_x_other_than(cards_by_rank, num_kickers, matching_set_rank)

    return matching_set, kickers


def find_full_house(cards_by_rank):
    threesomes = [cards for cards in cards_by_rank.values() if len(cards) == 3]

    if not threesomes:
        return None

    threesome = find_highest_card_set(threesomes)
    threesome_rank = threesome[0].rank

    other_two_plus_sets = [cards for rank, cards in cards_by_rank.items() if len(cards) >= 2 and rank != threesome_rank]

    if not other_two_plus_sets:
        return None

    twosome = find_highest_card_set(other_two_plus_sets)[:2]
    twosome_rank = twosome[0].rank

    return FullHouse(threesome + twosome, threesome_rank, twosome_rank)


def find_four_of_a_kind(cards_by_rank):
    result = find_x_of_a_kind(cards_by_rank, 4)
    
    if not result:
        return None

    (foursome, (kicker,)) = result
    return FourOfAKind(foursome + [kicker], foursome[0].rank, kicker)


def find_three_of_a_kind(cards_by_rank):
    result = find_x_of_a_kind(cards_by_rank, 3)
    
    if not result:
        return None

    (threesome, kickers) = result
    return ThreeOfAKind(threesome + kickers, threesome[0].rank, *kickers)


def find_pair(cards_by_rank):
    result = find_x_of_a_kind(cards_by_rank, 2)
    
    if not result:
        return None

    (twosome, kickers) = result
    return Pair(twosome + kickers, twosome[0].rank, *kickers)


def find_two_pair(cards_by_rank):
    twosomes = [cards for cards in cards_by_rank.values() if len(cards) == 2]

    if len(twosomes) < 2:
        return None

    two_highest_twosomes = find_x_highest_card_sets(twosomes, 2)
    highest_twosome_ranks = [twosome[0].rank for twosome in two_highest_twosomes]

    highest_twosome = two_highest_twosomes[0]
    second_twosome = two_highest_twosomes[1]

    highest_twosome_rank = highest_twosome[0].rank
    second_twosome_rank = second_twosome[0].rank

    kicker = pick_top_x_other_than(cards_by_rank, 1, *highest_twosome_ranks)

    final_hand = highest_twosome + second_twosome + [kicker]

    return TwoPair(final_hand, highest_twosome_rank, second_twosome_rank, kicker)


def evaluate_card_set(cards):
    sorted_cards = sorted(cards, key=lambda card: card.rank.value)

    straights = list(find_straights(sorted_cards))
    
    straight_flush = find_straight_flush(straights)
    if straight_flush:
        return straight_flush

    cards_by_rank = build_rank_histogram(sorted_cards)

    four_of_a_kind = find_four_of_a_kind(cards_by_rank)
    if four_of_a_kind:
        return four_of_a_kind

    full_house = find_full_house(cards_by_rank)
    if full_house:
        return full_house

    flush = find_highest_flush(cards)
    if flush:
        return flush

    if straights:
        return straights[-1]

    three_of_a_kind = find_three_of_a_kind(cards_by_rank)
    if three_of_a_kind:
        return three_of_a_kind

    two_pair = find_two_pair(cards_by_rank)
    if two_pair:
        return two_pair

    pair = find_pair(cards_by_rank)
    if pair:
        return pair

    return HighCard(cards)


def determine_winner(cards_by_player_index, board):
    evaluated_hands_by_player_index = {i: evaluate_card_set(board + hand) for (i, hand) in cards_by_player_index.items()}
    (winning_player_index, winning_hand) = max(evaluated_hands_by_player_index.items(), key=lambda item: item[1])
    return winning_player_index, winning_hand


def main():
    deck = list(generate_deck())
    random.shuffle(deck)
    
    player_count = 4
    cards_by_player_index = { i: deal_hand(deck) for i in range(player_count) }
    board = deal_board(deck)

    (winning_player_index, winning_hand) = determine_winner(cards_by_player_index, board)

    print(f'Player {winning_player_index} wins with a {winning_hand}')


if __name__ == "__main__":
    main()