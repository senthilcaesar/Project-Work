
----------------------------------------------------------------------------------------------------------------
                                                Part - I
----------------------------------------------------------------------------------------------------------------

Filename = 256.c
Binary   = 256
Makefile = make -f makefile.256

# Sample output:

        popcnt64: 1.044 sec
        avx: 1.365 sec

# Implementation Details:

        Intel AVX Intrinsic is used to count the number of 1's bit in a 256 bit vector
        Each 256 bit vector from data is loaded into the variable "vec"
        The "vec" variable is then masked and right shifted
        The total count is then extracted from four 64 bits

        Each Vector holds 8 long Integer values making the space of 256 bit
        ptr256 pointer variable points to each individual vector upon increment

         ----------------------------Vector 1--------------------------------

         data[0] = 32 bit = (value) 880876433  = (count) 12 = (addr) 36683840
         data[1] = 32 bit = (value) 1587994590 = (count) 22 = (addr) 36683844
         data[2] = 32 bit = (value) 1121047450 = (count) 15 = (addr) 36683848
         data[3] = 32 bit = (value) 287023274  = (count) 12 = (addr) 36683852
         data[4] = 32 bit = (value) 901533100  = (count) 17 = (addr) 36683856
         data[5] = 32 bit = (value) 1873247336 = (count) 19 = (addr) 36683860
         data[6] = 32 bit = (value) 610842225  = (count) 14 = (addr) 36683864
         data[7] = 32 bit = (value) 2079980768 = (count) 21 = (addr) 36683868

                                                 (Total) 132
         --------------------------------------------------------------------

         ptr256 + 0 points to address 36683840 ( Vector 1 )
         ptr256 + 1 points to address 36683872 ( Vector 2 )
         ptr256 + 2 points to address 36683904 ( Vector 3 )

         Size of Pointer (__m256i*)ptr256 is 32 bytes since the size of m256i data type is 32 bytes
         Each time ptr256 is incremented, it will point to the next integer location which is 32 bytes next to the current location

----------------------------------------------------------------------------------------------------------------
                                                Part - II
----------------------------------------------------------------------------------------------------------------

Filename = matrixMul.c
Binary   = matrixMul
Makefile = make -f makefile.matrixMul

# Sample output

        matrix size: 4096
        cpu time: 1023.370 ms
        gpu time: 21.847 ms

# Implementation Details:

        Step 1: Ignore all the Sub-Matrices blocks whose Index "by > bx" ( This conditon will skip the Lower Triangle Matrix Mutiplications )
        Step 2: For Sub-Matrices blocks whose Index "by == bx", Ignore all the threads whose Thread Index "ty > tx" ( We do this because the
                diagonal elements are in this blocks )
        Step 3: For Sub-Matrices blocks who Index "by < bx", we peform all threads Matrix Multiplications
        Step 4: We peform the Matrix Multiplication based on the blocks ( This computation only computes the Upper Triangle of the Matrix
                because we filtered few blocks and threads in Step 2 and Step 3 )
        Step 5: Copy the value "Csub" in parallel to respective index in the output matrix C[]
        Step 6: Simultaneously copy the value "Csub" to the lower traingle by switching the Index postion

# Note

        To perform the symmetric operation within the same block we just switch the Index position "ty" and "tx"
        To perform the symmetric operation between different blocks we switch the Index positions "ty" and "tx" and add the variable "Block_id"
        Block_id = (wA * BLOCK_SIZE) - BLOCK_SIZE
