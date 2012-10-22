#!/usr/bin/perl

use Crypt::CBC;

my ($username, $password, $correcthash) = ("SYSDBA", "DBAPASSWD", "C97C7B346237D4DB");
my $hash = &oracle_hash($username, $password);
printf "%-20s %-20s %-20s %-20s\n", $username, $correcthash, $hash, ($hash eq $correcthash) ? "OK" : "Failed";

sub oracle_hash
{
  my ($username, $password) = @_;

  my $userpass = pack('n*', unpack('C*', uc($username.$password)));
  $userpass .= pack('C', 0) while (length($userpass) % 8);

  my $key = pack('H*', "0123456789ABCDEF");
  my $iv = pack('H*', "0000000000000000");

  my $c = new Crypt::CBC( -literal_key => 1,
                          -cipher => "DES",
                          -key => $key,
                          -iv => $iv,
                          -header => "none" );

  my $key2 = substr($c->encrypt($userpass), length($userpass)-8, 8);

  my $c2 = new Crypt::CBC( -literal_key => 1,
                           -cipher => "DES",
                           -key => $key2,
                           -iv => $iv,
                           -header => "none" );

  my $hash = substr($c2->encrypt($userpass), length($userpass)-8, 8);

  return uc(unpack('H*', $hash));
}
