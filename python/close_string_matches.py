#!/usr/bin/env python

import difflib

def main():
  strings = ['Oct 25 10:17:01 ubuntu CRON[6319]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)',
             'Oct 25 11:11:01 ubuntu CRON[428]: (root) CMD (   cd / && run-parts --report /etc/cron.daily)',
             'Oct 25 11:19:01 ubuntu CRON[6528]: (root) CMD (   cd / && run-parts --report /etc/cron.daily)',
             'Oct 25 13:17:01 ubuntu CRON[6745]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)',
             'Oct 25 11:17:01 ubuntu CRON[879]: (root) CMD (   cd / && run-parts --report /etc/cron.daily)']

  for idx, string in enumerate(strings):
    print '%s' % string

    for match in difflib.get_close_matches(string, [x for x in strings if not x == string], len(strings)):
      print ' |- %s' % match

    print

if __name__ == "__main__":
  main()
