1. (todo) Sign up, sign in and edit userprofile validation for username, email, password
   11/11
2. (done) Custom error pages
3. (done) Upload profile image
   -(TODO) How to handle same file name on AWS? ->Rename with datetime
   -(done) How to preview image after selecting file?
4. (done) View images
   -(done) Create images model: user_id (as foreign_key), image_path
   -(done) Create html page to display images of any user
   -(done) Create html page to display images of current user
   11/12
5. Upload images
   -(done) Create html page to upload image of current user
   -(done) Add field for users model: private (default=False)
   11/13
6. (done) Payment gateway -> Brain tree
7. (done) Send email -> Sendgrid
8. (TODO) Background job
   11/14
9. (done)Sign in via OAuth -> Authlib
   11/15
10. User following user
    -User can follow other users
    -Create feed to show followed users
    -Followed user will receive email request to follow
    -If followed user's profile is private, followers can only see the profile after follow request is accepted
    -Route to approve follow request
    11/16
11. Deployment
12. API
