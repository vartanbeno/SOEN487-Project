# API Descriptions

### Messages
| Method | HTTP request | Description | 
------|------|-----|
| get_conversations | **GET** /conversation | Get all conversations | 
| get_messages | **GET** /conversation/*conversationId* | Get a conversation by ID |
| get_messages_with_limit | **GET** /conversation/*conversationId*/*limit* | Get a conversation by ID with a limit number of messages | 
| create_conversation | **POST** /conversation | Creates a conversation |
| post_message | **POST** /message | Creates a message | 
| delete_message | **DELETE** /message/*messageId* | Deletes a message by ID |
