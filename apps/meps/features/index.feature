Feature: Basic lettuce tests

    Scenario: Homepage
        Given I access the url "/"
        Then I see the header "Memopol"

    Scenario: Country list
        Given I access the url "/meps/countries"
        Then I see the header "MEPs by country"

    Scenario: Albert Dess
        Given I access the url "/meps/mep/AlbertDess"
        Then I see the header "Albert DESS, member of the european parliament"
