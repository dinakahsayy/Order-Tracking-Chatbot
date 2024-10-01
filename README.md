#Order Tracking Chatbot Overview

This code creates an order tracking chatbot using Python and GUI made with tkinter. It allows customers to check the status of their orders by entering their order number.
The chatbot uses SQLite to set up an orders table (if the database doesn't already exist) where it keeps important details like the order number, current status, location, shipment date, expected delivery date, and the last update that was logged. The interface is designed to feature an entry field for the order number and a submit button for a simpler interaction.
When a customer submits their order number, the chatbot looks up the information in the database. If the order is found, it displays all the relevant details; if not, it lets the user know that the order doesn’t exist. To make sure everything runs smoothly, the chatbot includes basic error handling to catch any invalid inputs or database issues.
