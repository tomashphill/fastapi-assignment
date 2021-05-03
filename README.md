### Project Structure:

```
    .
    app
    |-- main.py
    |-- dependencies.py (get_db, get_logger)
    |
    |-- routers
    |   |-- tags.py ("/tag" routes)
    |
    |-- model
        |-- tag.py (Tag, IncrementTag)
        |
        |-- database
            |-- db.py (interface DB)
            |-- firestore.py (firestore DB)
    .        
    tests
    |-- json_db.py 
    |-- test_main.py
    |-- test_main_mock.py (pytests mocking the FireStore api)

```