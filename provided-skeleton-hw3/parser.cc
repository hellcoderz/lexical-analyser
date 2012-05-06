// PL homework: calculator
// parser.cc

#include <iostream>
#include "parser.h"

using namespace std;

Parser::Parser() {
  // Load the parsing table in the constructor.
}

Parser::~Parser() {
}

bool Parser::ParseInputString(const std::string& input_string) {
  lexer_.SetInputString(input_string);
  // Make this function do the parsing.
  // The placeholder below just calls OnShift for all tokens then OnAccept.
  Token token = ERROR;
  do {
    token = lexer_.Lex();
    if (token == ERROR) {
      OnLexerError();
    } else {
      OnShift(token, lexer_.GetTokenString(), 0);
    }
  } while (token != ERROR && token != EOS);
  if (token != ERROR) {
    OnAccept();
  }
  return (token == EOS);
}

// Do not change the handlers for this homework.

bool Parser::OnShift(Token token, const string& token_string, int next_state) {
  cout << " S" << next_state << "[" << token << ":" << token_string << "]";
  return true;
}

bool Parser::OnReduce(int rule, int next_state) {
  cout << " R" << rule << "," << next_state;
  return true;
}

void Parser::OnAccept() {
  cout << " **" << endl;
}

void Parser::OnParseError() {
  cout << " ParseError" << endl;
}

void Parser::OnLexerError() {
  cout << " LexerError" << endl;
}

