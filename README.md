# The Digital Relatives
[![HTML](https://img.shields.io/badge/Tech-HTML-orange)](#)
[![CSS](https://img.shields.io/badge/Tech-CSS-blue)](#)
[![JavaScript](https://img.shields.io/badge/Tech-JavaScript-yellow)](#)
[![Python](https://img.shields.io/badge/Tech-Python-green)](#)
[![Bootstrap](https://img.shields.io/badge/Tech-Bootstrap-brightgreen)](#)
[![Django](https://img.shields.io/badge/Tech-Django-red)](#)

## Table of Contents
* [Project Description](#project-description)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [How to Use](#how-to-use)
* [Entity Relationship Diagram](#entity-relationship-diagram)
* [Manual Testing](#manual-testing)
* [Wireframes](#wireframes)
* [User Stories](#user-stories)
* [Future Enhancements](#future-enhancements)
* [Credits](#credits)

## Project Description
<details><summary>Project Description</summary>
This project is a mock "tech support" web application designed to help family members, especially elderly relatives, with their technical issues. Users can type in their questions, and the application will use AI to generate helpful responses.  The goal is to make technology more accessible and less intimidating for those who may not be as familiar with it.

For example, a user could ask:

* "How do I reset my WiFi?"
* "How do I download Facebook?"
</details>

## Tech Stack
<details><summary>Tech Stack</summary>
* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **AI:** Google Generative Language AI (Model: gemini-1.5-flash-002)
</details>

## Features
<details><summary>Features</summary>
* AI-powered question answering: Users can type in their tech support questions and receive AI-generated responses.
* User-friendly interface: The application is designed to be simple and easy to use, especially for elderly users.
* Web-based:  Accessible from any device with a web browser.
</details>

## How to Use
<details><summary>How to Use</summary>
1.  **Installation**
    * Clone the repository.
    * Set up a virtual environment (optional but recommended).
    * Install the required packages using `pip install -r requirements.txt`.
    * Set up your Google Cloud credentials (see "Configuration" below).
    * Run the Django migrations: `python manage.py migrate`.
    * Start the Django development server: `python manage.py runserver`.
    * Open your web browser and go to the provided URL (usually `http://127.0.0.1:8000`).

2.  **Configuration**
    * You will need a Google Cloud account and a project with the Gemini API enabled.
    * Set up authentication by creating a service account and downloading the credentials JSON file.
    * Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the path of your credentials JSON file.  **Important:** Do not include your credentials file in your code repository.
    * Ensure the Google Generative AI library is installed:  `pip install google-generativeai`

3.  **Usage**
    * Once the application is running, users can type their tech support questions into the input field on the main page.
    * The AI-generated response will be displayed on the page.
</details>

## Entity Relationship Diagram
<details><summary>Models</summary>
```mermaid
erDiagram
    User {
        int id
        string username
        string password
    }
    
    Note {
        int id
        string title
        datetime created_at
        int interaction_start_id
        int interaction_end_id
        int user_id
    }
    
    Interaction {
        int id
        string question
        string answer
        float timestamp
        int usr_id
    }

    User ||--o{ Note : owns
    User ||--o{ Interaction : has
    Note ||--|| Interaction : start_id (interaction_start_id)
    Note ||--|| Interaction : end_id (interaction_end_id)
    Note ||--o{ Interaction : references (via start_id to end_id)
    Interaction }o--|| User : belongs_to (usr)
```

- Only the User model is shown from external packages.
- Note references a range of Interactions (from interaction_start_id to interaction_end_id).
- Each Interaction belongs to a User.
- Each Note belongs to a User.

</details>

## Manual Testing
<details><summary>Manual Testing</summary>

### Landing Page (`index.html`)

| TEST ACTION                                                                    | EXPECTATION                                                                                               | RESULT    |
| :----------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- | :-------- |
| User opens the landing page URL                                                | The landing page is displayed with a title, introduction, and a call to action.                            | SUCCESS   |
| User interacts with the input field.                                            | The input field is responsive and allows the user to type their tech support question.                   | SUCCESS   |
| User views the page on different screen sizes (desktop, mobile)               | The layout is responsive and content is displayed correctly.                                               | SUCCESS   |
| User checks for broken links/images.                                            | All links are functional, and all images are displayed correctly.                                           | SUCCESS   |

### AI Response

| TEST ACTION                                                                    | EXPECTATION                                                                                               | RESULT    |
| :----------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- | :-------- |
| User enters a valid tech support question (e.g., "How do I reset my WiFi?")    | The AI generates a relevant and helpful response.                                                      | SUCCESS   |
| User enters an invalid question or gibberish.                                   | The AI provides a graceful error message or a general help response.                                        | SUCCESS   |
| User enters a question with spelling mistakes.                                  | The AI is able to understand the intent and provide a relevant answer.                                     | SUCCESS   |
</details>

## Wireframes
<details><summary>Wireframes</summary>
* *Add wireframes here.  Since I cannot directly create images, you would add image links or embed images here.*
* *Example:*
    * *![Wireframe of the main page](link_to_your_wireframe_image.png)*
</details>

## User Stories
<details><summary>User Stories</summary>
* As a user, I want to be able to easily input my tech support question.
* As a user, I want to receive a helpful and accurate response to my question.
* As a user, I want the application to be easy to use, even if I am not very tech-savvy.
* As a user, I want the application to be accessible from any device with a web browser.
* As a developer, I want to use a reliable AI model to generate accurate responses.
</details>

## Future Enhancements
<details><summary>Future Enhancements</summary>
* Improved AI response accuracy and relevance.
* Support for more complex technical issues.
* Multimedia support (e.g., images, videos) in responses.
* User accounts and history.
* Feedback mechanism for users to rate the helpfulness of the responses.
* Multi-language support.
</details>

## Credits
<details><summary>Credits</summary>
* This project was created by Team5
</details>
