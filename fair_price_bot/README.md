# Fair price bot

Gets the wallet holding from the wallets and calculates the token_supply_percent
token_supply_percent = (SUM(wallet_holdings) / total_token_supply) / 100

Calculates the fair price with the following formula:
token_price_in_SOL = 0.0001 ^ (token_supply_percent / 37)

If the token price is above fair price, sells 10.000 FISHIN' tokens

Run in in 1-minute loops.

The trading wallet is an FS wallet, keep all the other supply in hardware wallets for added security.

Make an email sending mechanism, if the trading wallet is low on tokens or SOL

This is just a draft version, once finished and tested migrate it to the blockchain as soon as possible.

designed to utilize Jupiter

written in JavaScript because both Solana an Jupiter offers JavaScript guide

https://station.jup.ag/docs/apis/swap-api

npm i @solana/web3.js
npm i cross-fetch
npm i @project-serum/anchor
npm i bs58

