#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

__global__ void vectorSum(float *a, float *b, float *c){
  int i = threadIdx.x + blockIdx.x * blockDim.x;
  c[i] = a[i] + b[i];
}

int main(int argc, char *argv[]){
  unsigned int length = 4194304;
  int i, Size;
  float *a, *b, *c, *copyC, *gpuA, *gpuB, *gpuC;
  time_t seed;
  cudaEvent_t start;
  cudaEvent_t stop;
  float msecTotal;

  cudaEventCreate(&start);
  cudaEventCreate(&stop);
  if (argc>1)
    sscanf(argv[1], "%d", &length);
  Size = sizeof(float)*length;
  a = (float *)malloc(Size);
  b = (float *)malloc(Size);
  c = (float *)malloc(Size);
  copyC = (float *)malloc(Size);
  time(&seed);
  srand48(seed);
  for (i=0; i<length; i++)
    a[i] = drand48(), b[i] = drand48();

  cudaSetDevice(0);
  cudaMalloc((void**)&gpuA, Size);
  cudaMalloc((void**)&gpuB, Size);
  cudaMalloc((void**)&gpuC, Size);

  cudaEventRecord(start, NULL);
  for (i=0; i<length; i++)
    c[i] = a[i] + b[i];
  cudaEventRecord(stop, NULL);
  cudaEventSynchronize(stop);
  cudaEventElapsedTime(&msecTotal, start, stop);
  printf("cpu time: %.3f ms\n", msecTotal);

  dim3 numThreads(256, 1);
  dim3 numBlocks(length/numThreads.x, 1);

  cudaEventRecord(start, NULL);
  cudaMemcpy(gpuA, a, Size, cudaMemcpyHostToDevice);
  cudaMemcpy(gpuB, b, Size, cudaMemcpyHostToDevice);

  vectorSum<<<numBlocks, numThreads>>>(gpuA, gpuB, gpuC);
  cudaDeviceSynchronize();
  cudaMemcpy(copyC, gpuC, Size, cudaMemcpyDeviceToHost);

  cudaEventRecord(stop, NULL);
  cudaEventSynchronize(stop);


  cudaEventElapsedTime(&msecTotal, start, stop);
  printf("gpu time: %.3f ms\n", msecTotal);

  for (i=0; i<length; i++)
    if (fabs(c[i]-copyC[i]) > 0.000001){
      printf("%d\t%f\t%f\n", i, c[i], copyC[i]);
      return 1;
    }
  return 0;
}
