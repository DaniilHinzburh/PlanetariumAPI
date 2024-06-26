# PlanetariumAPI

## Project: Simulates an online service for selling tickets to various shows in a planetarium.

## Features

#### JWT authenticated
#### Admin panel /admin/
#### Documentation is located at /api/doc/swagger/
#### Managing reservation and tickets
#### Creating astronomy show with themes
#### Creating planetarium domes 
#### Adding show sessions
#### Filtering astronomy show

## Models:

PlanetariumDome: The hall in which the show will be shown

ShowTheme: The theme of the show

AstronomyShow: A show that can have multiple themes

ShowSession: A show session that takes place in a specific PlanetariumDome and shows a specific show

Ticket: A ticket to a ShowSession

Reservation: A reservation that can include multiple tickets to different ShowSessions.

# Database Structure:

![img.png](database_structure.png)

# How to run the project?

## You need to use docker.

Enter the following commands in the terminal:

    docker-compose build

    docker-compose up

Then follow the link:

http://localhost:8001/api/planetarium/

You can see the list of endpoints:
![endpoints.png](endpoints.png)

Next, you need to log in and get a token (otherwise the system will not allow you to access the data)

Follow the link:

http://localhost:8001/api/user/token/

Here you can log in as an admin or as a regular user (the user has limited access rights, I recommend logging in as an
admin)

## Admin:

Email: admin@gmail.com

Password: 12345678

## User:

Email: user@gmail.com

Password: 12345678

## Next, use the ModHeader extension for your browser:

![modheader.png](modheader.png)

In the Name field: Authorization, in the Value field: Bearer “your access token”

Check the box opposite.

![modheader_check.png](modheader_check.png)

You can return to

http://localhost:8001/api/planetarium/

## Now you can use the project and visit all endpoints

### If you are logged in as an admin:

you can view, add, edit, delete objects of the PlanetariumDome, ShowTheme,
AstronomyShow, Reservation models.

You can view the lists of all objects of the PlanetariumDome, ShowTheme, AstronomyShow, Ticket, Reservation models.

### If you are logged in as a user:

you can only see the lists of the PlanetariumDome, ShowTheme, AstronomyShow, Ticket, Reservation models. You can also create a new object of the Reservation model.

### Note: 
Admin can see tickets and reservations of all users in the database, but a regular user will only see their own
tickets and reservations.
