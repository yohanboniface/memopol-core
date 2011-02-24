Feature: Basic lettuce tests

    Scenario: Homepage
        Given I access the url "/"
        Then I see the header "Memopol"

    Scenario: Country list
        Given I access the url "/countries"
        Then I see the header "Eurodéputés par pays"

    Scenario: Albert Dess
        Given I access the url "/mep/AlbertDess"
        Then I see the header "Albert DESS, eurodéputé"
