python generator.py
g++ --static -fuse-ld=lld -g -Wl,--omagic output.cpp -o a.out
python processor.py
