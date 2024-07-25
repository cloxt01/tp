import pickle

# Dictionary containing the cookies
cookies = [
    {'name': '_abck', 'value': '233EC549F0E1B1346E05C8E66008A6CA~0~YAAQzjLVjJX/D76QAQAAZgU+4gyZjx98aAyWT8macGt2TZMtDhI+WEoP6N0b2/eCfb9UEgbSSp0dunRAjzwZuUAL8UcJATKUM4Fl8Fg7Qvi/ls04/zfItk3kFrtpMeF2iovXIi2yUAm9/kH9tJ5VuuPVqkYNkLd4botPVltY/r1UH9ueVcOP3lwqJ5rRDmwRq3zppVvAoncn6Ff5pCsuxKGRkaCKeoLwUceCLU3CIrF90Ju6jH17dqj4s76poCw5B/gLQeujEXuYi9zYjGPM9a3F1Ss6u9j8UOrCbdumbno9Lcq6hLmrEznaE8cEtH/LfXK9IRdAMEY7arvgy36htXb2ElkMlqEmswlfmihe4j4JBq6IeHN4nDjs6uBotkx27bBtqlAD6t6Y5yCxb38kYM+rhGhiO3mxJSHHnTiEClEq4Tmy68fAdB3sQbPnj4Ck4xgQcl48UsJYnZuUG6a+Sbv…717f313c297f677f6d7f717f313f317f677f173c363c2f293c7d0d282e3c297f717f3132333a7f677f6d7f717f2d1e327f677f7f717f2e14397f676c6c686e6d686a6e717f2e09242d387f677f32323e7f717f2a14397f676d717f2a352e7f677f06007f717f2a352e2e7f677f06007f20', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': 'webauthn-session', 'value': '1eda3556-671d-4f58-ad90-fe20f60cb55e', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': '_UUID_CAS_', 'value': '8f279f87-748d-4039-a50f-0db0d6e652fc', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': 'uidh', 'value': 'M82rZ/zar6Faz1BM2KpkrEeGjWZ9z6MNDPA5Q4PHXsg=', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': 'uide', 'value': 'XQv1Gp4KNB96pj48D0/DLMtVthwxAeDr6t9M2h9TO95dzlp3FQ==', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': '_dc_gtm_UA-126956641-6', 'value': '1', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': '_dc_gtm_UA-9801603-1', 'value': '1', 'domain': 'www.tokopedia.com', 'path': '/'},
    {'name': '_gat_UA-9801603-1', 'value': '1', 'domain': 'www.tokopedia.com', 'path': '/'}
]

# Save cookies to a file
with open('cookies.pkl', 'wb') as file:
    pickle.dump(cookies, file)
