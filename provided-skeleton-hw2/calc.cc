// PL homework: calculator

#include <iostream>
#include <sstream>
#include <string>

#include "lexical_analyzer.h"

using namespace std;

int main(int argc, char** argv) {
  string input_str;
  LexicalAnalyzer lex;
  while (!cin.eof()) {
    // Get user input.
    cout << "> ";
    std::getline(cin, input_str);

    // Setup lexical analyzer.
    lex.SetInputString(input_str);
    Token token = ERROR;
    do {
      token = lex.Lex();
      if (token == ERROR) {
        cout << "calc: lex error in '" << input_str << "'" << endl;
      } else {
        cout << "calc: lex " << token << " - " << lex.GetTokenString() << endl;
      }
    } while (token != ERROR && token != EOS);
  }
  return 0;
}

