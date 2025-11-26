from workflow import process_new_emails

def main():
    print("="*60)
    print("Starting Server")

    process_new_emails()

    print("Finished Processing All Emails")
    print("="*60)

if __name__ == '__main__':
    main()
