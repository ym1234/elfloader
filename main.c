// clang -c -fno-asynchronous-unwind-tables -fno-unwind-tables -ffreestanding -march=native -O2 -Wall -Werror -fno-plt -fPIC -x c  main.c -o main.o
// use -target aarch64-apple-none-elf on mac
// Clang trunk has fixes for no-plt on aarch64

/* #include <tgmath.h> */

/* #define __fp16 _Float16 */
/* __attribute__((used)) */
/* /1* __attribute__((noplt)) *1/ */
/* unsigned short __truncdfhf2(double t) { */
/*   return 0; */
/* } */

/* extern void whatever(void); */

/* void r_10_10(__fp16* restrict data0) { */
/*   for (int ridx0 = 0; ridx0 < 10; ridx0++) { */
/*     whatever(); */
/*     int acc0 = __truncdfhf2(20); */
/*     int alu0 = (ridx0*(-1)); */
/*     data0[ridx0] = (1+((alu0<0)?1:0)+((alu0<(-1))?1:0)+((alu0<(-2))?1:0)+((alu0<(-3))?1:0)+((alu0<(-4))?1:0)+((alu0<(-5))?1:0)+((alu0<(-6))?1:0)+((alu0<(-7))?1:0)+((alu0<(-8))?1:0)+acc0+(-1)); */
/*   } */
/* } */

/* void copy(double *restrict data0, __fp16 *restrict data1) { */
/*   for (int ridx0 = 0; ridx0 < 10; ridx0++) { */
/*     data1[ridx0]  = (__fp16)data0[ridx0]; */
/*   } */
/* } */

extern void foo(void);

int main() {
  foo();
}
