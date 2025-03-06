黑色 C2
===

## Description
你了解C2伺服器嗎？
我做了一個簡單的 C2 伺服器模擬器，但我認為它太糟糕了。


## 備註
部署備註，或者內部說明可以在這裡寫下。例如，非常大的文件的連結是： http://drive.google.com/abcd

模板 `{...LINK}` 將在我們確定端口號後被實際值替換。

如果文件放在 `public/` 文件夾中，它們將被自動壓縮。如果一個 zip 文件放在 `public/` 文件夾中，它將不會再次壓縮。

## 開發挑戰

查看去年的挑戰示例，以了解如何使用Docker編寫挑戰：

- [C](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/59-easyheap)
- [Python](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/04-pyjail1)
- [PHP](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/70-jqplayground)

主要要點包括：

- 在使用 `apt install` 後進行清理，使用 `rm -rf /var/lib/apt/lists/* /var/cache/apt/*`
- 確保挑戰文件和旗幟由 root 擁有，具有嚴格的權限 `444` 或更低，目錄的權限為 `555` 或更低
- 確保非root用戶執行挑戰