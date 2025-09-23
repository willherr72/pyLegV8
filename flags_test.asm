// Test program for condition flags and MUL instruction
// Demonstrates flag usage with conditional branches

// Test 1: Basic multiplication 
ADDI X1, XZR, #6     // Load 6
ADDI X2, XZR, #7     // Load 7  
MUL  X3, X1, X2      // X3 = 6 * 7 = 42

// Test 2: Flag setting with SUBS
ADDI X4, XZR, #10    // Load 10
ADDI X5, XZR, #20    // Load 20

// Compare X4 and X5 (10 vs 20) - should set N flag
SUBS X6, X4, X5      // X6 = 10 - 20 = -10, sets N flag (negative)
B.LT  negative_test  // Branch if X4 < X5 (should branch)
MOVZ X7, #999        // This shouldn't execute
B    continue1

negative_test:
    MOVZ X7, #1      // X7 = 1 (confirmed X4 < X5)

continue1:
// Test 3: Zero flag test
SUBS X8, X4, X4      // X8 = X4 - X4 = 0, sets Z flag
B.EQ  zero_test      // Branch if equal (should branch) 
MOVZ X9, #888        // This shouldn't execute
B    continue2

zero_test:
    MOVZ X9, #2      // X9 = 2 (confirmed result was zero)

continue2:
// Test 4: Use multiplication in comparison
ADDI X10, XZR, #3    // Load 3
ADDI X11, XZR, #4    // Load 4
MUL  X12, X10, X11   // X12 = 3 * 4 = 12

SUBS X13, X12, X4    // Compare X12 (12) with X4 (10): 12-10=2
B.GT  greater_test   // Branch if X12 > X4 (should branch)
MOVZ X14, #777       // This shouldn't execute
B    end

greater_test:
    MOVZ X14, #3     // X14 = 3 (confirmed 12 > 10)

end:
// Store results to verify correct execution
STUR X3, [X28, #0]   // Store 42 (6 * 7)
STUR X7, [X28, #8]   // Store 1 (negative test passed)
STUR X9, [X28, #16]  // Store 2 (zero test passed)
STUR X14, [X28, #24] // Store 3 (greater test passed)
B    end             // Halt program
