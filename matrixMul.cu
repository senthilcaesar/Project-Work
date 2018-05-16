#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>


#define BLOCK_SIZE 32
// include the kernel
#include "matrixMul_kernel.cu"

unsigned Size;
float *A, *B, *C;

void gpuInit(void){
  cudaSetDevice(0);
}

int main(int argc, char *argv[]){
  int i, j, k, c;
  float cpuTime, gpuTime;
  cudaEvent_t start;
  cudaEvent_t stop;

 Size = 1024;
 while ((c = getopt(argc, argv, "s:")) != -1){
    switch (c){
    case 's': sscanf(optarg, "%u", &Size); break;
    default: break;
    }
  }

  size_t memSize = Size * Size * sizeof(float);

  gpuInit();
  cudaEventCreate(&start);
  cudaEventCreate(&stop);

  A = (float*)malloc(memSize);
  B = (float*)malloc(memSize);
  C = (float*)malloc(memSize);

  printf("matrix size: %d\n", Size);

 for (i=0; i<Size; i++) {
    for (j=0; j<Size; j++){
        if(i <= j) {
                A[i*Size + j] = drand48();
                A[j*Size + i] = A[i*Size + j];
                C[i*Size + j] = 0.0;
          }
   }
}


  cudaEventRecord(start, NULL);
#pragma omp parallel for shared(A,B,C,i) private(j,k)
  for (i=0; i<Size; i++){
    for (j=0; j<Size; j++){
      for (k=0; k<Size; k++) {
        if(i <= j) {
        C[i*Size + j] += A[i*Size + k] * A[j*Size + k];
        }
       }
        C[j*Size + i] = C[i*Size + j];
    }
  }


  cudaEventRecord(stop, NULL);
  cudaEventSynchronize(stop);
  cudaEventElapsedTime(&cpuTime, start, stop);
  printf("cpu time: %.3f ms\n", cpuTime);

  float *d_A, *d_B, *d_C;
  cudaMalloc((void**) &d_A, memSize);
  cudaMalloc((void**) &d_B, memSize);
  cudaMalloc((void**) &d_C, memSize);

  cudaMemcpy(d_A, A, memSize, cudaMemcpyHostToDevice);
  cudaMemcpy(d_B, B, memSize, cudaMemcpyHostToDevice);
  dim3 threads(BLOCK_SIZE, BLOCK_SIZE);                 // 32*32 ( 1024 threads in each block )
  dim3 grid(Size/threads.x, Size/threads.y);            // 4096/32 = 128*128 Blocks = 16,384 blocks and
                                                        // 16,384 * 1024 = 16,777,216
 // There are 32 warps in each block . There are 32 threads in a warp each having consecutive threadIdx
  cudaEventRecord(start, NULL);
  matrixMul<<<grid, threads>>>(d_C, d_A, d_B, Size, Size);
 // The follwing would launch 16,384 blocks of 1024 threads each ( total of 16,777,216 threads )
 // threads.x = 32
 // threads.y = 32


cudaDeviceSynchronize();
  cudaEventRecord(stop, NULL);
  cudaEventSynchronize(stop);
  cudaMemcpy(C, d_C, memSize, cudaMemcpyDeviceToHost);
  cudaEventElapsedTime(&gpuTime, start, stop);
  printf("gpu time: %.3f ms\n", gpuTime);

//for(int i=0; i < 16; i++) {
//      printf("C[%d] = %f\n", i, C[i]);

//}

  return 0;
}
