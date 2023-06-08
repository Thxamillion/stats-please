def handle_query(query):
    # Replace this with your NLP and database logic
    print(f"Handling query: {query}")


while True:
    query = input("Enter a query: ")
    if query.lower() == "quit":
        break
    handle_query(query)
