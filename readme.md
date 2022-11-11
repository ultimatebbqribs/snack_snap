# snack-snap

**A snack rating site where you take a photo of your food/snack and your friends up vote or downvote the photo of your food.** 

***update - scope change 12/11/22 - site will now show users random recipes from the mealsdb api, which the user can the comment on. Comments from all users to be shown in a feed. User can view their post history on profile page and delete their posts**

The site will have 4 main pages

- login page
- main scroll showing your friends photos with an up/down vote
- add post page -
- profile page listing your history and edit options

database tables will include a user table, post table, comments table 

challenges: how to display data!! 

work on designing website first - and make it responsive! 
Use jinja base templates 

MVP should show images with a like/unlike + comments 

Extra releases will show additional features like uploading images

users 

| id | username | email | password |
| --- | --- | --- | --- |
| num | char | char | hash |

post 

| username | image  | img_title  | upvotes | downvotes | post_id |
| --- | --- | --- | --- | --- | --- |
| char | url | char | num | num | num |
|  |  |  |  |  |  |

post comments 

| post_id | comment | username  |
| --- | --- | --- |
| num | char | char  |