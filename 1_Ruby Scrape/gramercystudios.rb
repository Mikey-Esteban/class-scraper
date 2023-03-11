require 'nokogiri'
require 'open-uri'
require 'watir'
require 'io/console'
require 'csv'

def continue_story
  print "press any key"
  STDIN.getch
  print "            \r"
end

browser = Watir::Browser.new :chrome
# continue_story
browser.goto "https://www.gramercydancestudios.com/schedule"
continue_story
data = Nokogiri::HTML(browser.html)

rows = data.css('.sqs-block-content')
rows.each do | row |
    puts row.attr('class')
end

browser.close

print rows

CSV.open("gramercystudios.csv", "w") do |csv|
  csv << rows
end