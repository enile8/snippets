#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <rpc/des_crypt.h>

#define DES_IV  "\x00\x00\x00\x00\x00\x00\x00\x00"
#define DES_KEY "\x01\x23\x45\x67\x89\xab\xcd\xef"

int main(int argc, char *argv[])
{
  char key[8] = "";
  char iv[8] = "";
  char hash[8] = "";
  char upblk[64] = "";
  char upenc[64] = "";
  char c;
  char *ptr;
  int uplen;
  int i;

  if (argc != 3)
  {
    printf("usage: %s <username> <password>\n", argv[0]);
    exit(1);
  }

  ptr = upblk;

  while (c = *argv[1]++)
  {
    *ptr++ = '\x00';
    if ((int)c > 96 && (int)c < 123)
        c ^= 0x20;

    *ptr++ = c;
  }

  while (c = *argv[2]++)
  {
    *ptr++ = '\x00';
    if ((int)c > 96 && (int)c < 123)
        c ^= 0x20;

    *ptr++ = c;
  }

  uplen = ptr - upblk;

  while (uplen % 8)
    uplen++;

  memcpy(upenc, upblk, 64);

  strncpy(iv, DES_IV, 8);

  if (cbc_crypt(DES_KEY, upenc, uplen, DES_ENCRYPT|DES_SW, iv) != DESERR_NONE)
  {
    printf("error, cbc_crypt()\n");
    exit(2);
  }

  memcpy(key, upenc + (uplen - 8), 8);

  strncpy(iv, DES_IV, 8);

  if (cbc_crypt(key, upblk, uplen, DES_ENCRYPT|DES_SW, iv) != DESERR_NONE)
  {
    printf("error, cbc_crypt()\n");
    exit(3);
  }

  memcpy(hash, upblk + (uplen - 8), 8);

  printf("%02X%02X%02X%02X%02X%02X%02X%02X\n", *(hash+0) & 0xff, *(hash+1) & 0xff,
                                               *(hash+2) & 0xff, *(hash+3) & 0xff,
                                               *(hash+4) & 0xff, *(hash+5) & 0xff,
                                               *(hash+6) & 0xff, *(hash+7) & 0xff);

  exit(0);
}


