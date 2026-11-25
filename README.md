## Date Calculator
Hello there!

I needed a bit of motivation to learn Python and Alfred workflows, so I thought I’d kill two horses with one bullet, so to speak.

This is a date calculator – kind of. It won’t tell you when you’ll win the lottery, but it will answer one or two _very simple_ questions about dates: how long until Christmas, what’s the date 20 working days from now, which week number are we in, that sort of thing.

### Contents
- [Requirements](#requirements) and [Installing](#installing)
- [Quick start](#quick-start)
- [Dates, times and names](#dates-times-and-names)
- [Adding and subtracting](#adding-and-subtracting)
- [Time between two dates](#time-between-two-dates)
- [Week numbers and other details](#week-numbers-and-other-details)
- [Exclusions](#exclusions)
- [Anniversaries](#anniversaries)
- [Settings](#settings)
- [Natural language](#natural-language)
- [Troubleshooting](#troubleshooting)
- [Checking changes](#checking-changes), [Credits](#credits), [Version history](#version-history), [License](#license)

### Requirements
- Alfred 6 with the Powerpack
- macOS 12 or later
- Python 3.8 or later at `/usr/bin/python3`, which comes with Apple's Command Line Tools. If they're missing, macOS offers to install them the first time the workflow runs.

### Installing
Download _DateCalculator.alfredworkflow_ from the [latest release](https://github.com/bbrown/Alfred-Workflows-DateCalculator/releases/latest), then double-click it to add it to Alfred. Earlier versions are on the [releases page](https://github.com/bbrown/Alfred-Workflows-DateCalculator/releases).

Or build the workflow file yourself from a clone of this repository, then double-click it:

    git archive --format=zip -o DateCalculator.alfredworkflow HEAD

### Quick start
Type **dcalc** followed by an expression. The examples below use the default date format, _dd.mm.yy_; you can [change it](#settings).

| Type this | To get |
|---|---|
| **dcalc now** | The current date and time |
| **dcalc 25.12.14 - 18.01.14** | The time between two dates |
| **dcalc christmas - today** | How long until Christmas |
| **dcalc today + 6d** | The date six days from now |
| **dcalc today + 20d x weekends** | The date 20 working days from now |
| **dcalc time + 6h 8M** | The time 6 hours 8 minutes from now |
| **dcalc today wn** | This week’s number |
| **dcalc next tue** | Next Tuesday’s date |
| **dcalc easter** | Next Easter Sunday |

The workflow reads the expression as you type, so you’ll see _. . ._ or messages such as _Invalid Command_ until it’s complete. Then it shows the result. Press Enter to copy the result and paste it into the app you were using.

Typing **date** on its own is a shortcut for **dcalc date**.

### Dates, times and names
Anywhere a date or time can go, you can use any of these.

**Dates and times you type.** These follow your [settings](#settings). With the defaults:

| Kind | Example |
|---|---|
| Date | **25.12.14** |
| Time | **14:35** |
| Date and time | **21.06.14@14:20** |

**Words and abbreviations:**

| Word | Short | Means |
|---|---|---|
| **today** or **date** | **\*** | Today’s date |
| **now** | **#** | The current date and time |
| **time** | **&** | The current time |
| **yesterday** | **<** | Yesterday’s date |
| **tomorrow** | **\>** | Tomorrow’s date |

So **dcalc \*+6d** is the date six days from now.

**Days of the week.** **next mon** to **next sun** give the coming Monday to Sunday, and **prev mon** to **prev sun** give the last one. On a Tuesday, **next tue** is a week away.

**Named dates.** Each of these gives the next one to come:

| Name | Date |
|---|---|
| **christmas** | Christmas Day |
| **easter** | Easter Sunday |
| **pancake day** | Shrove Tuesday |
| **lent** | Ash Wednesday, the start of Lent |
| **passover** | The first day of Passover |
| **mum** | Mothering Sunday (UK) |
| **mom** or **mutter** | Mother’s Day (US and Germany) |
| **mlk** | Martin Luther King Jr. Day |
| **start bst**, **end bst** | The start and end of British Summer Time |
| **next month** | The first day of next month |
| **start year**, **end year** | The first and last days of this year |

Christmas is one of the [anniversaries](#anniversaries), so you can change it, or add your own.

### Adding and subtracting
Add or take away amounts of time with **+** and **-**:

**dcalc today + 4d**

**dcalc 18.12.14 + 9w**

**dcalc time + 6h 8M**

**dcalc 14:35 + 6h**

The units are:

| Unit | Means |
|---|---|
| **y** | years |
| **m** | months |
| **w** | weeks |
| **d** | days |
| **h** | hours |
| **M** | minutes |
| **s** | seconds |

Note the capital **M** for minutes. Odd, I know, but the workflow has to tell it apart from **m** for months, and I figured minutes would see much less use. (They have for me.)

You can chain as many as you like:

**dcalc 18.12.12 + 5y 9d 3w - 2d + 1d 1w**

What does that mess do? It takes 18.12.12, adds 5 years, 9 days and 3 weeks, takes off 2 days, then adds 1 day and 1 week.

To skip weekends or other days while counting, see [Exclusions](#exclusions).

### Time between two dates
Subtract one date from another to get the time between them. The order doesn’t matter.

**dcalc 25.12.14 - 18.01.14** gives _11 months, 1 week_

**dcalc 21.06.14@14:20 - 23.01.12@09:21 long**

Add units at the end to choose how the answer is shown. With one unit you get a decimal; with several you get a breakdown:

| Type this | To get |
|---|---|
| **dcalc 25.12.14 - 18.01.14 w** | _48.71 weeks_ |
| **dcalc 25.12.14 - 18.01.14 y** | _0.93 years_ |
| **dcalc 25.12.14 - 18.01.14 wd** | _48 weeks, 5 days_ |
| **dcalc 25.12.14 - 18.01.14 ymwd** | _0 years, 11 months, 1 week, 0 days_ |
| **dcalc 25.12.14 - 18.01.14 long** | _0 years, 11 months, 7 days, 0 hours, 0 minutes, 0 seconds_ |

You can use any of the [units](#adding-and-subtracting), in any order. Without units, the answer leaves out anything that’s zero, and seconds. Personally, I always use _long_ because it’s the most precise.

### Week numbers and other details
Put one of these after a date to find out something about it instead:

| Add | To get | Example | Gives |
|---|---|---|---|
| **wn** or **!** | The ISO week number | **dcalc 25.12.14 wn** | _52_ |
| **wd** | The day of the week | **dcalc 25.12.14 wd** | _THU_ |
| **wdi** | The day of the week as a number, Monday being 1 | **dcalc 25.12.14 wdi** | _4_ |
| **iso** | The date and time in ISO 8601 format | **dcalc now iso** | |
| **sign** | The star sign, just for a laugh | **dcalc 25.12.14 sign** | _Capricorn_ |

These work after a calculation, too: **dcalc today + 100d wd**.

**wn** also works the other way round, finding the date for a week number:

**dcalc wn 2015 5**

gives the date in the fifth week of 2015 that falls on today’s day of the week. Add a day to choose a different one:

**dcalc wn 2015 5 sun**

Leave out the year for the current year: **dcalc wn 7**. And you can calculate with the result, if you can stand the syntax:

**dcalc wn 2015 6 tue +1d wd**

That’s the Tuesday of week 6 in 2015, plus 1 day, shown as a day of the week. Which is Wednesday, obviously :-)

### Exclusions
Added at the request of a friend. Say you have 20 days to finish a project:

**dcalc today + 20d**

But you don’t work weekends, so leave them out of the count:

**dcalc today + 20d exclude weekends**

And you won’t be working on your wife’s birthday, if you know what’s good for you:

**dcalc today + 20d exclude weekends 26.09.14**

Nor during that break you were planning in October:

**dcalc today + 20d exclude weekends 26.09.14 05.10.14 to 10.10.14**

Nor the day you’re having a wisdom tooth out:

**dcalc today + 20d exclude weekends 26.09.14 05.10.14 to 10.10.14 next wed**

After **exclude** (or **x** for short) you can list any mix of:

| Exclude | Example |
|---|---|
| A date | **26.09.14**, **next wed** |
| A range of dates | **05.10.14 to 10.10.14** |
| Weekends or weekdays | **weekends** or **wknd**, **weekdays** or **wkdy** |
| A day of the week | **tuesdays** or **tue** |
| Every day except one | **all except tuesdays** or **xtue** (**exsat**, **exsun** for the weekend days) |
| Every day except weekends or weekdays | **all except weekends** or **xwknd**, **all except weekdays** or **xwkdy** |

For example, **dcalc today + 20d x weekends tuesdays** is 20 days from now, not counting weekends and Tuesdays, and **dcalc today + 3d x all except tuesdays** is three Tuesdays from now.

Exclusions work when taking days away, too: **dcalc today - 20d x weekends** is 20 working days ago. They don’t work when subtracting one date from another.

### Anniversaries
Anniversaries are dates you name, then use like any other date. Using the name gives the next time it comes round; put **^** in front for the original date:

| Type this | To get |
|---|---|
| **dcalc wedding** | The next wedding anniversary |
| **dcalc wedding - today** | How long until it |
| **dcalc today - ^wedding** | How long you’ve been married |

The workflow starts with four: _christmas_, _alfred_ (Alfred’s birthday), _leap_ (a leap day) and _future_ (1 January 2072).

To add, change or delete one, first [set a date format](#settings) with a four-digit year, such as _dd.mm.yyyy_. Then:

| Type this | To |
|---|---|
| **dcalcset list add wedding 26.09.2014** | Add an anniversary |
| **dcalcset list edit wedding 27.09.2014** | Change its date |
| **dcalcset list delete wedding** | Delete it |

Names are letters and underscores, at least two of them. Instead of a date, you can use anything from [Dates, times and names](#dates-times-and-names), such as **today**.

**dcalcshow list** shows them all; type part of a name to narrow the list. On an entry:

| Press | To |
|---|---|
| ⌘-Enter | Calculate with the next anniversary |
| ⇧-Enter | Calculate with the original date |
| ⌥-Enter | Change it |
| ⌃-Enter | Delete it |

### Settings
Choose how dates and times are written, both when you type them and in results:

| Keyword | Choices |
|---|---|
| **dcalcset date format** | UK (_dd.mm.yy_), US (_mm.dd.yy_), each with _-_, _/_ or _._ and two- or four-digit years; _yyyy-mm-dd_; _yyyymmdd_; and _dd mmm yyyy_. The default is _dd.mm.yy_. |
| **dcalcset time format** | 24-hour (_14:35_), the default; 12-hour (_2:35PM_); and military (_1435_) |
| **dcalcset date and time format** | _date@time_, the default; _dateTtime_; _date at time_; _time on date_; and _DATE ==> date TIME ==> time_ |

Each list marks the current choice with a \*.

The same three settings are in Alfred Preferences: open the workflow and click _Configure Workflow_. Changing a setting in either place changes it in both.

I’d recommend the 24-hour format. It’s easier to type, because 12-hour times need AM and PM in capitals.

### Natural language
Surround a simple expression in double quotes, and something quite magical happens:

**dcalc "4 hours 8 minutes after 4pm"**

**dcalc "6 weeks and 4 days after next wednesday"**

**dcalc "1 day after tomorrow"**

Yup! A natural date language parser! You can even combine it with the usual syntax:

**dcalc "next friday" + 1d**

This is a little bit experimental, but I thought I’d throw it in for a bit of fun.

### Troubleshooting
- **No result for an expression you’re sure is right:** check the [settings](#settings). Dates have to be typed in the chosen format, so _25.12.14_ won’t work when the format is _mm/dd/yyyy_.
- **No result after a word:** leave a space between words. **today wd** works, **todaywd** doesn’t.
- **Can’t add an anniversary:** choose a date format with a four-digit year first.
- **That’s too far away:** an exclusion is skipping more days than the workflow will look through. Shorten the excluded range.

### Checking changes
If you change the code, run the two self-checks. They need nothing but Python:

    /usr/bin/python3 test_dates.py
    /usr/bin/python3 workflow.py

Alfred shows a copy of this README as the workflow's help, kept in `info.plist`. After editing the README, copy it there with:

    /usr/bin/python3 sync_readme.py

`test_dates.py` fails if the two copies differ.

### Credits
A list of things that made my first attempt at Python programming possible:
- Dean Jackson for his more-than-slightly awesome [Alfred Workflow framework](http://www.deanishe.net/alfred-workflow/), and for his ‘parse-as-you-type’ idea.
- The folk at [Jetbrains](http://www.jetbrains.com/pycharm/), for making programming, in any language, bearable.
- Gustavo Niemeyer for [Python-DateUtil](https://labix.org/python-dateutil).
- Volker Birk for [PyPEG](http://fdik.org/pyPEG/).
- Mike Taylor for [ParseDateTime](https://github.com/bear/parsedatetime).
- [Programming Praxis](http://programmingpraxis.com) for the Passover calculation.
- And finally, and by no means least – Mr Smirnoff for discovering how to bottle patience.

### Version history
**4.2** – The date, time and date‑and‑time formats are now in _Configure Workflow_ as well as the _dcalcset_ keywords. The _dcalcshow date format_ and _dcalcshow time format_ keywords are gone, because the lists mark the current choice with a \*. Formats chosen in an earlier version go back to the defaults, so pick them again once. Anniversaries are kept.

**4.1** – Bug fixes. Countdowns to holidays such as _easter - today_ are no longer a day short, decimal years and months are no longer too high, month counts no longer drift after a short month, the _s_ format shows seconds, and _next month_ works. Also fixed: week numbers around New Year, exclusions when a time is given, anniversaries whose names start with another name, and adding an anniversary overwriting one with the same name in different capitals. Exclusions are documented again and now work when taking days away, and Alfred's built-in help now matches this README. Needs Python 3.8 or later.

**4.0** – Updated for Alfred 6. The workflow now runs on Python 3, because macOS no longer includes Python 2.

**2.7** – Removed the exclude stuff. It wasn't very reliable and was very hard to explain. Also fixed a problem which caused incorrect date calculations if the input phrase was right at the end of the month. (Exclusions came back later; see [Exclusions](#exclusions).)

**2.4** – Bug fixes. Added abbreviations. Added functions for Pancake Day, Lent and Martin Luther King Day.

**2.3** – Bug fixes. Reworked the auto formatting. You can now apply exclusions to date calculations as well as timespan calculations. Added function to return the date when given a year, a week number and an optional day of the week.

**2.1** – Bug fixes. Made the default formatting a little bit more intelligent.

**2.0** – Refactoring. Added a natural date language parser. Added support for 12-hour clock. Added function to get date of the next passover.

**1.6** – Refactoring. Added exclusion functionality, and macros for _year start_ and _year end_. Changed the calls for days of the week: You now need to enter _next mon_ to get the date for next Monday, but you can also now type _prev mon_ to get the date for last Monday. Huzzah!
Increased the accuracy of the date intervals. If you select _y_ for the date format then you will get _11.5 years_. But if you select _ym_ then you get _11 years, 6 months_. Trust me, it’s better this way.

**1.5** – Refactoring. Rewrote the code for date subtraction arithmetic. Now it’s a lot more accurate, even when working with uneven months and weeks. Minor bug fixes.

**1.4** – Fixed bug that caused inaccuracies when calculating anniversaries. Refactored code to make it easier to add new date functions and date formatters. General tidy-up.

**1.3** – Adds extra formatting functions (day of week) and bug fixes.

**1.2** – An improvement to add user-defined macros.

**1.1** (01.07.2014) – Included a new anniversary list function, and the addition of the international date format (yyyy-mm-dd).

**1.0** (27.06.2014) – Included an improved date parser, added macros (days of week, christmas and easter) and a general tidy up. The symbol for getting the week number for a particular date has changed from ‘^’ to ‘!’ or ‘wn’. Why? Because I seemed to be struggling to find ‘^’ on the keyboard.

### License
Well, I guess the [MIT](http://opensource.org/licenses/MIT) one will do. :-)

The MIT License (MIT)
Copyright (c) 2014 MuppetGate Media

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
