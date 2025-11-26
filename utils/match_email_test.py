from match_email import extract_email

def test_exctract_email():
    e = "luke hallal <luke.hallal@gmail.com>"

    email = extract_email(e)

    print(email)

if __name__ == "__main__":
    test_exctract_email()