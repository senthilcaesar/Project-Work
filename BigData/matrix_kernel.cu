/*
 * Copyright 1993-2010 NVIDIA Corporation.  All rights reserved.
 *
 * Please refer to the NVIDIA end user license agreement (EULA) associated
 * with this source code for terms and conditions that govern your use of
 * this software. Any use, reproduction, disclosure, or distribution of
 * this software and related documentation outside the terms of the EULA
 * is strictly prohibited.
 *
 */

/* Matrix multiplication: C = A * B.
 * Device code.
 */

__global__ void matrixMul(float* C, float* A, float* B, int wA, int wB){
  // Block index
  int bx = blockIdx.x;
  int by = blockIdx.y;

  // Thread index
  int tx = threadIdx.x;
  int ty = threadIdx.y;

  // Index of the first sub-matrix of A processed by the block
  int aBegin = wA * (BLOCK_SIZE * by);

  // Index of the last sub-matrix of A processed by the block
  int aEnd   = aBegin + wA;

// Step size used to iterate through the sub-matrices of A
  int aStep  = BLOCK_SIZE;

  // Index of the first sub-matrix of B processed by the block
  int bBegin = BLOCK_SIZE * bx;

  // Step size used to iterate through the sub-matrices of B
  int bStep  = BLOCK_SIZE * wB;
  // Csub is used to store the element of the block sub-matrix
  // that is computed by the thread
  float Csub = 0;

  // Loop over all the sub-matrices of A and B
  // required to compute the block sub-matrix
  for (int a = aBegin, b = bBegin; a < aEnd; a += aStep, b += bStep){
    // Declaration of the shared memory array As used to
    // store the sub-matrix of A
    __shared__ float As[BLOCK_SIZE][BLOCK_SIZE]; // 32 * 32

    // Declaration of the shared memory array Bs used to
    // store the sub-matrix of B
    __shared__ float Bs[BLOCK_SIZE][BLOCK_SIZE];

// Load the matrices from device memory
    // to shared memory; each thread loads
    // one element of each matrix

   if(by <= bx){
          As[ty][tx] = A[a + wA * ty + tx];
          Bs[ty][tx] = A[b + wB * ty + tx];



// Synchronize to make sure the matrices are loaded
          __syncthreads();

    // Multiply the two matrices together;
    // each thread computes one element
    // of the block sub-matrix
        if(by == bx) {
          #pragma unroll
            for (int k = 0; k < BLOCK_SIZE; ++k) {
                   if(ty <= tx) {
                        Csub += As[ty][k] * Bs[k][tx];
                           }
                      }
           }

        else {
          #pragma unroll
            for (int k = 0; k < BLOCK_SIZE; ++k) {
                        Csub += As[ty][k] * Bs[k][tx];


                      }
           }
}



    // Synchronize to make sure that the preceding
    // computation is done before loading two new
    // sub-matrices of A and B in the next iteration
    __syncthreads();
  }

   // Write the block sub-matrix to device memory;
  // each thread writes one element
  int c = wB * BLOCK_SIZE * by + BLOCK_SIZE * bx;
  int block_id = (wA*BLOCK_SIZE)-BLOCK_SIZE;
  if(by == bx){
        if(ty <= tx){
        C[c + wB * ty + tx] = Csub;
        C[c + wB * tx + ty] = C[c + wB * ty + tx];
        }
     }

  if(by < bx) {
        C[c + wB * ty + tx] = Csub;
        C[c + wB * tx + ty + block_id] = C[c + wB * ty + tx];
          }


}
