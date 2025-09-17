// Sample LEGv8 Assembly Program
// Demonstrates arithmetic operations and branching

// Initialize values
ADDI X1, XZR, #15    // Load 15 into X1
ADDI X2, XZR, #25    // Load 25 into X2

// Perform arithmetic
ADD X3, X1, X2       // X3 = X1 + X2 = 40
SUB X4, X2, X1       // X4 = X2 - X1 = 10

// Test shifting
LSL X5, X1, X4       // X5 = X1 << X4 = 15 << 10 = 15360
LSR X6, X5, X4       // X6 = X5 >> X4 = 15360 >> 10 = 15

// Compare and branch
SUBS X7, X3, X2      // Compare X3 - X2 (40 - 25 = 15)
B.GT result_positive // Branch if X3 > X2

// This shouldn't execute
MOVZ X8, #999

result_positive:
    MOVZ X8, #42     // X8 = 42 (success indicator)

// Store results
STUR X8, [X28, #0]   // Store final result
STUR X3, [X28, #8]   // Store sum
STUR X4, [X28, #16]  // Store difference
