for F in $(ls *.txt)
do
    python rap_tokenizer.py $F
done
