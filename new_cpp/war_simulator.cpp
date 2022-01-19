#include <iostream>

using namespace std;

enum suit_t : char { DIAMONDS, HEARTS, CLUBS, SPADES };

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

int main(int argc, char* argv[]) {
    return EXIT_SUCCESS;
}