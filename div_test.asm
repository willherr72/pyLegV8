// Test program for DIV (Division) instruction
// Demonstrates integer division operations

// Test 1: Simple division
ADDI X1, XZR, #20    // Load 20 (dividend)
ADDI X2, XZR, #4     // Load 4 (divisor)
DIV  X3, X1, X2      // X3 = 20 / 4 = 5

// Test 2: Division with remainder (integer division)
ADDI X4, XZR, #23    // Load 23 (dividend)
ADDI X5, XZR, #7     // Load 7 (divisor)
DIV  X6, X4, X5      // X6 = 23 / 7 = 3 (remainder discarded)

// Calculate remainder using: remainder = dividend - (quotient * divisor)
MUL  X7, X6, X5      // X7 = 3 * 7 = 21
SUB  X8, X4, X7      // X8 = 23 - 21 = 2 (remainder)

// Test 3: Larger numbers
ADDI X9, XZR, #100   // Load 100
ADDI X10, XZR, #12   // Load 12  
DIV  X11, X9, X10    // X11 = 100 / 12 = 8 (integer division)

// Test 4: Division by 1
ADDI X12, XZR, #42   // Load 42
ADDI X13, XZR, #1    // Load 1
DIV  X14, X12, X13   // X14 = 42 / 1 = 42

// Test 5: Division where dividend is smaller than divisor  
ADDI X15, XZR, #3    // Load 3
ADDI X16, XZR, #10   // Load 10
DIV  X17, X15, X16   // X17 = 3 / 10 = 0 (integer division)

// Store results to memory
STUR X3, [X28, #0]   // Store 5 (20/4)
STUR X6, [X28, #8]   // Store 3 (23/7 quotient)
STUR X8, [X28, #16]  // Store 2 (23/7 remainder)  
STUR X11, [X28, #24] // Store 8 (100/12)
STUR X14, [X28, #32] // Store 42 (42/1)
STUR X17, [X28, #40] // Store 0 (3/10)

// End program 
end:
    B end            // Halt program

// NOTE: Division by zero would cause runtime error
// Uncomment the following line to test error handling:
// DIV X18, X1, XZR  // This would throw "Division by zero error"
