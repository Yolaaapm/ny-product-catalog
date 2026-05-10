Feature: Product Catalog Administration
    As a Product Manager
    I want to manage the product catalog
    So that I can keep the product information up to date

    Background:
        Given the following products
            | name       | description       | price | available | category    |
            | Hat        | A stylish hat     | 10.0  | True      | CLOTHS      |
            | Apple      | A crunchy apple   | 1.0   | True      | FOOD        |
            | Hammer     | A heavy hammer    | 15.0  | False     | TOOLS       |

    Scenario: Read a Product
        Given I am on the "Home Page"
        When I set the "Name" to "Hat"
        And I click the "Search" button
        Then I should see the message "Success"
        When I click the "Edit" button
        Then I should see "Hat" in the "Name" field
        And I should see "A stylish hat" in the "Description" field

    Scenario: Update a Product
        Given I am on the "Home Page"
        When I set the "Name" to "Hat"
        And I click the "Search" button
        Then I should see the message "Success"
        When I click the "Edit" button
        And I set the "Description" to "A very stylish hat"
        And I click the "Update" button
        Then I should see the message "Success"
        When I click the "Clear" button
        And I set the "Name" to "Hat"
        And I click the "Search" button
        Then I should see "A very stylish hat" in the results

    Scenario: Delete a Product
        Given I am on the "Home Page"
        When I set the "Name" to "Hat"
        And I click the "Search" button
        Then I should see "Hat" in the results
        When I click the "Delete" button
        Then I should see the message "Product has been Deleted!"
        When I click the "Search" button
        Then I should not see "Hat" in the results

    Scenario: List all Products
        Given I am on the "Home Page"
        When I click the "Search" button
        Then I should see "Hat" in the results
        And I should see "Apple" in the results
        And I should see "Hammer" in the results

    Scenario: Search by Category
        Given I am on the "Home Page"
        When I select "Food" from the "Category" dropdown
        And I click the "Search" button
        Then I should see "Apple" in the results
        And I should not see "Hat" in the results

    Scenario: Search by Availability
        Given I am on the "Home Page"
        When I select "True" from the "Available" dropdown
        And I click the "Search" button
        Then I should see "Hat" in the results
        And I should see "Apple" in the results
        And I should not see "Hammer" in the results

    Scenario: Search by Name
        Given I am on the "Home Page"
        When I set the "Name" to "Apple"
        And I click the "Search" button
        Then I should see "Apple" in the results
        And I should not see "Hat" in the results
