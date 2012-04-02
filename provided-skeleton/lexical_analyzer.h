// PL homework: calculator
// lexical_ananlyzer.h

#ifndef _PL_HOMEWORK_LEXICAL_ANALYZER_H_
#define _PL_HOMEWORK_LEXICAL_ANALYZER_H_

#include <map>
#include <string>

enum Token {
  ERROR = -1,
  EOS = 0,  // End-Of-String.
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
  std::string token_string_;  // Detected string for the current token.
};

#endif //_PL_HOMEWORK_LEXICAL_ANALYZER_H_
