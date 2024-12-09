# Travel Agent Project

This project demonstrates the creation of an agent for the travel industry, specifically focused on a use case for booking flight tickets.

## TechStack
* MySQL
* MongoDB
* FastAPI
* Chainlit
* OpenAI 

## Main Components

   #### 1. Flight Service
    Provides the functionality for booking flight tickets. This service handles searching for available flights, making reservations, and providing booking details.

   #### 2. Agent
    Acts as the intermediary between the user and the flight service. The agent assists with answering questions and performing flight bookings based on user input.

   #### 3. UI
    A user interface for interacting with the agent. This provides a messaging interface that allows users to ask questions, make flight bookings, and receive updates about their reservations.

## How to Run the Project

To run the project, execute the following command:

```bash
chainlit run ui/app.py
```

Requirements

```bash
poetry install 
```
Before running the project, make sure to install the necessary dependencies.

