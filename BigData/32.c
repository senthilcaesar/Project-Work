#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include <x86intrin.h>

#define MASK_01 0x01010101
#define MASK_0F 0x0F0F0F0F
#define MASK_33 0x33333333
#define MASK_55 0x55555555

#define MILLION 1000000L
#define NumVec   8     // 2^28
#define VecLen   32            // vector length in bits
#define NumWord  (VecLen >> 5) // # of unsigned in each vector
#define RandSeed 1283

unsigned *data, *cnt1, *cnt2;

void init(void){
  unsigned i;

  srand48(RandSeed);
  posix_memalign((void **)&data, 16, (size_t)NumVec * (VecLen>>3)); //Dynamic memory allocation that returns 32-bit alligned address
  for (i=0; i<NumVec*NumWord; i++)
    data[i] = lrand48(); // lrand48() returns long int which is of size 32 bit = 4 bytes
  posix_memalign((void **)&cnt1, 16, sizeof(unsigned) * NumVec);
  posix_memalign((void **)&cnt2, 16, sizeof(unsigned) * NumVec);
}

void verify(void){
  unsigned i;

  for (i=0; i<NumVec; i++)
    if (cnt1[i] == cnt2[i]){
      printf("%u %u %u\n", i, cnt1[i], cnt2[i]);
     /* exit(1);*/
    }
}

void popcnt32(const unsigned *data, unsigned *cnt){
  unsigned i;

#pragma vector aligned
  for (i=0; i<NumVec; i++)
    cnt[i] = _mm_popcnt_u32(data[i]);
}

void diy32(const unsigned *data, unsigned *cnt){
  unsigned i, v;

#pragma vector aligned
  for (i=0; i<NumVec; i++){
    v = data[i];
    v = v - ((v >> 1) & MASK_55);
    v = (v & MASK_33) + ((v >> 2) & MASK_33);
    v = (((v + (v >> 4)) & MASK_0F) * MASK_01)>> 24;
    cnt[i] = v;
    printf("Total 1's bit in V[%d] = %d and the values = %d\n", i, cnt[i], data[i]);
  }
}

int main(int argc, char* argv[]){
  struct timeval start, stop;
  float sec;

  init();
  gettimeofday(&start, NULL);
  popcnt32(data, cnt1);
  gettimeofday(&stop, NULL);
  sec = (stop.tv_sec - start.tv_sec) +
    (stop.tv_usec - start.tv_usec) / (float)MILLION;
  printf("popcnt32: %.3f sec\n", sec);

  gettimeofday(&start, NULL);
  diy32(data, cnt2);
  gettimeofday(&stop, NULL);
  sec = (stop.tv_sec - start.tv_sec) +
    (stop.tv_usec - start.tv_usec) / (float)MILLION;
  printf("diy32: %.3f sec\n", sec);

  verify();

  return 0;
}
