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
browser.goto "https://app.glofox.com/portal/#/branch/602aab1088ec83092e2e83f1/classes-day-view"
continue_story
data = Nokogiri::HTML(browser.html)

rows = data.css('.list-text-left')
rows.each do | row |
    puts row.attr('class')
end

rows2 = data.css('.list-text-right')
rows2.each do | row |
    puts row.attr('class')
end

browser.close

print rows

CSV.open("pmt.csv", "w") do |csv|
  csv << rows
  csv << rows2
end