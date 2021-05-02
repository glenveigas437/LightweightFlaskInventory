#Inventory App
Inventory Management Application built with Flask

Features of this App
1) Add Products, Update Products, View Products
2) Add Locations, Update Locations, View Locations
3) Add Movements of Products to the Base Location(X) or Move Products from Location(X) to Location(Y)
4) Update Movements, View Movements

To run this app
1) Download the Source Code
2) Open your Command Prompt in Windows/Terminal in Linux
3) and type the command: 'python inventoryApp.py'
4) The App will be running in your localhost
5) Play with it!


So, let me give you a walkthrough of this Application

This is how the Home Screen Looks 
![Application Home](https://user-images.githubusercontent.com/31877827/109277123-e5943b80-783c-11eb-935d-77e54dc4fd3a.PNG)

As per the features the articles contain the views, and the navbar consists of the actual functionalities

1) Adding Products

![When no products are added the 'View Products' article provides a link to the 'Add Product' page](https://user-images.githubusercontent.com/31877827/109277503-6fdc9f80-783d-11eb-909b-6b7771de63f8.PNG)

![Adding Product](https://user-images.githubusercontent.com/31877827/109277548-7e2abb80-783d-11eb-9ac2-5a8c5966a70b.PNG)

![Flash providing confirmation of Product being added to the database](https://user-images.githubusercontent.com/31877827/109277752-bd590c80-783d-11eb-9466-b5fbac4d2944.PNG)

2) Adding Location

![Add Location](https://user-images.githubusercontent.com/31877827/109277918-f42f2280-783d-11eb-8238-6b7e82ea0ffd.PNG)

3) Adding Movements
i) Moving Product to base location
![No Location](https://user-images.githubusercontent.com/31877827/109278094-250f5780-783e-11eb-8e36-5ee34f8429f6.PNG)

ii) Transfering Product from Location(X) to Location(Y) 
![Transfer](https://user-images.githubusercontent.com/31877827/109278187-407a6280-783e-11eb-93a1-a37e0f64206e.PNG)

iii) Flashing Error if Product being transferred is not available in the base location
![Error](https://user-images.githubusercontent.com/31877827/109278298-6142b800-783e-11eb-99d5-4815fa33c303.PNG)

4) View Products, Locations and Movements

![Product List](https://user-images.githubusercontent.com/31877827/109278601-b4b50600-783e-11eb-9287-6133487a4094.PNG)

![Location List](https://user-images.githubusercontent.com/31877827/109278606-b5e63300-783e-11eb-916b-2bdb340830f1.PNG)

![Movements](https://user-images.githubusercontent.com/31877827/109278608-b5e63300-783e-11eb-8c04-350666b4b3ea.PNG)

You can also view the Status of the stocks that are allocated at each location and also view the unallocated items too.

![Stock Status1](https://user-images.githubusercontent.com/31877827/109278789-f3e35700-783e-11eb-81a1-c127eca46fa9.PNG)

![Stock Status2](https://user-images.githubusercontent.com/31877827/109278795-f5148400-783e-11eb-8d25-b2cddf9e876f.PNG)

5) Update Feature
![Update](https://user-images.githubusercontent.com/31877827/109278877-0e1d3500-783f-11eb-82ea-24cb350e099d.PNG)







