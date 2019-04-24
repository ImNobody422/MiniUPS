#product differentiation
##Functionalities
###Restoring current stutas of world
To handle the condition that when we reconnect a world, we need to recover its previous state. We create a table to store world's id and a boolean field named curr to differentiate the current world and previous worlds, and we ceate an attribute named world_id in each table. We have tables of trucks, packages and account, when server changes current world, we will update all other worlds'curr field in world table into false, and the current world's status into true. Meanwhile, all tuples in other tables cannot be used if their world is marked false. Since we use database to get infomation, we will check availability first by comparing world_id attribute of each tuple with current world_id.
###Email notification
When registering, user could fill profile form which has a field for email. Also, after creating an account, we also provide a function for user to edit email, if user didn't provide email before, he/she could also choose to add email. For sending email, when status of a package changes, we will get user's email from database and send an email to inform the user. So it enables user to prepare to pickup the package, and they can know the current status of his/her packages.
###Sorting packages
To improve convenience, we provide three different buttons in the page for user to view all packages, they are wait for pick up, out for delivery and arrived. By clicking different button, user could view orders which have associated status. With this development, users could have a better way to choose a certain kind of orders to view. 
###Change Destination
In addition to the basic function we provide for users that a user could change his/her own packages destination, we enable a user to edit package's destination by editing packges table when receiving a change destination request. To maintain consistency, both Amazon side and UPS side only enable user to change detination before delivering status.
###Tracking history
In our web side, we provide a page for a user to view his all packages and all status. They could view when the package's status changed and the location the package has been delivered to. 

##Security
###Reconnect previous world
After reconnecting a previous world, since we have store all previous status in our database, we could let the world continue previous opertations but not redo all steps again. 
###Check user_id when editing
We enable everyone to search a package's detail with specific ID, which is what the real UPS do. To maintain security, when user click 'edit destination' button, firstly, we check if user has logged in. If the user has logged in, then check if the maintainer of the package is same as the user. If the user has logged in, and the package belongs to the user, we will empower the user to change destination if the package's status is before delivering. 
###Registeration and login 
We use Django Frame Work to maintain security, for user, they password will be encypted before being inserted into database, which will avoid hackers read the database and use raw password directly.
##Scalibility
###thread and thread pool
In order to handle high concurrency, we use thread and thread pool to handle requests. We create two threads, one is to handle interaction with world and the other is to handle interaction with Amazon. For each thread, we split the whole message into smaller pieces, and we will create a thread pool to handle nesting messages. Through this way, threads could be reused instead creating a large number of threads for multithreaded tasks. 

