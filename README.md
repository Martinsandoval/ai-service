# ia-service
A service that provides IA features such as Q&amp;A, text summarization, etc

## Setup

### Requirements
Python version 3.10

Postman version 10+

1. Clone the repository
2. Create a run configuration like this:

![RunConfiguration](https://github.com/Martinsandoval/ia-service/assets/9439367/23e87b17-89f6-4825-a3f4-472c8d439fa1)

4. Install the requirements with `pip install -r requirements.txt`
5. Run the app and you will see that it is running in http://127.0.0.1:5000

## GraphQL Api's

Default DB
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
Code DB
```
query GetCodeSolutionForQuestion {
    getCodeSolutionForQuestion(question: "Write a unit test for the app.py file") {
        result
        errors
    }
}
```
```
mutation GetAnswerForQuestionAndCreateFile {
    getAnswerForQuestionAndCreateFile(
        question: "Write a unit test for the app.py file"
        directory_path: "/home/sando/workspace/generatedFiles"
        filename: "app.test"
    ) {
        result
        errors
    }
}
```


## Demo Video
This video shows how to generate an AI response to different topics using information from other content on the site that has been stored as embeddings in a local vector database.

https://github.com/Martinsandoval/ia-service/assets/9439367/4ea747f0-829e-409c-91df-93439310b53e

