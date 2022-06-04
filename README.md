
# Trivia API

This is part of Udacity's Trivia app. This API enable different frontend route communicate with the backend. This API enable the app to do the following




## Features

- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
- Delete questions.
- Add questions and require that they include question and answer text.
- Search for questions based on a text query string.
- Play the quiz game, randomizing either all questions or within a specific category.


## About the Stack

The API is follows a microservice structure and employ separarte technology stacks for Backend and Frontend.


### Backend

While the backend is build upon Python using FLASK, it employs different packages to further enhance functionality and features.
All the backed code follows [PEP8 style guidelines](https://peps.python.org/pep-0008/).

- Flask-SQLAlchemy: Adds support for SQLAlchemy
- Flask-CORS: Extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible


#### Folder Structure

- `\backend\flaskr\__init__.py`: Main server file, home to all the routes and their business logic
- `\backend\models.py`: Model file to hold database related logic
- `\backend\test_flaskr.py`: File to run unit tests for routes
### Frontend

The frontend contains a complete React frontend to consume the data from the Flask server



#### Folder Structure

- `\frontend\src\components\FormView.js`: View to render the Home page
- `\frontend\src\components\Header.js`: Navbar Links View
- `\frontend\src\components\Question.js`: Add new question view
- `\frontend\src\components\QuestionView.js`: View questions for a category
- `\frontend\src\components\QuizView.js`: View to play Quiz
- `\frontend\src\components\Search.js`: Search question box
## Installation

Fork, Clone or Copy and open terminal/command prompt/powershell in the program directory


### Backend

Navigate to the `\backend` folder from root directory

```bash
  cd backend
```

Activate virtual env:

- Mac/Linux

```bash
python -m virtualenv env
source env/bin/activate
env\Scripts\activate
```

- Windows

```bash
python -m virtualenv env
env\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the development server

- Mac/Linux
```bash
export  FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

- Windows

Running from commnad prompt
```bash
set  FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Running from powershell/VSCode terminal
```bash
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
flask run --reload
```

The app will start locally on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 


### Frontend

Navigate to the `\frontend` folder from root directory

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run the local server

```bash
npm start
```

The app will start locally on [http://127.0.0.1:3000/](http://127.0.0.1:3000/) or [http://localhost:3000](http://localhost:3000) 


#### Setup DB

Install and run Postgres locally and create the db locally


- Create `trivia` db
```bash
createbd trivia
```

- Populate the database using the `trivia.psql` file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```





## API Reference

- BaseURL: Currently the application is run locally.
- Authentication/API key: Currently the application doesnt require authentication key

#### Get all categories

```http
  GET '/categories'
```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Sample response

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}

```

#### Get questions based on category

```http
GET '/categories/${id}/questions'
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 

Sample response

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

#### Get questions paginated question list

```http
  GET '/questions?page=${integer}'
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `page`      | `integer` | **Optional**. Page number of item to fetch |

- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Sample response
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```


#### Add a new question

```http
  POST '/questions'
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `question`      | `string` | **Required**. Question to be added |
| `answer`      | `string` | **Required**. Answer to be added |

- Sends a post request in order to add a new question
- Request Body: 
Sample request

```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
Does not return any new data

#### Search for a question

```http
  POST '/question'
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `searchTerm`      | `string` | **Required**. Question to search for |
- Sends a post request in order to search for a specific question by search term 
- Request Body: 

Sample request
```
{
    'searchTerm': 'this is the term the user is looking for'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 

Sample response
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```


```http
DELETE '/questions/${id}'
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of question to delete |

- Deletes a specified question using the id of the question
- Request Arguments: id - integer


Does not need to return anything besides the appropriate HTTP status code. 



```http
POST '/quizzes'
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quiz.id`      | `integer` | **Required**. Id of quiz category |
| `previous_questions`      | `array` | **Optional**. If previous question is not determined than it will fetch the very first question in that category |
- Sends a post request in order to get the next question 
- Request Body: 

Sample request
```
{ 
 'previous_questions':  [1, 4, 20, 15],
 'quiz_category': {
                'type': 'Science',
                 'id': '1'
                 }
 }
```

## Running Tests

In order to run the Tests

```bash
  python3 test_flaskr.py
```


## Author

- [@shu-chou](https://github.com/shu-chou)


## Acknowledgements

 - Udacity's API course instructor Coach Caryn 
 - Program mentor Ujjawal Sharma, and all the program batchmates


