#include <iostream>
#include <cuda.h>
#include <stdio.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>

// Create two integers for the host
// Allocate memory for copies of them on the device GPU
// Copy the integers to the device memory
// Call the kernel to add them together  <<<   >>>
// Copy the result back to the host memory
// Print out the result that GPU computed
// Free the device memory we allocated


__global__ void Addition(int* a, int* b, int* c) {

        *c = *a + *b;

}

int main()
{
  int a,b,c;
  int *dev_a,*dev_b,*dev_c; // Device Pointers
  int size = sizeof(int);

  cudaMalloc((void**)&dev_a, size);
  cudaMalloc((void**)&dev_b, size);
  cudaMalloc((void**)&dev_c, size);

  a=5,b=6;

  cudaMemcpy(dev_a, &a,sizeof(int), cudaMemcpyHostToDevice);
  cudaMemcpy(dev_b, &b,sizeof(int), cudaMemcpyHostToDevice);

  Addition<<< 1,1 >>>(dev_a,dev_b,dev_c);
  cudaMemcpy(&c, dev_c,size, cudaMemcpyDeviceToHost);

   cudaFree(&dev_a);
   cudaFree(&dev_b);
   cudaFree(&dev_c);

   printf("%d\n", c);
   return 0;

}
