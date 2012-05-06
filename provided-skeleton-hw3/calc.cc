// PL homework: calculator

#include <iostream>
#include <sstream>
#include <string>

#include "parser.h"

using namespace std;

int main(int argc, char** argv) {
  string input_str;
  Parser parser;
  while (!cin.eof()) {
    // Get user input.
    cout << "> ";
    std::getline(cin, input_str);
    cout << "input: '" << input_str << "'" << endl;

    // Do the parsing.
    parser.ParseInputString(input_str);
  }
  return 0;
}

