#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include <x86intrin.h>
#include <inttypes.h>
#define MILLION  1000000L

// 256-bit vector containing integers
__m256i MASK_55;
__m256i MASK_33;
__m256i MASK_0F;

#define NumVec   268435456     // 2^28*/
//#define NumVec   1     // 2^28
#define VecLen   256           // vector length in bits
#define NumWord  (VecLen >> 5) // # of unsigned in each vector
#define RandSeed 1283

unsigned *data, *cnt1, *cnt2;

void init(void){
  unsigned i, j;

  srand48(RandSeed); // 32-byte aligned for 256-bit access
  posix_memalign((void **)&data, 32, (size_t)NumVec * (VecLen>>3));
  for (i=0; i<NumVec; i++)
    for (j=0; j<NumWord; j++)            // NumWord = 8, Each vector in AVX can hold upto 32 bytes (256 bit) . Each vector can hold 8 Long int values
        data[(uint64_t)i * NumWord + j] = lrand48();
  posix_memalign((void **)&cnt1, 32, sizeof(unsigned) * NumVec);
  posix_memalign((void **)&cnt2, 32, sizeof(unsigned) * NumVec);
}

void verify(void){
  unsigned i;

  for (i=0; i<NumVec; i++)
    if (cnt1[i] != cnt2[i]){
      printf("%u %u %u\n", i, cnt1[i], cnt2[i]);
      exit(1);
    }
}

void popcnt64(const unsigned *data, unsigned *cnt){
  uint64_t *ptr64;


  uint64_t i; // unsigned integer type with width of exactly 64 bits

  ptr64 = (uint64_t*)data;
#pragma vector aligned
  for (i=0; i<NumVec; i++) {
    cnt[i] =
      _mm_popcnt_u64(ptr64[4 * i]) +
      _mm_popcnt_u64(ptr64[4 * i + 1]) +
      _mm_popcnt_u64(ptr64[4 * i + 2]) +
      _mm_popcnt_u64(ptr64[4 * i + 3]);
        /*printf("The data values is = %d\n", ptr64[0]);
        printf("The data values is = %d\n", ptr64[1]);
        printf("The data values is = %d\n", ptr64[2]);
        printf("The data values is = %d\n", ptr64[3]);
        printf("The count = %u\n", _mm_popcnt_u64(ptr64[4 * i]));
        printf("The count = %u\n", _mm_popcnt_u64(ptr64[4 * i + 1]));
        printf("The count = %u\n", _mm_popcnt_u64(ptr64[4 * i + 2]));
        printf("The count = %u\n", _mm_popcnt_u64(ptr64[4 * i + 3]));*/
        }
}


void avx(const unsigned *data, unsigned *cnt){
  //use AVX and SSE to implement the DIY popcnt for 256-bit vectors
  //https://software.intel.com/sites/landingpage/IntrinsicsGuide/
}



size_t diy256(const unsigned *data, unsigned *cnt){

MASK_55 = _mm256_set1_epi8(0x55);
MASK_33 = _mm256_set1_epi8(0x33);
MASK_0F = _mm256_set1_epi8(0x0F);

unsigned int total;
__m256i *ptr256;
uint64_t *nptr64;
unsigned i;

nptr64 = (uint64_t*)data;
ptr256 = (__m256i*)nptr64;
__m256i count =  _mm256_setzero_si256();

for(i=0; i<NumVec; i++) {
        const __m256i vec = _mm256_load_si256((__m256i*)ptr256 + i);
        const __m256i v1  = _mm256_sub_epi8(vec, (_mm256_srli_epi64(vec,  1) & MASK_55));
        const __m256i v2  = _mm256_add_epi8(v1 & MASK_33, (_mm256_srli_epi64(v1, 2) & MASK_33));
        const __m256i v3  = _mm256_add_epi8(v2, _mm256_srli_epi64(v2, 4)) & MASK_0F;
                   count  = _mm256_sad_epu8(v3, _mm256_setzero_si256());
                   total  = _mm256_extract_epi64(count, 0) + _mm256_extract_epi64(count, 1) + _mm256_extract_epi64(count, 2) + _mm256_extract_epi64(count, 3);
                  cnt[i]  = total;

        //printf("Pointing to Address = %d\n", ptr256 + i);
        //printf("AVX Bit count vec[%d] = %u\n", i, cnt[i]);
        //printf("Size of count = %d\n", sizeof(count));
        }
}

int main(int argc, char* argv[]){
  struct timeval start, stop;
  float sec;

  init();
  gettimeofday(&start, NULL);
  popcnt64(data, cnt1);
  gettimeofday(&stop, NULL);
  sec = (stop.tv_sec - start.tv_sec) +
    (stop.tv_usec - start.tv_usec) / (float)MILLION;
  printf("popcnt64: %.3f sec\n", sec);

  gettimeofday(&start, NULL);
  diy256(data, cnt2); //avx(data, cnt2);
  gettimeofday(&stop, NULL);
  sec = (stop.tv_sec - start.tv_sec) +
    (stop.tv_usec - start.tv_usec) / (float)MILLION;
  printf("avx: %.3f sec\n", sec);

  verify();

  return 0;
}
