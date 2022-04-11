declare -a req
req=$(find . -type f -name "requirements.txt")
for filename in $req
do
    echo "file path" ${filename}
    pip3 install -r ${filename}
done
