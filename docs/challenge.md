Having in mind that the goal is to identify possible delayed flights, the most important metric here is recall for class "1" (delayed flights).

XGBoost Recall (Class 1 - Delayed Flights): 69%
Logistic Regression Recall (Class 1 - Delayed Flights): 69%
Accuracy for both models: 55%

Both models provided the same recall for delayed flights (69%), but XGBoost is more flexible and tunable, thus I would choose this one for production.

Why?
It can be further fine-tuned to improve performance.
It handles non-linear relationships better than Logistic Regression.
In real-world deployments, XGBoost often outperforms Logistic Regression when more data is available.


### Part I
I didn't manage to pass all the tests, but given the time I allocated for this challenge I prefered to finish all parts better than focus on passing tests.

I have chosen XGBoost for my model, given the facts mentioned above. :)

### Part II
Again, just like Part I, I didn't pass all the 4 tests, instead I focused on finishing the tasks.

### Part III
This was the hardest part, I chose GCP, but I had to install and configure a lot of things in my computer, I also had to set a billing information in my google account to manage to make it work properly, Seems to it is online and passed the test.

### Part IV
This part was quite new to me, so I used chatGPT in order to help me to do this step. Hope it works properly :)

Final comments:
I created a postRequest.py file in the project's root in order to save the json and execute the command.

