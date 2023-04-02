# Du-Script

# First Script
ls -l | tail -n +2 | (while read -r Line; do FileSize=$(echo $Line | awk '{print $5}'); FileName=$(echo $Line | awk '{print $9}'); SumSize=$((SumSize + FileSize)); printf "%-16s %8s %5s\n" $FileName $FileSize $SumSize; done) | tail -n 1

# Second Script
find . -type file | grep -E './[a-zA-Z0-9]*\.(md|jpg|markdown|bash|bashrc|dockerfile|vimrc|gitconfig)' | (while read -r FileName; do FileSize=$(stat -f "%z" $FileName); SumSize=$((SumSize + FileSize)); printf "%-16s %8s %5s\n" $FileName $FileSize $SumSize; done) | tail -n 1
