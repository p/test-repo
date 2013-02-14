require 'capybara'
require 'capybara/dsl'
require 'capybara/poltergeist'
require 'test/unit'

Capybara.default_driver = :poltergeist

#Capybara.configure do |config|
  #config.default_driver = :poltergeist
#end

class TestCase < Test::Unit::TestCase
  include Capybara::DSL
  
  def teardown
    Capybara.reset_sessions!
    Capybara.use_default_driver
  end
end

class OneTest < TestCase
  def test_foo
    puts 'Visiting'
    visit 'http://localhost/'
    puts 'Asserting'
    assert true
    puts 'Done'
  end
end
