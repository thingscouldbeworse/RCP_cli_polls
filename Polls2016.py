import calendar
import datetime
import urllib.request
import re
import sys

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

today = datetime.date.today()
one_day = datetime.timedelta(days=1)

yesterday = today - one_day
two_days_back = yesterday - one_day

get_today = calendar.day_name[today.weekday()] + ", " + calendar.month_name[today.month] + " " + str(today.day)
get_day = calendar.day_name[yesterday.weekday()] + ", " + calendar.month_name[yesterday.month] + " " + str(yesterday.day)
prev_get_day = calendar.day_name[two_days_back.weekday()] + ", " + calendar.month_name[two_days_back.month] + " " + str(two_days_back.day)


url_contents = str(urllib.request.urlopen("http://www.realclearpolitics.com/epolls/latest_polls/pres_general/").read())

if url_contents.find(get_today) < 0:  
    first_pos = url_contents.find(get_day)
    second_pos = url_contents.find(prev_get_day)
elif url_contents.find(get_today):
    first_pos = url_contents.find(get_today)
    second_pos = url_contents.find(get_day)

chunk = first_pos = url_contents[first_pos:second_pos]

pattern = re.compile('(<a .*?(Clinton \+[\d]{1,2}|Trump \+[\d]{1,2}))')

bits = re.findall( pattern, chunk )

index = 0

for bit in bits:


    if( index > 0):
        sys.stdout.write( " | " )

    new_bit = bit[0].replace( "http:", "" )
    new_bit = new_bit.replace( "https:", "" )
    pattern = re.compile( '([A-Z].*?:)' )
    election_type = re.findall( pattern, new_bit )
    if( election_type[0] == "General Election:" ):
    	election_type = "Gen"
    elif( not election_type[0][:-1] in us_state_abbrev ):
        election_type = election_type[0][:3]
    else:
    	election_type = us_state_abbrev.get(election_type[0][:-1])

    pattern = re.compile( '(class="lp-poll.*?</a>)' )
    bits = re.findall( pattern, bit [0] )
    poll_chunk = bits[0][20:]
    first_pos = poll_chunk.find(">")
    poll_chunk = poll_chunk[first_pos+1:-4]

    split_result = bit[1].split(" ")
    result = split_result[0][:2] + split_result[1]
    sys.stdout.write( election_type + " " + poll_chunk + ", " + result )

    index += 1

print()
