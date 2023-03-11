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
browser.goto "https://www.wny.nxgnstudios.com/class-schedules"
continue_story
data = Nokogiri::HTML(browser.html)

rows = data.css('.font_8')
rows.each do | row |
    puts row.attr('class')
end

browser.close

print rows

CSV.open("nxgn.csv", "w") do |csv|
  csv << rows
end