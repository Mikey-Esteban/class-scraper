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
browser.goto "https://sutrapro.com/modega"
continue_story
data = Nokogiri::HTML(browser.html)

rows = data.css('div.card-list__card-group')
rows.each do | row |
    puts row.attr('class')
end

browser.close

print rows

CSV.open("modega.csv", "w") do |csv|
  csv << rows
end