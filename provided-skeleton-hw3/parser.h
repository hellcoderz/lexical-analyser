// PL homework: calculator
// parser.h

#ifndef _PL_HOMEWORK_PARSER_H_
#define _PL_HOMEWORK_PARSER_H_

#include <string>
#include "lexical_analyzer.h"

class Parser {
 public:
  Parser();
  ~Parser();

  // ParseInputString performs the syntax analysis and calls the handlers.
  bool ParseInputString(const std::string& input_string);

  // Handlers for the actions. A handler returns false when an error occurs.
  bool OnShift(Token token, const std::string& token_string, int next_state);
  bool OnReduce(int rule, int next_state);
  void OnAccept();
  void OnLexerError();
  void OnParseError();

 private:
  LexicalAnalyzer lexer_;
};

#endif //_PL_HOMEWORK_PARSER_H_
