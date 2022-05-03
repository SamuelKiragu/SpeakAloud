# SpeakAloud
Speak aloud is a book review web application that leverages various web technologies to allow the reviewing of books within a set of 5000 books available on Amazon. The list of book's data, in my implementation of this project, was stored using the Heroku cloud service. I used an automation script(which is available in the source code) to populate the database.

(The list of books was made available by the Harvard CS50 team.)

---

### System Workflow
1. The login page allows one to log in while the register file allows on to create an account if they don't already have one.
2. Once one is logged in they are taken to the index.html page which allows them to search for content
3. The results of the search are then held in the results.html page
4. when one clicks on a specific result they are taken to a book.html page which has dynamic content.

> We created an API that can be accessed by keying in the correct path for a specific isbn.   
> In addition we made use of the goodreads API to provide the average rating of a selected book.

---

I created a short walkthrough of the system which is publicly available on [Youtube](https://youtu.be/fKeBRfGjq4c)
