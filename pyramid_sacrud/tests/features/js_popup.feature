Feature: Popup window for delete button

    And now I want to test JavaScript

    Scenario: Check popup in list of users when page is firt time load
        Given list user URL
        Then I should see unactive delete button

    Scenario: Check popup when select 1 row
        Given list user URL
        When sleep 4
        When select 1 item
        Then I should see active delete button
        When Click delete button
        Then I should see active delete popup window

        # reload page
        When f5
        Then I should see unactive delete popup window
        Then I should see active delete button

        # unselect row with id==1
        When select 1 item
        Then I should see unactive delete popup window
        And I should see unactive delete button

    Scenario: Check cancel button in delete popup window on list user
        Given list user URL
        When sleep 4
        When select 1 item
        Then I should see active delete button

        When Click delete button
        Then I should see active delete popup window

        When Click cancel button
        When sleep 1
        Then I should see unactive delete popup window
        Then I should see active delete button

    Scenario: Check cancel button in delete popup window on update form
        Given update 2 user URL
        When sleep 4
        Then I should see active delete button

        When Click delete button
        Then I should see active delete popup window

        When Click cancel button
        When sleep 1
        Then I should see unactive delete popup window
        Then I should see active delete button

    Scenario: Check delete popup window in update form of user when page is firt time load
        Given Update 2 user URL
        When sleep 4
        Then I should see active delete button

    Scenario: Check delete popup window in update form
        Given Update 2 user URL
        When sleep 4
        Then I should see active delete button
        When Click delete button
        Then I should see active delete popup window

        # reload page
        When f5
        Then I should see unactive delete popup window
        Then I should see active delete button
