# ia-service
A service that provides IA features such as Q&amp;A, text summarization, etc

## Setup

### Requirements
Python version 3.10

Postman version 10+

1. Clone the repository
2. Create a run configuration like this
3. Install the requirements with `pip install -r requirements.txt`
4. Run the app and you will see that it is running in http://127.0.0.1:5000

## GraphQL Api's

```
query GetSuggestionForText {
    getSuggestionForText(text: "put your text here") {
        result
        errors
    }
}
```
```
mutation CreateEmbedding {
    createEmbedding(document: "insert your text embedding here") {
        success
        errors
    }
}
```

## Demo Video
https://github.com/Martinsandoval/ia-service/assets/9439367/4ea747f0-829e-409c-91df-93439310b53e

