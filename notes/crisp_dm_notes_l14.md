## Lesson 1.4: CRISP-DM ML Process

This discusses the methodology for organizing ML project.

CRISP-DM stands for ``Cross Industry Standard Process for Data Mining`` and is a standard methodology for organizing and executing machine learning and data mining projects.

## Steps

**1. Business Understanding**: the goal here is to identify the problem that needs to be solved and how to solve it. An important question here is *"Do we need ML here?"*. Understand the depth of the problem, the number of users facing this problem and whether ML will help. If not, propose an alternative solution.
If ML is the solution:
`a. Define the goal`
    - be very specific about how success will be measured. For e.g., reduce spam by 50%

**2. Data Understanding**: we need to make sure the data for solving this problem by building a model is available or if not available, where can we get the data for this problem. Is the data good enough, or even large enough or even reliable enough? What is learned here can also influence our understanding of the problem and even result in revising the solution for the problem

**3. Data Preparation**: here, we transform the data so it can be put into a ML algorithm.
The steps here include:
    - clean the data
    - build the pipelines
    - convert cleaned data into tabular form redy to feed to a machine learning model

**4. Modelling**: training the model happpens here. Different models are trained and the best one is selected e.g., logistic regression, decision tree, neural networks, etc. Sometimes, the engineer can go back to the data preparation step and add more data to improve performance.

**5. Evaluation**: here, you go back to the business goal and ask whether the model has successfully achieved that goal. Based on evaluation, you can decide to reevaluate the business goal, or roll out the model to users or completely stop the project.

**6. Deployment**: evaluation and deployment goes together. Here, we deploy the model to production and introduce proper monitoring ensuring model quality and maintainability.

This process is iterative. ML projects require multiple iterations and doesn't stop at deployment.
Basically, *start small -> learn from feedback -> improve*
