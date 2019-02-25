# API Descriptions

### Authentication

| Method | HTTP request | Description | Body parameters |
------|------|-----|------|
| register | **POST** /user/register | Register for an account.<br>Once registered, you receive<br>an email with a verification link.<br>Username must be unique. | **firstName**: string<br>**lastName**: string<br>**email**: string<br>**username**: string<br>**password**: string
| login | **POST** /user/login | Log in to your account.<br>You cannot log in unless verified. | **username**: string<br>**password**: string
| verify | **POST** /user/verify?key=[key] | Verify your account.<br>The verification key is given as<br> a parameter in the URL. | N/A

Once logged in, the user is provided a JSON Web Token (JWT) which authorizes them to make authenticated requests to the server.

If we choose to offer different privileges to different users, we can also put roles in the claims of the token, which can be decoded for each request where we want to check its claims.

### Messages

| Method | HTTP request | Description | Body parameters |
------|------|-----|------|
| get_conversations | **GET** /conversation | Get all conversations | 
| get_messages | **GET** /conversation/*conversationId* | Get a conversation by ID |
| get_messages_with_limit | **GET** /conversation/*conversationId*/*limit* | Get a conversation by ID with a limit number of messages | 
| create_conversation | **POST** /conversation | Creates a conversation | **creator_id**: int<br /> **participant_id**:int |
| post_message | **POST** /message | Creates a message | **conversation_id**:int <br/>**sender_id**:int <br /> **text**:string |
| delete_message | **DELETE** /message/*messageId* | Deletes a message by ID |

### Users and Notifications
| Method | HTTP request | Description | Body parameters |
------|------|-----|------|
| get_all_persons | **GET** /person | Gets the list of all registered users and admins |
| get_person | **GET** /person/*personID* | Gets a person by passeed ID |
| put_person | **PUT** /person | Inserts a person into the DB | **name**: String <br /> **email**: email <br /> **password**: String <br /> **notifications**: Boolean <br /> **notificationType**: String |
| get_all_admin | **GET** /admin | Gets a list of all admins |
| get_admin | **GET** /admin/*adminID* | Gets an admin by passed ID |
| delete_admin | **DELETE** /admin/*adminID* | Deletes an admin by ID |
| get_notifications | **GET** /notifications | Gets all notification types available |
| put_notification | **PUT** /notifications | Puts a notification based on parameters | **type**: String |
| delete_notifications | **DELETE** /notifications/*notificationID* | Deletes a notification based on passed ID |

### Image storage
| Method | HTTP request | Description | Body parameters |
------|------|-----|------|
| get_img_by_album | **GET** /image/Album/*albumID* | Gets the list of all images in an album by passed ID |
| get_img | **GET** /image/*imageID* | Gets an image by passed ID |
| create_img | **POST** /Album/*album_id*/addPicture | Inserts an image into the DB | **image**: file <br /> **name**: String |
| create_album | **POST** /createAlbum | Inserts an Album into the DB | **name**: String |
| delete_album | **DELETE** /deleteAlbum/*albumID* | Deletes an album and its related pictures by ID | 
| delete_img | **DELETE** /deleteImg/*imgageID* | Deletes an image by ID |

