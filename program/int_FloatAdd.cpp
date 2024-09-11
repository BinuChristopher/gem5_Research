#include <cstdlib> // For malloc and free
#include <iostream>

using namespace std;

int main() {
    // Allocate memory to hold 3000 integers
    int *ptr = (int *)malloc(3000 * sizeof(int));
    // Allocate memory to hold 1000 floats
    double *fptr = (double *)malloc(1000 * sizeof(double));

    // Initialize first elements
    ptr[0] = 11;
    fptr[0] = 22.00;

    // Perform simple integer addition
    ptr[1] = 20;
    int int_sum = ptr[0] + ptr[1];

    // Perform simple float addition
    fptr[1] = 33.00;
    double float_sum = fptr[0] + fptr[1];

    // Free allocated memory
    free(ptr);
    free(fptr);

    return 0;
}
