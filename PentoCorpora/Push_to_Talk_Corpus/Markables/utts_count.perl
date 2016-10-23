#!/usr/bin/perl -w
#

foreach $utts_markable (@ARGV) {

  open UM, "<$utts_markable";
  $utts_markable =~ s/(.*)_utterance_markables.xml/$1/;


  $utts = 0; 
  $utts_p = 0;
  $utts_e = 0;

  while (<UM>) {

  if (/p-utts/) {
    $utts_p++;
    $utts++;
  } elsif (/e-utts/) {
    $utts_e++;
    $utts++;

  }
}

print "$utts_markable:\n";
print "total utterances: $utts \n";
print "player: $utts_p\n";
print "executor: $utts_e\n\n";

}
