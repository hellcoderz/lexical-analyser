// PL homework: calculator
// lexical_ananlyzer.h

#ifndef _PL_HOMEWORK_LEXICAL_ANALYZER_H_
#define _PL_HOMEWORK_LEXICAL_ANALYZER_H_

#include <map>
#include <string>
#include <vector>

enum Token {
  ERROR = -1,
  EOS = 0,  // End-Of-String.
  ID = 1, NUMBER = 2,
  OP_PLUS = 10, OP_MINUS = 11, OP_MUL = 12, OP_DIV = 13, OP_POW = 14,
  OP_ASSIGN = 15, OP_LPAREN = 16, OP_RPAREN = 17,
  CMD_EXIT = 20, CMD_LIST = 21, CMD_CLEAR = 22,
};

class LexicalAnalyzer {
 public:
  LexicalAnalyzer();
  ~LexicalAnalyzer();

  // SetInputString sets the input string for lexical analysis.
  void SetInputString(const std::string& input_string);

  // Lex function returns the next token from the input string.
  // The detected token string is stored until the next Lex is called.
  Token Lex();

  // GetTokenString returns the character string for the detected token.
  const std::string& GetTokenString() const { return token_string_; }

 private:
  static bool IsBlank(char c) { return c == ' ' || c == '\t' || c == '\n'; }
  static bool IsAlpha(char c) { return ('A' <= c && c <= 'Z') ||
                                       ('a' <= c && c <= 'z') || c == '_'; }
  static bool IsDigit(char c) { return ('0' <= c && c <= '9'); }

  std::string token_string_;  // Detected string for the current token.

  std::string str_;
  size_t index_;

#ifdef USE_TABLE
  typedef std::map<std::pair<int, char>, int> Table;
  Table table_;
  std::vector<Token> state_tokens_;
#endif //USE_TABLE
};

#endif //_PL_HOMEWORK_LEXICAL_ANALYZER_H_
