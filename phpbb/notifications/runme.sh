#!/bin/sh

b=/home/pie/apps/test-repo/phpbb/notifications

:>$b/p1;
:>$b/p2;
:>$b/p3;
:>$b/p4;
for c in `cat $b/clist`; do git rh; rm -rf `git st`; git cp -n $c; git reset;
for k in 1 2 3 4; do
for i in `cat $b/f$k`; do if test -e $i; then git add $i; 
else git rm -fr $i 2>/dev/null; fi; done;
git ci -C $c && git show HEAD|head -1|awk '{print $2}' >> $b/p$k;
done;
git st |grep -q 'nothing to commit' || {
    echo 'stuff did not get committed';
    break;
}
done
