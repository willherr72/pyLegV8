// Test program for CMP and CMPI instructions
// Demonstrates clean comparison operations with conditional branches

// Load test values
ADDI X1, XZR, #15    // Load 15
ADDI X2, XZR, #20    // Load 20 
ADDI X3, XZR, #15    // Load 15 (same as X1)

// Test 1: CMP with less than comparison
CMP  X1, X2          // Compare 15 vs 20, sets flags (N flag set since 15-20 < 0)
B.LT test1_pass      // Should branch (15 < 20)
MOVZ X4, #0          // Fail value
B    test2

test1_pass:
    MOVZ X4, #1      // Pass value (X4 = 1)

// Test 2: CMP with equal comparison  
test2:
CMP  X1, X3          // Compare 15 vs 15, sets flags (Z flag set since 15-15 = 0)
B.EQ test2_pass      // Should branch (15 == 15)
MOVZ X5, #0          // Fail value
B    test3

test2_pass:
    MOVZ X5, #2      // Pass value (X5 = 2)

// Test 3: CMPI with immediate comparison
test3:
CMPI X2, #25         // Compare 20 vs 25, sets flags (N flag set since 20-25 < 0)
B.LT test3_pass      // Should branch (20 < 25)
MOVZ X6, #0          // Fail value
B    test4

test3_pass:
    MOVZ X6, #3      // Pass value (X6 = 3)

// Test 4: CMPI with equal immediate
test4:
CMPI X1, #15         // Compare 15 vs 15, sets flags (Z flag set since 15-15 = 0)
B.EQ test4_pass      // Should branch (15 == 15)
MOVZ X7, #0          // Fail value
B    test5

test4_pass:
    MOVZ X7, #4      // Pass value (X7 = 4)

// Test 5: CMP with greater than
test5:
CMP  X2, X1          // Compare 20 vs 15, sets flags (positive result, no flags set)
B.GT test5_pass      // Should branch (20 > 15)
MOVZ X8, #0          // Fail value
B    results

test5_pass:
    MOVZ X8, #5      // Pass value (X8 = 5)

// Store results to verify all tests passed
results:
STUR X4, [X28, #0]   // Should be 1 (CMP less than test)
STUR X5, [X28, #8]   // Should be 2 (CMP equal test)
STUR X6, [X28, #16]  // Should be 3 (CMPI less than test)  
STUR X7, [X28, #24]  // Should be 4 (CMPI equal test)
STUR X8, [X28, #32]  // Should be 5 (CMP greater than test)

// End program
end:
    B end

// Expected results in memory:
// [X28 + 0]  = 1 (CMP X1, X2 with B.LT)
// [X28 + 8]  = 2 (CMP X1, X3 with B.EQ) 
// [X28 + 16] = 3 (CMPI X2, #25 with B.LT)
// [X28 + 24] = 4 (CMPI X1, #15 with B.EQ)
// [X28 + 32] = 5 (CMP X2, X1 with B.GT)
