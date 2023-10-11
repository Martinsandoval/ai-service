# ia-service
A service that provides IA features such as Q&amp;A, text summarization, etc

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

