## Date Calculator cookbook
Worked examples of the calculations Date Calculator can do, with the reasoning behind each one. The [README](README.md) is the full reference; this is the "how do I…?" companion.

Each example shows what you type in Alfred, then the answer after **→**. Press Enter on an answer to copy it and paste it into the app you were using. An answer starting _error:_ is the message Alfred shows instead, which Enter doesn't copy.

The answers assume:

- **The default settings:** dates written _dd.mm.yy_, 24-hour times, and _@_ between a date and a time. A few examples use other settings, and say so.
- **The clock:** Thursday 26 November 2026, 14:30, in UTC. On another day you'll get other answers, worked out the same way.
- **A birthday saved as the anniversary _bday_:** 15 March 1990.

### Contents
- [Today, now and the time](#today-now-and-the-time)
- [Adding and taking away time](#adding-and-taking-away-time)
- [Time between two dates](#time-between-two-dates)
- [Working days](#working-days)
- [Holidays and other named dates](#holidays-and-other-named-dates)
- [Birthdays and anniversaries](#birthdays-and-anniversaries)
- [Week numbers](#week-numbers)
- [Finding out about a date](#finding-out-about-a-date)
- [Unix time](#unix-time)
- [Plain English](#plain-english)
- [Other date and time formats](#other-date-and-time-formats)
- [When it says no](#when-it-says-no)
- [Just for fun](#just-for-fun)
- [Keeping this cookbook right](#keeping-this-cookbook-right)

### Today, now and the time
Each word has a one-character short form: **\*** for today (or _date_), **#** for now, **&** for the time, **<** for yesterday and **>** for tomorrow. Short forms don't need spaces around them.

```dcalc
dcalc today
→ 26.11.26
dcalc now
→ 26.11.26@14:30
dcalc time
→ 14:30
dcalc <
→ 25.11.26
dcalc >
→ 27.11.26
dcalc *+6d
→ 02.12.26
dcalc & + 1h
→ 15:30
```

A date you type, or a word like _today_, means midnight at the start of that day. A time on its own means that time today.

### Adding and taking away time
#### Days, weeks, months and years
Units are single letters: **y** years, **m** months, **w** weeks, **d** days, **h** hours, **M** minutes, **s** seconds. Mind the capital **M** for minutes.

```dcalc
dcalc today + 30d
→ 26.12.26
dcalc today + 6w
→ 07.01.27
dcalc today + 18m
→ 26.05.28
dcalc 25.12.26 - 1y
→ 25.12.25
```

#### Several units at once
Put units side by side, and switch between **+** and **-** as often as you like.

```dcalc
dcalc today + 1y 2m 3w 4d
→ 20.02.28
dcalc today + 1m - 1d
→ 25.12.26
```

#### Words instead of letters
If you can't remember which **m** is which, use words: **year** or **yr**, **month** or **mo**, **week** or **wk**, **day**, **hour** or **hr**, **minute** or **min**, **second** or **sec**. They can be plural or not, in any case, with or without a space.

```dcalc
dcalc time + 90min
→ 16:00
dcalc today + 2 weeks 3 days
→ 13.12.26
dcalc today + 1 Year
→ 26.11.27
```

#### Hours and minutes
A time that goes past midnight gets its date, so you can tell it's another day.

```dcalc
dcalc now + 45M
→ 26.11.26@15:15
dcalc 09:00 + 7h 30M
→ 16:30
dcalc 22:30 + 3h
→ 27.11.26@01:30
dcalc 25.12.26@18:00 + 90min
→ 25.12.26@19:30
```

#### Month ends and leap days
A month after 31 January would be 31 February, so you get the last day of February instead. That makes month sums one-way: taking the month off again doesn't get you back to the 31st. Leap days work the same way.

```dcalc
dcalc 31.01.26 + 1m
→ 28.02.26
dcalc 31.01.26 + 1m - 1m
→ 28.01.26
dcalc 29.02.28 + 1y
→ 28.02.29
dcalc 29.02.28 + 4y
→ 29.02.32
```

#### The order of units can matter
Units are added in the order you type them. Usually that makes no difference, but near a month end it can.

```dcalc
dcalc 30.01.26 + 1d 1m
→ 28.02.26
dcalc 30.01.26 + 1m 1d
→ 01.03.26
```

The first adds a day to get 31 January, then a month, which lands on the last day of February. The second adds a month to get 28 February, then a day.

### Time between two dates
#### How long until something
Subtract one date from the other. The order doesn't matter.

```dcalc
dcalc christmas - today
→ 4 weeks, 1 day
dcalc today - christmas
→ 4 weeks, 1 day
dcalc christmas - now
→ 4 weeks, 9 hours, 30 minutes
```

Christmas on its own means the start of Christmas Day, so _christmas - now_ counts to Christmas morning.

#### In the units you want
Add unit letters after the second date. One unit gives a decimal; several give a breakdown. Without units you get everything that isn't zero, except seconds. **long** lists every unit down to seconds, zeros included, in days rather than weeks.

```dcalc
dcalc christmas - today d
→ 29 days
dcalc christmas - today w
→ 4.14 weeks
dcalc christmas - today wd
→ 4 weeks, 1 day
dcalc 25.12.26 - 18.01.14 ymwd
→ 12 years, 11 months, 1 week, 0 days
dcalc 25.12.26 - 18.01.14 y
→ 12.93 years
dcalc 25.12.26 - 18.01.14 long
→ 12 years, 11 months, 7 days, 0 hours, 0 minutes, 0 seconds
```

Decimals use the real length of each year and month: 0.93 years is 341 days out of 365.

#### Hours and minutes between two times
```dcalc
dcalc 17:30 - 09:00
→ 8 hours, 30 minutes
dcalc 17:30 - 09:00 h
→ 8.5 hours
dcalc 17:30 - 09:00 M
→ 510 minutes
dcalc 17:00 - now
→ 2 hours, 30 minutes
dcalc tomorrow - now s
→ 34200 seconds
```

#### Across midnight
Two times on their own are both today, so a night shift from 22:00 to 06:00 comes out as 16 hours. Move the end to tomorrow with **+ 1d**:

```dcalc
dcalc 06:00 - 22:00
→ 16 hours
dcalc 06:00 + 1d - 22:00
→ 8 hours
```

#### Calculating on either side
Either date can have units added or taken away before the subtraction.

```dcalc
dcalc christmas + 1d - today
→ 1 month
dcalc next month - 1d - today
→ 4 days
```

Boxing Day is exactly a calendar month after 26 November, so the first answer is in months, where Christmas Day, one day short of a month, came out in weeks.

### Working days
Add **x** (or **exclude**) and a list of days to leave out of the count.

#### Working days from today
```dcalc
dcalc today + 10d x weekends
→ 10.12.26
dcalc today + 10d exclude weekends
→ 10.12.26
dcalc today - 10d x weekends
→ 12.11.26
```

The count starts the day after today and skips every Saturday and Sunday, so the answer is the 10th weekday after (or before) today.

#### Working days between two dates
```dcalc
dcalc christmas - today x weekends
→ 21 days
```

This counts the days after the first date, up to and including the second, that aren't left out. So it undoes the sum above: 10 working days after today is 10.12.26, and from today to then is 10 working days.

```dcalc
dcalc 10.12.26 - today x weekends
→ 10 days
```

Working days always come out in days, so units after the list are a mistake (see [When it says no](#when-it-says-no)).

#### Leaving out holidays, too
Mix weekdays, dates, names and ranges in one list. Leaving out Christmas Day and the bank holiday on 28 December moves the 22nd working day two days later. A range, with **to** or **until**, includes both its ends.

```dcalc
dcalc today + 22d x weekends
→ 28.12.26
dcalc today + 22d x weekends christmas 28.12.26
→ 30.12.26
dcalc today + 20d x weekends 24.12.26 to 01.01.27
→ 04.01.27
dcalc today + 20d x weekends 24.12.26 until 01.01.27
→ 04.01.27
dcalc christmas - today x weekends 24.12.26
→ 20 days
```

#### Leaving out particular weekdays
Name days of the week in the plural or by their first three letters: **fridays** or **fri**. **weekends** (**wknd**) and **weekdays** (**wkdy**) cover several at once. **all except tuesdays**, or **xtue** for short, leaves out every day but Tuesday, so it counts Tuesdays. For the weekend days the short forms are **exsat** and **exsun**.

```dcalc
dcalc today + 10d x fridays weekends
→ 15.12.26
dcalc today + 3d x all except tuesdays
→ 15.12.26
dcalc today + 3d x xtue
→ 15.12.26
```

### Holidays and other named dates
Each name gives the next one to come. Today's doesn't count, so on Thanksgiving, _thanksgiving_ is next year's. Add a year for the one in that year.

```dcalc
dcalc easter
→ 28.03.27
dcalc easter - today d
→ 122 days
dcalc easter 2030
→ 21.04.30
dcalc thanksgiving
→ 25.11.27
dcalc thanksgiving 2026
→ 26.11.26
```

The other named dates, in order: Shrove Tuesday, Ash Wednesday, Mothering Sunday (UK), Mother's Day (US and Germany, as _mom_ or _mutter_), the first day of Passover, Martin Luther King Jr. Day, the start and end of British Summer Time and of US daylight saving time, and the next Friday the 13th. A year works after any of them.

```dcalc
dcalc pancake day
→ 09.02.27
dcalc lent
→ 10.02.27
dcalc mum
→ 07.03.27
dcalc mom
→ 09.05.27
dcalc mutter
→ 09.05.27
dcalc passover
→ 22.04.27
dcalc mlk
→ 18.01.27
dcalc start bst
→ 28.03.27
dcalc end bst
→ 31.10.27
dcalc start dst
→ 14.03.27
dcalc end dst
→ 07.11.27
dcalc friday 13
→ 13.08.27
```

#### Next and previous weekdays
_next_ is the coming one, a week away if it's today. _prev_ is the last one, a week ago if it's today.

```dcalc
dcalc next fri
→ 27.11.26
dcalc next thu
→ 03.12.26
dcalc prev mon
→ 23.11.26
```

#### Month and year boundaries
There's no name for the end of this month, but the day before next month is the same thing. Likewise, a year after the start of this year is next New Year's Day.

```dcalc
dcalc next month
→ 01.12.26
dcalc next month - 1d
→ 30.11.26
dcalc start year
→ 01.01.26
dcalc end year
→ 31.12.26
dcalc start year + 1y
→ 01.01.27
dcalc end year - today d
→ 35 days
```

### Birthdays and anniversaries
An anniversary's name gives the next time it comes round. With **^** in front it's the original date, and with a year after it, the one in that year.

```dcalc
dcalc bday
→ 15.03.27
dcalc ^bday
→ 15.03.90
dcalc bday 2030
→ 15.03.30
dcalc bday - today d
→ 109 days
dcalc today - ^bday ymd
→ 36 years, 8 months, 11 days
dcalc today - ^bday y
→ 36.7 years
```

#### Saving one
Saving needs a date format with a four-digit year, so these examples use _dd.mm.yyyy_. Names are letters and underscores, at least two of them. **dcalcshow list** shows the ones you've saved.

```dcalc date-format=dd.mm.yyyy
dcalcset list add wedding 26.09.2014
→ wedding added
dcalc wedding
→ 26.09.2027
dcalc today - ^wedding ym
→ 12 years, 2 months
dcalcset list edit wedding 27.09.2014
→ wedding changed
dcalcset list delete wedding
→ wedding deleted
dcalc wedding
→ error: Invalid Command
```

Once it's deleted, _wedding_ isn't a name any more, so it's an invalid command.

### Week numbers
**wn** (or **!**) after a date gives its ISO week number. Weeks start on Monday, and week 1 is the one with the year's first Thursday, so the first days of January can be in the last week of the year before.

```dcalc
dcalc today wn
→ 48
dcalc christmas !
→ 52
dcalc 01.01.27 wn
→ 53
```

Put **wn** first to go the other way, from a week number to a date: the same weekday as today, unless you name one. Leave out the year for this year.

```dcalc
dcalc wn 2027 1
→ 07.01.27
dcalc wn 2027 1 mon
→ 04.01.27
dcalc wn 10
→ 05.03.26
dcalc wn 2026 53 fri
→ 01.01.27
```

### Finding out about a date
Put one of these after any date or sum.

```dcalc
dcalc christmas wd
→ FRI
dcalc christmas wdi
→ 5
dcalc christmas doy
→ 359
dcalc today + 100d wd
→ SAT
dcalc now iso
→ 2026-11-26T14:30:00
dcalc christmas iso
→ 2026-12-25T00:00:00
```

**wd** is the day of the week, **wdi** the same as a number (Monday is 1), and **doy** the day of the year.

#### Signs, animals, the moon and the year
**sign** and **zodiac** are the same thing. **animal** goes by the calendar year, so it's wrong for dates in January and February before Chinese New Year. **moon** is right to within a day or so. **progress** shows how much of the year has gone.

```dcalc
dcalc ^bday zodiac
→ Pisces
dcalc ^bday animal
→ Horse
dcalc ^bday moon
→ 🌖 Waning gibbous
dcalc * zodiac
→ Sagittarius
dcalc today progress
→ ▓▓▓▓▓▓▓▓▓░ 90%
```

### Unix time
**@** and a Unix time gives its date and time where you are; **unix** turns any answer into one. The answers here are for UTC.

```dcalc
dcalc now unix
→ 1795703400
dcalc @1800000000
→ 15.01.27@08:00
dcalc @1800000000 - now
→ 1 month, 2 weeks, 5 days, 17 hours, 30 minutes
dcalc @0 + 1d unix
→ 86400
```

### Plain English
Put a phrase in double quotes and a natural language parser reads it. You can calculate with the result like any other date.

```dcalc
dcalc "4 hours 8 minutes after 4pm"
→ 20:08
dcalc "6 weeks and 4 days after next wednesday"
→ 17.01.27
dcalc "tomorrow at noon" - now
→ 21 hours, 30 minutes
dcalc "in 3 days" wd
→ SUN
```

The parser has its own rules: _"next friday"_ is the Friday of next week, while _"friday"_, like _next fri_, is the coming one.

```dcalc
dcalc "next friday"
→ 04.12.26
dcalc "friday"
→ 27.11.26
```

Every word has to be one it understands. It doesn't know Christmas, so rather than guess, it says so:

```dcalc
dcalc "3 days after christmas"
→ error: Invalid Date/time
dcalc christmas + 3d
→ 28.12.26
```

### Other date and time formats
Type dates and times the way your settings show them; the README's [Settings](README.md#settings) section lists the choices. With the 12-hour format, AM and PM can be in either case, and the minutes can be left off on the hour:

```dcalc time-format=12-hour
dcalc 4pm + 90min
→ 05:30PM
dcalc 9am - 5:30pm
→ 8 hours, 30 minutes
dcalc now
→ 26.11.26@02:30PM
```

With ISO-style dates and a **T** between date and time:

```dcalc date-format=yyyy-mm-dd date-time-format=T
dcalc 2026-12-25T09:00 - now
→ 4 weeks, 18 hours, 30 minutes
dcalc today + 1w
→ 2026-12-03
```

With military time:

```dcalc time-format=Military
dcalc 0900 + 8h 30M
→ 1730
```

### When it says no
While you type, Alfred shows _Invalid Command_ until the expression is complete. If it still says so at the end, one of these is the usual reason.

Words need a space between them:

```dcalc
dcalc todaywd
→ error: Invalid Command
dcalc today wd
→ THU
```

A date has to be in your format, here with a two-digit year, and it has to exist:

```dcalc
dcalc 25.12.2026
→ error: Invalid Command
dcalc 31.02.26
→ error: Invalid Date/time
```

A year can only follow a name that comes round every year, and the date has to exist in that year:

```dcalc
dcalc next month 2030
→ error: Invalid Command
dcalc leap 2027
→ error: Invalid Date/time
```

Units have to be ones it knows, and working days don't take units:

```dcalc
dcalc today + 5 dayz
→ error: Invalid Command
dcalc christmas - today x weekends w
→ error: Invalid Command
```

Leaving out every day leaves nothing to count:

```dcalc
dcalc today + 1d x weekdays weekends
→ error: All days excluded
```

### Just for fun
```dcalc
dcalc ^bday + 10000d
→ 31.07.17
dcalc ^bday + 1000000000s iso
→ 2021-11-21T01:46:40
dcalc ^bday wd
→ THU
dcalc friday 13 - today d
→ 260 days
dcalc @2147483647
→ 19.01.38@03:14
```

That's the day you were 10,000 days old, the second you were a billion seconds old (counting from the midnight you were born), the day of the week you were born, the wait for the next Friday the 13th, and the moment 32-bit Unix clocks run out.

### Keeping this cookbook right
`test_dates.py` runs every example in this file and fails if an answer changes, so the cookbook can't drift from what the workflow does. Run it with `/usr/bin/python3 test_dates.py`.

It reads each code block marked `dcalc`, sets the clock, time zone and birthday given at the top, and checks each `dcalc` or `dcalcset list` line against the **→** line after it. An error is written _error:_ and its message. A block's own settings go after `dcalc` on its first line, such as `dcalc time-format=12-hour`, and its anniversaries start afresh, so a block's `dcalcset list` lines only affect that block.

To add an example, put it in a `dcalc` block with the answer you expect, and run the check. Every fenced code block here has to be a `dcalc` block, so an example can't be left out of the check by mistake.
