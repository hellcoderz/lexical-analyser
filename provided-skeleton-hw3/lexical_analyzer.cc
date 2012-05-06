// PL homework: calculator
// lexical_ananlyzer.cc

#include "lexical_analyzer.h"

#include <iostream>
using namespace std;

#ifdef USE_TABLE
#include <map>

const char ALPHA = 1;
const char DIGIT = 2;

struct TableElement {
  int state;
  char input_char;
  int next_state;
};

static TableElement table_elements[] = {
  { 0, ALPHA, 1 },
  { 0, DIGIT, 2 },
  { 0, '.', 3 },
  { 0, '+', 8 },
  { 0, '-', 9 },
  { 0, '*', 10 },
  { 0, '/', 11 },
  { 0, '^', 12 },
  { 0, '=', 13 },
  { 0, '(', 14 },
  { 0, ')', 15 },
  { 1, ALPHA, 1 },
  { 1, DIGIT, 1 },
  { 2, DIGIT, 2 },
  { 2, '.', 4 },
  { 2, 'e', 5 },
  { 2, 'E', 5 },
  { 2, ALPHA, -1 },
  { 3, DIGIT, 4 },
  { 4, DIGIT, 4 },
  { 4, 'e', 5 },
  { 4, 'E', 5 },
  { 4, ALPHA, -1 },
  { 4, '.', -1 },
  { 5, DIGIT, 7 },
  { 5, '+', 6 },
  { 5, '-', 6 },
  { 6, DIGIT, 7 },
  { 7, DIGIT, 7 },
  { 7, ALPHA, -1 },
  { 7, '.', -1 },
};

static Token states[] = {
  ERROR,  // 0
  ID,  // 1
  NUMBER,  // 2
  ERROR,  // 3
  NUMBER,  // 4
  ERROR,  // 5
  ERROR,  // 6
  NUMBER,  // 7
  OP_PLUS,  // 8
  OP_MINUS,  // 9
  OP_MUL,  // 10
  OP_DIV,  // 11
  OP_POW,  // 12
  OP_ASSIGN,  // 13
  OP_LPAREN,  // 14
  OP_RPAREN,  // 15
};
#endif //USE_TABLE

LexicalAnalyzer::LexicalAnalyzer()
    : index_(0) {
#ifdef USE_TABLE
  const int num_elements = sizeof(::table_elements) / sizeof(TableElement);
  for (int i = 0; i < num_elements; ++i) {
    const TableElement& elem = ::table_elements[i];
    table_[make_pair(elem.state, elem.input_char)] = elem.next_state;
  }
  const int num_states = sizeof(::states) / sizeof(Token);
  state_tokens_.reserve(num_states);
  for (int i = 0; i < num_states; ++i) {
    state_tokens_.push_back(::states[i]);
  }
#endif //USE_TABLE
}

LexicalAnalyzer::~LexicalAnalyzer() {
}

void LexicalAnalyzer::SetInputString(const std::string& input_string) {
  str_ = input_string;
  index_ = 0;
}

Token LexicalAnalyzer::Lex() {
  // Skip white spaces.
  while (index_ < str_.length() && IsBlank(str_[index_])) ++index_;
  // Start the Finite State Machine.
  const Token UNKNOWN = EOS;  // Use EOS to mark that the token is not found.
  Token token = UNKNOWN;
  size_t start_index = index_;
  int state = 0;
  while (token == UNKNOWN && index_ <= str_.length()) {
    const char ch = index_ < str_.length() ? str_[index_] : 0;
#ifdef USE_TABLE
    Table::const_iterator it = table_.find(make_pair(state, ch));
    if (it == table_.end()) {
      if (IsAlpha(ch)) it = table_.find(make_pair(state, ALPHA));
      if (IsDigit(ch)) it = table_.find(make_pair(state, DIGIT));
    }
    if (it == table_.end()) {
      token = state_tokens_[state];
    } else if (it->second < 0) {  // Errorneous transition.
      token = ERROR;
    } else {
      state = it->second;
    }
#else //USE_TABLE
    switch (state) {
      case 0:
        if (IsAlpha(ch)) state = 1;
        else if (IsDigit(ch)) state = 2;
        else if (ch == '.') state = 3;
        else if (ch == '+') ++index_, token = OP_PLUS;
        else if (ch == '-') ++index_, token = OP_MINUS;
        else if (ch == '*') ++index_, token = OP_MUL;
        else if (ch == '/') ++index_, token = OP_DIV;
        else if (ch == '^') ++index_, token = OP_POW;
        else if (ch == '=') ++index_, token = OP_ASSIGN;
        else if (ch == '(') ++index_, token = OP_LPAREN;
        else if (ch == ')') ++index_, token = OP_RPAREN;
        else token = ERROR;
        break;
      case 1:
        if (IsAlpha(ch) || IsDigit(ch)) state = 1;
        else token = ID;
        break;
      case 2:
        if (IsDigit(ch)) state = 2;
        else if (ch == '.') state = 4;
        else if (ch == 'e' || ch == 'E') state = 5;
        else if (IsAlpha(ch)) token = ERROR;
        else token = NUMBER;
        break;
      case 3:
        if (IsDigit(ch)) state = 4;
        else token = ERROR;
        break;
      case 4:
        if (IsDigit(ch)) state = 4;
        else if (ch == 'e' || ch == 'E') state = 5;
        else if (IsAlpha(ch) || ch == '.') token = ERROR;
        else token = NUMBER;
        break;
      case 5:
        if (IsDigit(ch)) state = 7;
        else if (ch == '+' || ch == '-') state = 6;
        else token = ERROR;
        break;
      case 6:
        if (IsDigit(ch)) state = 7;
        else token = ERROR;
        break;
      case 7:
        if (IsDigit(ch)) state = 7;
        else if (IsAlpha(ch) || ch == '.') token = ERROR;
        else token = NUMBER;
        break;
      default:  // This should never happen.
        token = ERROR;
    }
#endif //USE_TABLE
    if (token == UNKNOWN) ++index_;
  }
  token_string_ = (start_index >= str_.length())? "" :
    token_string_ = str_.substr(start_index, index_ - start_index);

  if (start_index >= str_.length()) token = EOS;
  else if (token_string_ == "exit") token = CMD_EXIT;
  else if (token_string_ == "quit") token = CMD_EXIT;
  else if (token_string_ == "list") token = CMD_LIST;
  else if (token_string_ == "clear") token = CMD_CLEAR;
  return token;
}

