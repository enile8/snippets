#include <stdio.h>
#include <stdlib.h>

int align(int value, int boundary)
{
  return (value + ((value + (align - 1) & ~(align - 1))) - value);
}

int main(void)
{
  printf("value=%d, align=%d, next=%d\n", 13, 4, align(13, 4));
  printf("value=%d, align=%d, next=%d\n", 7, 4, align(7, 4));
  printf("value=%d, align=%d, next=%d\n", 62, 4, align(62, 4));
  printf("value=%d, align=%d, next=%d\n", 14, 16, align(14, 16));
  printf("value=%d, align=%d, next=%d\n", 21, 16, align(21, 16));
  printf("value=%d, align=%d, next=%d\n", 58, 16, align(58, 16));
  exit(0);
}
