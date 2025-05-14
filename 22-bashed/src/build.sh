#!/bin/bash


python3 -u generate-step-2.py | tee gen.out
cp out/👂.sh out.sh
chmod +x out.sh
clear;

# ensure that the solution works
python3 solve.py
solutions=$(python3 solve.py | wc -l);
if [[ $solutions -ne 1 ]]; then echo "$solutions solutions found. Please rerun."; exit 1; fi

cp ./out/👂.sh ../public/❤️.sh
cp ./out/👂.sh ./out/.sh
cp -r ./out/. ../env/chall/files

