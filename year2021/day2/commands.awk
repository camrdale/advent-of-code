#!/usr/bin/awk -f
BEGIN {
  forward=0
  depth=0
  depth2=0
  aim=0
}

/^forward/ { forward+=$2 ; depth2+=(aim*$2) }
/^down/ { depth+=$2 ; aim+=$2 }
/^up/ { depth-=$2 ; aim-=$2 }

END {
  print "Forward =", forward 
  print "Depth =", depth 
  print "Part 2 Depth =", depth2 
  print "Aim =", aim 
  print "Part 1 Position*Depth =", (forward * depth)
  print "Part 2 Position*Depth =", (forward * depth2)
}
