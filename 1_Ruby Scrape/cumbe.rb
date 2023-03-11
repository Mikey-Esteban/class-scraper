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


@mbo_id = '16827'
browser = Watir::Browser.new :chrome
# continue_story
browser.goto "https://clients.mindbodyonline.com/classic/mainclass?studioid=#{@mbo_id}"
# continue_story
browser.goto "https://clients.mindbodyonline.com/classic/mainclass?studioid=#{@mbo_id}&fl=true&tabID=7"
continue_story
data = Nokogiri::HTML(browser.html)

even_rows = data.css('.evenRow')
odd_rows = data.css('.oddRow')

rows = data.xpath('//*[@id="classSchedule-mainTable"]/tbody/tr')
rows.each do | row |
    puts row.attr('class')
end

browser.close

print rows

CSV.open("cumbe.csv", "w") do |csv|
  csv << rows
end