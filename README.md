# BeSpoked-Bikes
Tech Stack: Flask web frameworkfor the backend (Python & SQLAlchemy object-relational mapping mechanism) and HTML, CSS, and JavaScript for the frontend, 

Brainstorming Process & Course of Action: 
Create the database schema:
We need to define the database schema based on the entities mentioned in the requirements. We can use SQLAlchemy to define the schema and create the tables in the database. We will also insert some sample data for testing purposes.

Define the API endpoints:
We need to define the endpoints for each operation mentioned in the requirements. For example, the /salespersons endpoint can be used to retrieve a list of all salespersons, the /salespersons/<id> endpoint can be used to update a specific salesperson, and so on. We will use Flask's routing mechanism to define these endpoints.

Implement the business logic:
We need to implement the business logic for each operation. For example, when creating a new sale, we need to update the product's quantity on hand, calculate the salesperson's commission, and update the sales table with the new sale data. We will use Python functions to implement this logic and call them from the API endpoints.

Define the frontend pages:
We need to create HTML templates for each frontend page, such as the salesperson list page, product list page, and sales report page. We will use Jinja2 templating engine to render these templates with data from the API. The frontend pages should correctly communicate information from the backend through the middleground client API. 

Test the application:
We need to test the application by running it locally and checking if all the operations are working as expected.

Strengths:
Optimized space complexity based on given inputs
Universal attributes quickly accessible as instance variables
Programmer productivity - current implementation is readily scalable

Room for Improvement:
Technical barrier...most efficent tech stack? Issues running Flask framework on local machine
Unique methods for ORM queries and models separate from traditional raw SQL & C#/.Net work environments - learning curve!
Timing
