#Pasadena ARTS Visualization App

##Dependencies:
* Node.js
* SASS
* PostgresSQL



##To start the application:

Create a Postgres server and use the SQL commands given in `public/data` to create the table. Change database configurations in `app.js`. Ensure that Ruby is installed on your machine. 

Then run the following commands in the terminal:  

```
npm install

gem install sass

grunt browserify
```

Open a new terminal
```
npm start
```

Go to https://locahost:3000. 