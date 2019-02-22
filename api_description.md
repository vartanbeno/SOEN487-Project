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
