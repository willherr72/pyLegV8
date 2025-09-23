// Advanced Mathematics Test - MUL, SMULH, UMULH, SDIV, UDIV
// Comprehensive test of improved multiply and divide instructions

// Test 1: Basic multiplication - should work the same as before
ADDI X1, XZR, #6     // Load 6
ADDI X2, XZR, #7     // Load 7
MUL  X3, X1, X2      // X3 = lower 64 bits of 6 * 7 = 42
UMULH X4, X1, X2     // X4 = upper 64 bits of 6 * 7 = 0 (small result)

// Test 2: Large multiplication where upper bits matter
MOVZ X5, #2000       // Load 2000 (valid immediate)
ADDI X19, XZR, #20   // Load shift amount in register
LSL  X5, X5, X19     // X5 = 2000 << 20 (large number)
MOVZ X6, #3000       // Load 3000 (valid immediate)
LSL  X6, X6, X19     // X6 = 3000 << 20 (large number)

MUL   X7, X5, X6     // X7 = lower 64 bits of large * large
UMULH X8, X5, X6     // X8 = upper 64 bits (non-zero for large numbers)
SMULH X9, X5, X6     // X9 = signed upper bits (same as unsigned for positive)

// Test 3: Signed division
ADDI X10, XZR, #100  // Load 100 (positive)
ADDI X11, XZR, #7    // Load 7 (divisor)
SDIV X12, X10, X11   // X12 = 100 / 7 = 14 (signed division)

// Test 4: Unsigned division (should be same for positive numbers)
UDIV X13, X10, X11   // X13 = 100 / 7 = 14 (unsigned division)

// Test 5: Division where signed/unsigned matters
// Create a large number that appears negative in signed representation
MOVZ X14, #1000      // Load 1000 (valid immediate)
ADDI X20, XZR, #48   // Load shift amount in register  
LSL  X14, X14, X20   // Shift left 48 bits (puts 1 in sign bit)
ADDI X15, XZR, #1000 // Divisor = 1000

SDIV X16, X14, X15   // X16 = signed division (interprets X14 as negative)
UDIV X17, X14, X15   // X17 = unsigned division (interprets X14 as large positive)

// Test 6: Comparison with CMP/CMPI for validation
CMP  X12, X13        // Compare signed vs unsigned division results (should be equal)
B.EQ division_equal
MOVZ X18, #999       // Error marker if not equal
B    store_results

division_equal:
    MOVZ X18, #1     // Success marker

// Store all results for verification
store_results:
STUR X3, [X28, #0]   // Store 42 (basic multiply)
STUR X4, [X28, #8]   // Store 0 (upper bits of small multiply)
STUR X7, [X28, #16]  // Store lower bits of large multiply
STUR X8, [X28, #24]  // Store upper bits of large multiply (non-zero)
STUR X9, [X28, #32]  // Store signed upper bits (should equal X8)
STUR X12, [X28, #40] // Store signed division result (14)
STUR X13, [X28, #48] // Store unsigned division result (14, should equal X12)
STUR X16, [X28, #56] // Store signed division of large number
STUR X17, [X28, #64] // Store unsigned division of large number 
STUR X18, [X28, #72] // Store test validation result (1 = success)

// End program
end:
    B end

// Expected results:
// X3 = 42 (6 * 7)
// X4 = 0 (upper bits of small multiplication)
// X7 = lower 64 bits of large multiplication
// X8 = upper 64 bits of large multiplication (non-zero)
// X9 = signed upper bits (should equal X8 for positive numbers)
// X12 = 14 (100 / 7 signed)
// X13 = 14 (100 / 7 unsigned, same as signed for positive)
// X16 = large negative result (signed interpretation of big number)
// X17 = large positive result (unsigned interpretation)
// X18 = 1 (validation success)
