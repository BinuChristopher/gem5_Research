#include <iostream>

using namespace std;

int main() {
// Allocate memory to hold 5 integers
// std::cout << "Size of int: " << sizeof(int) << " bytes" << std::endl;
// std::cout << "Size of float: " << sizeof(float) << " bytes" << std::endl;
  int *ptr = (int *)malloc(3000 * sizeof(int));
  float *fptr = (float *)malloc(1000 * sizeof(float));
  ptr[0] = 11;
  fptr[0] = 22.00;
  free(ptr);
  return 0;
}
