Feature: CRUD actions
    (CREATE) I want to be able to create a new user
    (READ)   and view this user
    (UPDATE) and when update user name
    (DELETE) and when delete user

    Scenario: create a new user
        Given create user URL
        When Change user name to Mr.Vasya
        Then I should find user in user table

    Scenario: update user
        Given User Mr.Vasya form
        When Change user name to Mr.Petya
        Then I should find user in user table

    Scenario: update goods
        Given update 1 goods URL
        When Change visible to toggle
        When Submitt
        Given update 1 goods URL
        When sleep 2
        Then visible == True
        Then archive == False
        When Change visible to toggle
        When Submitt
        Given update 1 goods URL
        When sleep 2
        Then visible == False
        Then archive == False

    Scenario: delete user
        When Delete user Mr.Petya
        Then I don't want find user in user table
