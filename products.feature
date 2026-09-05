Feature: The product catalog service back-end
    As a Product Catalog Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | category     | availability | price  |
        | Laptop     | electronics  | True         | 999.99 |
        | T-Shirt    | clothing     | True         | 19.99  |
        | Sofa       | furniture    | False        | 499.50 |
        | Headphones | electronics  | True         | 59.99  |

Scenario: Read a product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Laptop" in the "Name" field

Scenario: Update a product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    When I change "Name" to "Gaming Laptop"
    And I press the "Update" button
    Then I should see the message "Success"

Scenario: Delete a product
    When I visit the "Home Page"
    And I set the "Name" to "Sofa"
    And I press the "Search" button
    Then I should see the message "Success"
    When I press the "Delete" button
    Then I should see the message "Product has been Deleted!"

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "T-Shirt" in the results
    And I should see "Headphones" in the results

Scenario: Search products by name
    When I visit the "Home Page"
    And I set the "Name" to "Headphones"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Headphones" in the results
    And I should not see "Laptop" in the results

Scenario: Search products by category
    When I visit the "Home Page"
    And I select "electronics" in the "Category" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop" in the results
    And I should see "Headphones" in the results

Scenario: Search products by availability
    When I visit the "Home Page"
    And I select "False" in the "Availability" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Sofa" in the results
