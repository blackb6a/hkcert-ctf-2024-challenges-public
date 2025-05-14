Writeup
===

Scammer's wallet address in the YouTube video

1. Check your eyesight: https://youtu.be/dK6U9P9pt6A?t=267
2. https://etherscan.io/block/19836136
3. Find the list of transactions and get `0x414f7e5052e016e79bd405648fab12257dcdd7bb` 

Scammer's actual wallet address to receive fund from victims

1. Find the contract code from video description: https://codeshare.io/0bV94e
2. On line 246: `payable(tradeRouter).transfer(address(this).balance);` it will transfer the victim's fund to the attacker.
3. The `tradeRouter` address could be found by track back to line 243: `address tradeRouter = getDexRouter(DexRouter, factory);`
4. The function `getDexRouter` at L236-L239 is basically xor the two inputs.
5. `DexRouter` is `0xfdc54b1a6f53a21d375d0dea4b719169497dbac884f858c6cc4034ec1a5c51dc` and `factory` is `0xfdc54b1a6f53a21d375d0deacc54b9f1d5309afc19f5eb0cca35296fc6da89ed`. After xor the two input it gives `0x872528989c4d20349d0db3ca06751d83dc86d831`

First victim's wallet address

1. Go to Etherscan.io and search the attacker's wallet addres. https://etherscan.io/address/0x872528989c4d20349d0db3ca06751d83dc86d831
2. Find the first internal transaction: 0x8e65aedf6afc5a7f58557571ddf3781e3cb5eee4
3. Find the contract creator: https://etherscan.io/address/0x8e65aedf6afc5a7f58557571ddf3781e3cb5eee4 and get `0x04db59d574be8d84a2e5d1ee8613c3ca16fd784c`