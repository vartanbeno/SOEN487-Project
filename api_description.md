# API Descriptions

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
| delete_admin | **DELETE** /delete/*adminID* | Deletes an admin by ID |
| get_notifications | **GET** /notifications | Gets all notification types available |
| put_notification | **PUT** /notifications | Puts a notification based on parameters | **type**: String |
| delete_notifications | **DELETE** /notifications/*notificationID* | Deletes a notification based on passed ID |
