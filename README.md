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
