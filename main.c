// clang -c -fno-asynchronous-unwind-tables -fno-unwind-tables -ffreestanding -march=native -O2 -Wall -Werror -fno-plt -fPIC -x c  main.c -o main.o

/* #include <tgmath.h> */

/* #define __fp16 _Float16 */
/* __attribute__((used)) */
/* static unsigned short __truncdfhf2(double t) { */
/*   return 0; */
/* } */

void r_10_10(__fp16* restrict data0) {
  for (int ridx0 = 0; ridx0 < 10; ridx0++) {
    int acc0 = 0;
    int alu0 = (ridx0*(-1));
    data0[ridx0] = (1+((alu0<0)?1:0)+((alu0<(-1))?1:0)+((alu0<(-2))?1:0)+((alu0<(-3))?1:0)+((alu0<(-4))?1:0)+((alu0<(-5))?1:0)+((alu0<(-6))?1:0)+((alu0<(-7))?1:0)+((alu0<(-8))?1:0)+acc0+(-1));
  }
}

/* void copy(double *restrict data0, __fp16 *restrict data1) { */
/*   for (int ridx0 = 0; ridx0 < 10; ridx0++) { */
/*     data1[ridx0]  = (__fp16)data0[ridx0]; */
/*   } */
/* } */
