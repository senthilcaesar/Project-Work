#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<time.h>
#include<sys/time.h>
#include<omp.h>

unsigned size, numThread, chunk;
double *A, *B, *C;
unsigned verbose;

int main(int argc, char *argv[]) {
 int c;
 unsigned i, j, k;
 struct timeval tv1, tv2;

 numThread = omp_get_max_threads();
 size = 1024;
 verbose = 0;
 while ((c = getopt(argc, argv, "s:t:v")) != -1){
    switch (c){
    case 's': sscanf(optarg, "%u", &size); break;
    case 't': sscanf(optarg, "%u", &numThread); break;
    case 'v': verbose = 1; break;
    default: break;
    }
  }
  if (numThread < 2 || numThread > omp_get_max_threads())
    numThread = omp_get_max_threads();
  omp_set_num_threads(numThread);
  size = (size < 128) ? 1024 : size;

 printf("matrix size %u, number of threads %u\n", size, numThread);
 posix_memalign((void **)&A, 64, sizeof(double) * size * size);
 posix_memalign((void **)&B, 64, sizeof(double) * size * size);
 posix_memalign((void **)&C, 64, sizeof(double) * size * size);

  gettimeofday(&tv1, NULL);
  srand48(tv1.tv_sec + tv1.tv_usec);
  for (i=0; i<size; i++) {
    for (j=0; j<size; j++){
        if(i <= j) {
                A[i*size + j] = drand48();
                A[j*size + i] = A[i*size + j];
                C[i*size + j] = 0.0;
   }
}
}
  gettimeofday(&tv1, NULL);
#pragma omp parallel shared(A,B,C) private(j,k)
{
  #pragma omp for schedule(dynamic) nowait
  for (i=0; i<size; i++){
    for (j=0; j<size; j++){
      for (k=0; k<size; k++) {
        if(i <= j) {
        C[i*size + j] += A[i*size + k] * A[j*size + k];
        /*printf("Thread %d has completed iteration %d.\n", omp_get_thread_num( ), (i*size+j));*/
        }
       }
        C[j*size + i] = C[i*size + j];
    }
  }
}


  gettimeofday(&tv2,NULL);
  printf("elapsed time %f sec\n",
    (tv2.tv_sec-tv1.tv_sec) + (tv2.tv_usec-tv1.tv_usec) / 1000000.0);

  return 0;

}
