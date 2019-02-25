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
