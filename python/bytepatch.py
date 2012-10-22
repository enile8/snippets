#!/usr/bin/env python

import os
import sys
import getopt
import mmap
import binascii

def usage():
  print "usage: %s [-o|--offset <seek offset>] -s|--search <search bytes> -r|--replace <replace with bytes> -f|--file <filename>" % os.path.basename(sys.argv[0])
  sys.exit(-1)


def fmtsize(n):
  for x in ['bytes', 'KB', 'MB', 'GB']:
    if n < 1024:
      return "%d %s" % (n, x)
    n /= 1024


def hexdump(start, end, data, prefix='', bytesperline=16):
  sys.stdout.write('%s %08x  ' % (prefix, start))
  for seek, byte in enumerate(data[start:end]):
    if seek > 0 and not seek % bytesperline:
      sys.stdout.write('\n%s %08x  ' % (prefix, (start + seek)))
    elif seek > 0 and seek % bytesperline and not seek % (bytesperline / 2):
      sys.stdout.write(' ')
    sys.stdout.write('%02x ' % ord(data[start+seek]))
  sys.stdout.write('\n')


def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:s:r:f:", ["help", "offset=", "search=", "replace=", "file="])
  except getopt.GetoptError, e:
    usage()

  offset = 0
  search = None
  replace = None
  filename = None

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
    if opt in ('-o', '--offset'):
      offset = arg
    if opt in ('-f', '--file'):
      filename = arg
    if opt in ('-s', '--search'):
      search = arg
    if opt in ('-r', '--replace'):
      replace = arg

  if None in (search, replace, filename):
    usage()

  try:
    offset = int(offset)
    search = binascii.unhexlify(search)
    replace = binascii.unhexlify(replace)
  except TypeError:
    print "[!] search and replace values must be a hexadecimal string (eg: 41420a43440a)"
    sys.exit(1)
  except ValueError:
    print "[!] offset value must be a number"
    sys.exit(1)

  if len(replace) > len(search):
    print "[!] number of patch bytes must be less than or equal to the number of bytes being replace"
    sys.exit(1)

  patch = [x for x in '\x90' * len(search)]
  patch[0:len(replace)] = replace

  sz_file = os.stat(filename).st_size

  print 'File: %s' % filename
  print 'Size: %s (%d bytes)' % (fmtsize(sz_file), sz_file)
  print 'Search: %s' % ' '.join(['%02X' % x for x in bytearray(search)])
  print 'Replace: %s' % ' '.join(['%02X' % x for x in bytearray(patch)])

  if offset:
    print 'Seeking to 0x%x (%d) before pattern search' % (offset, offset)

  if os.path.exists(filename):
    try:
      fd = open(filename, 'rb+')
      map = mmap.mmap(fd.fileno(), 0)

      needle = map.find(search, offset)

      if needle > -1:
        print 'Pattern found at offset 0x%x (%d)' % (needle, needle)

        start = 0
        if needle > 32:
          start = needle - 32

        end = needle + len(search) + 32
        if end > len(map):
          end = len(map)

        hexdump(start, end, map, '-')
        map[needle:needle+len(patch)] = ''.join(patch)
        hexdump(start, end, map, '+')
      else:
        print 'Could not find pattern in file'

      map.close()
    except:
      raise

if __name__ == "__main__":
  main()
