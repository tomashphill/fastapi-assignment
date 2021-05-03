### Project Structure:

```
    app
    |-- main.py (dependency injection, calls create_app)
    |-- application.py (creates app)
    |
    |-- model
        |-- tag.py (Tag, IncrementTag)
        |
        |-- database
            |-- db.py (interface DB)
            |-- firestore.py (firestore DB)
            
    tests
    |-- mock_db.py (json DB)
    |-- test_main.py

```