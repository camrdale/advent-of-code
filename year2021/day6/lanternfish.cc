
#include <iostream>
#include <fstream>
#include <gmpxx.h>
#include <string>
#include <deque>
#include <sstream>
#include <memory>

void run(const std::string& filename, int days) {
  std::ifstream infile;
  infile.open(filename);
  std::deque<std::unique_ptr<mpz_class>> fish;
  for (int i = 0; i < 9; i++) {
    fish.emplace_back(std::make_unique<mpz_class>(0));
  }
  std::string v;
  while (std::getline(infile, v, ',')) {
    (*fish[std::stoi(v)])++;
  }

  for (int day = 0; day < days; day++) {
    std::unique_ptr<mpz_class> multipliers = std::move(fish.front());
    fish.pop_front();
    (*fish[6]) += *multipliers;
    fish.emplace_back(std::move(multipliers));
    // std::cout << "After day " << day << " state is: "
    //   << fish[0] << ", " << fish[1] << ", " << fish[2] << ", "
    //   << fish[3] << ", " << fish[4] << ", " << fish[5] << ", "
    //   << fish[6] << ", " << fish[7] << ", " << fish[8] << std::endl;
  }

  mpz_class result = 0;
  for (const std::unique_ptr<mpz_class>& count : fish) {
    result += *count;
  }
  std::string result_string = result.get_str();
  if (result_string.size() < 100) {
    std::cout << filename << " after " << days
      << " days the number of fish is: " << result_string << std::endl;
  } else {
    std::cout << filename << " after " << days
      << " days the number of digits in the number of fish is: "
      << result_string.size() << std::endl;
  }
}

int main() {
    run("example_input.txt", 80);
    run("input.txt", 80);
    run("example_input.txt", 256);
    run("input.txt", 256);
    run("example_input.txt", 9999999);
    return 0;
}
