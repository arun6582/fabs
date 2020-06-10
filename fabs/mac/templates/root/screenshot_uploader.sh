#file_name=`ls -t $1 | head -n1`
echo "`date` Screenshot uploader initiated"
sleep .25s
file_name=`ls -Art $1| tail -n 1`
address=`$imguruploader "$1/$file_name" | $grep -oP 'https.*'`
echo $file_name at $address
osascript -e 'display notification "Screenshot uploaded"'
