# Feature: List of table entries
#
#     And now I want to test JavaScript
#
#     Scenario: check grid columns
#         Given list user URL
#         Then I should see xpath
#             """
#             .//*[@class='sacrud-grid-content-grid__header-item-link' and contains(text(), 'name')]
#             """
#         Then I should see xpath
#             """
#             .//*[@class='sacrud-grid-content-grid__header-item-link' and contains(text(), 'id')]
#             """
#
#     Scenario: check selected all items
#         Given list user URL
#         Then I should see checkbox is unselected
#         When select all item
#         Then I should see checkbox is selected
#         When select all item
#         Then I should see checkbox is unselected
#         When select all item
#         Then I should see checkbox is selected
#
#         # Unselect one item
#         When select 2 item
#         Then I should see checkbox is selected
#             | id | value        |
#             | 1  | selected     |
#             | 2  | unselected   |
#         Then I should see unselected selected_all_item
#         When select all item
#         Then I should see selected selected_all_item
#         When select all item
#         Then I should see checkbox is unselected
#         When select 3 item
#         Then I should see checkbox is unselected
#             | id | value        |
#             | 3  | selected     |
#         When select all item
#         Then I should see checkbox is selected
#         When select 3 item
#         Then I should see checkbox is selected
#             | id | value        |
#             | 3  | unselected   |
#         Then I should see unselected selected_all_item
#         When select 3 item
#         Then I should see checkbox is selected
#         Then I should see selected selected_all_item
#
#     Scenario: check delete button status
#         Given list user URL
#
#         # select all items
#         Then I should see checkbox is unselected
#         Then I should see unactive delete button
#         When select all item
#         Then I should see active delete button
#         When select all item
#         Then I should see unactive delete button
#         When f5
#         Then I should see unactive delete button
#         When select all item
#         Then I should see active delete button
#         When f5
#         Then I should see active delete button
#         When select all item
#         Then I should see unactive delete button
#
#         # select one row
#         When select 3 item
#         Then I should see active delete button
#         When f5
#         Then I should see active delete button
#         When select all item
#         Then I should see active delete button
#         When f5
#         Then I should see active delete button
#         When select 3 item
#         Then I should see active delete button
#         # When sleep 55
#         Then I should see checkbox is selected
#             | id | value       |
#             | 3  | unselected  |
#
#     Scenario: check delete button popup
#         Given list user URL
#         When select all item
#         Then I should see active delete button
#         When click delete button
