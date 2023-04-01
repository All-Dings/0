# Du-Script

find . -type file | grep -E './[a-zA-Z0-9]*\.(md|jpg|markdown|bash|bashrc)' | (while read -r FileName; do FileSize=$(stat -f "%z" $FileName); SumSize=$((SumSize + FileSize)); printf "%-16s %8s %5s\n" $FileName $FileSize $SumSize; done)
