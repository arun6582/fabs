echo "`date` Screenshot uploader initiated"
sleep .25s
file_name=`ls -Art $1| tail -n 1`
$B2_PATH authorize-account
address=`$B2_PATH upload-file $B2_BUCKET "$1/$file_name" "snaps/$file_name" | $GREP -oP 'URL by file name: https.*'`
echo $address | $GREP -oP 'https.*' | pbcopy
echo $file_name at $address
osascript -e 'display notification "Screenshot uploaded"'
