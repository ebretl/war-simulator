#include <iostream>
#include <vector>
#include <random>
#include <optional>
#include <deque>
#include <algorithm>
#include <map>
#include <iomanip>

using namespace std;

enum suit_t : char { DIAMONDS=0, HEARTS=1, CLUBS=2, SPADES=3 };

ostream& operator<<(ostream& os, suit_t suit) {
    switch (suit) {
        case DIAMONDS:
            os << 'D';
            break;
        case HEARTS:
            os << 'H';
            break;
        case CLUBS:
            os << 'C';
            break;
        case SPADES:
            os << 'S';
            break;
    }
    return os;
}

constexpr char JACK = 11;
constexpr char QUEEN = 12;
constexpr char KING = 13;
constexpr char ACE = 14;

struct Card {
    char value;
    suit_t suit;
};

bool operator<(const Card& lhs, const Card& rhs) {
    return lhs.value < rhs.value;
}

// ostream& operator<<(ostream& os, const Card& card) {
//     switch (card.value) {
//         case 
//     }
// }

class Player final {
 public:
    explicit Player(mt19937& rand_gen, vector<Card>&& cards) 
    : rand_gen_{rand_gen}, draw_{std::move(cards)} {
        draw_.reserve(52);
        discard_.reserve(52);
    }

    size_t n_cards() const {
        return (draw_.size() + discard_.size());
    }

    bool is_alive() const {
        return n_cards() > 0;
    }

    optional<Card> fight() {
        if (draw_.empty()) {
            if (discard_.empty()) {
                return nullopt;
            } else {
                draw_ = discard_;
                discard_.clear();
                shuffle(draw_.begin(), draw_.end(), rand_gen_);
            }
        }

        const auto card = draw_.back();
        draw_.pop_back();
        return card;
    }

    template <typename C>
    void plunder(const C& cards) {
        discard_.insert(discard_.end(), begin(cards), end(cards));
    }

 private:
    mt19937 rand_gen_;
    vector<Card> draw_;
    vector<Card> discard_;
};


enum Winner { WINNER_P1, WINNER_P2, WINNER_TIE };

struct GameResult {
    Winner winner = WINNER_TIE;
    size_t turn_count = 0;
};

// Statistics tracker per turn count
struct TurnStats {
    size_t p1_wins = 0;
    size_t p2_wins = 0;
};

Winner play_turn(Player& p1, Player& p2, deque<Card>& pot) {
    pot.push_front(*p1.fight());
    pot.push_back(*p2.fight());

    const auto& c1 = pot.front();
    const auto& c2 = pot.back();

    if (c1 < c2) {
        p2.plunder(pot);
        return WINNER_P2;
    }
    if (c2 < c1) {
        p1.plunder(pot);
        return WINNER_P1;
    }
    if (!p1.is_alive() && p2.is_alive()) {
        return WINNER_P2;
    }
    if (p1.is_alive() && !p2.is_alive()) {
        return WINNER_P1;
    }

    // war
    for (int ii = 0; ii < 3; ++ii) {
        if (p1.n_cards() > 1) {
            pot.push_front(*p1.fight());
        }
        if (p2.n_cards() > 1) {
            pot.push_back(*p2.fight());
        }
    }
    return play_turn(p1, p2, pot);
}

GameResult play_game(vector<Card>& deck, mt19937& rand_gen) {
    shuffle(deck.begin(), deck.end(), rand_gen);

    Player p1{rand_gen, vector<Card>{deck.begin(), deck.begin() + deck.size()/2}};
    Player p2{rand_gen, vector<Card>{deck.begin() + deck.size()/2, deck.end()}};

    GameResult result;
    deque<Card> pot;
    while (p1.is_alive() && p2.is_alive()) {
        ++result.turn_count;
        pot.clear();

        result.winner = play_turn(p1, p2, pot);
    }
    return result;
}


int main(int argc, char* argv[]) {
    vector<Card> deck;
    deck.reserve(52);
    for (char suit = 0; suit < 4; ++suit) {
        for (char value = 2; value <= 14; ++value) {
            deck.push_back(Card{value, static_cast<suit_t>(suit)});
        }
    }

    mt19937 rand_gen{random_device{}()};

    map<size_t, TurnStats> stats;
    
    size_t num_games = 100;
    if (argc > 1) {
        num_games = stoi(argv[1]);
    }

    for (size_t game_count = 0; game_count < num_games; ++game_count) {
        const auto result = play_game(deck, rand_gen);

        if (!stats.count(result.turn_count)) {
            stats[result.turn_count] = TurnStats{};
        }
        stats[result.turn_count].p1_wins += (result.winner == WINNER_P1);
        stats[result.turn_count].p2_wins += (result.winner == WINNER_P2);
    }

    // Output CSV
    cout << "game_length,p1_wins,p2_wins" << endl;
    for (const auto& [turns, s] : stats) {
        cout << turns << "," << s.p1_wins << "," << s.p2_wins << endl;
    }

    return EXIT_SUCCESS;
}
