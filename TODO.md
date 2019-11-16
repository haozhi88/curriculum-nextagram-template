11/11

1. (done) Custom error pages
2. (done) Upload profile image
   -(TODO) How to handle same file name on AWS? ->Rename with datetime
   -(done) How to preview image after selecting file?
3. (done) View images
   -(done) Create images model: user_id (as foreign_key), image_path
   -(done) Create html page to display images of any user
   -(done) Create html page to display images of current user
   11/12
4. Upload images
   -(done) Create html page to upload image of current user
   -(done) Add field for users model: private (default=False)
   11/13
5. (done) Payment gateway -> Brain tree
6. (done) Send email -> Sendgrid
   11/14
7. (done)Sign in via OAuth -> Authlib
   11/15
8. User following user
   -(done) User can follow/unfollow other users
   -(done) Create feed to show followed users
   -(done) Followed user will receive email request to follow
   -(done) If followed user's profile is private, followers can only see the profile after follow request is accepted
   -(done) Route to approve follow request
   11/18
9. Deployment
10. API
11. Bonus
    -Show loading status when uploading image
    -Graceful image
    -Background job
    -Validation for username, password, email during sign in/sign up
    -Card columns
