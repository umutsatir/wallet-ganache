
# Ganache Wallet Program

This program provides you to make transactions in your local Ganache chain. You can create an account and every account automatically connects one of the public key in your local chain. You can create accounts until your keys are done. Also, you can view your current balance, public key and *private key (will be added)* in the website.

## Deployment

To deploy this project run:

Create a Ganache chain and copy the MNEMONIC *(12 word secret recovery phrase)* and create a .env file into the folder.
Open the .env file and write:
```
MNEMONIC = "YOUR_MNEMONIC"
```
Save the file then run these commands:

```bash
  pip install -r requirements.txt
  streamlit run YOUR_PATH/app.py
```



## Roadmap

- Data will be stored in MySQL database


## Appendix

This program is for educational purpose ONLY. Keys can be stolen if you use it in public.
