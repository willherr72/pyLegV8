// Simple LEGv8 program
// Just basic arithmetic

ADDI X1, XZR, #10
ADDI X2, XZR, #20
ADD X3, X1, X2
STUR X3, [X28, #0]
