import re

from date_format_mappings import WN_FUNCTION_REGEX
from date_formatters import DATE_FORMATTERS_MAP
from date_functions import DATE_FUNCTION_MAP, get_date_format_regex, get_time_format_regex, get_full_format_regex, \
    EXCLUSION_MAP

from pypeg2 import List, attr, maybe_some, optional, parse, some


class DateParser:
    def __init__(self, settings):
        self.date_expression = get_date_format_regex(settings)
        self.time_expression = get_time_format_regex(settings)
        self.full_date_time_expression = get_full_format_regex(settings)
        self.settings = settings
        self.date_re = re.compile(self.date_expression, re.IGNORECASE)
        self.time_re = re.compile(self.time_expression, re.IGNORECASE)
        self.date_time_re = re.compile(self.full_date_time_expression, re.IGNORECASE)
        self.date_functions_re = re.compile(self._get_date_functions(), re.IGNORECASE)
        self.user_macros_re = re.compile(self._get_anniversaries(self.settings), re.IGNORECASE)
        self.operator_re = re.compile(r'[+-]')
        self.time_span_re = re.compile(r'[ymwdhMs]')
        self.time_digits_re = re.compile(r'[0-9]+')
        self.format_re = re.compile(r'[ymwdhMs]+|long')
        self.date_formatters_re = re.compile(self._get_date_formatters(), re.IGNORECASE)

        # This is for the exclusions
        # a whole word, so "xmon" typed without the keyword isn't read as "x mon"
        self.exclusion_keyword_re = re.compile(r'(?:exclude|ex|x)(?![a-z_])')
        self.exclusion_macro_re = re.compile(self._get_exclusion_macros(), re.IGNORECASE)
        self.exclusion_range_operator_re = re.compile(r'to|until', re.IGNORECASE)

        # The money shot
        self.parseable_date_re = re.compile(r'\"[^\"]+\"', re.IGNORECASE)

        # Week number calculation
        self.wn_command_re = WN_FUNCTION_REGEX

    @staticmethod
    def _get_anniversaries(settings):
        """
        This method gets the anniversaries from the settings
        file and builds them into a regex string for the
        parser. This allows us to accept user-defined
        anniversaries as macros.
        :param settings:
        """
        # Nothing complicated. We're just creating a | separated string
        # by looping through keys and joining them.
        # Those funny characters we're prepending to the string are so we
        # can match an options "^" which we use to denote an absolute macro
        # invocation:
        # mybirthday ====> returns the date of my next birthday
        # ^mybirthday ===> the date I was born
        # A name may not run on into more letters, so "bday" can't match the start of "bdaytwo".
        # With no anniversaries, (?!) matches nothing, where an empty pattern would match everything.
        return r'\^?(?:%s)(?![a-z_])' % ('|'.join(map(re.escape, settings['anniversaries'])) or '(?!)')

    @staticmethod
    def _get_date_formatters():
        """
        This method will get the list of defnined functions and build
        a regular expression from them so that they can be interpreted
        later on. Note that we escape the strings during concatenation
        so that we can use symbols like '*' for abbreviated keywords.
        :return: a regex string of allowable function names
        """
        return '|'.join(re.escape(str(x)) for x in DATE_FORMATTERS_MAP.keys())

    @staticmethod
    def _get_date_functions():
        # A name ending in a letter may not run on into more letters: "next mon" mustn't match the start of
        # "next month", nor "mum" the start of an anniversary called "mum_bday". Symbols are exempt, so "*wd" works.
        return '|'.join(re.escape(x) + ('(?![a-z_])' if x[-1].isalpha() else '') for x in DATE_FUNCTION_MAP)

    @staticmethod
    def _get_exclusion_macros():
        # a name may not run on into more letters, so "sat" can't match the start of "saturdays"
        return '|'.join(re.escape(x) + '(?![a-z_])' for x in EXCLUSION_MAP)

    def parse_command(self, command_string):
        class Operator(str):
            grammar = self.operator_re

        class TimeSpans(str):
            grammar = attr("amount", self.time_digits_re), attr("span", self.time_span_re)

        class Operand(str):
            grammar = attr("operator", Operator), attr("timeSpans", some(TimeSpans))

        class OperandList(List):
            grammar = maybe_some(Operand)

        class DateFormat(str):
            grammar = self.date_formatters_re

        class DateTime(str):
            grammar = [self.date_time_re, self.date_re, self.time_re, self.date_functions_re, self.user_macros_re,
                       self.parseable_date_re, self.wn_command_re]

        class Format(str):
            grammar = optional(self.format_re)

        class ExclusionKeyword(str):
            grammar = self.exclusion_keyword_re

        class ExclusionRange(str):
            grammar = attr("fromDateTime", DateTime), self.exclusion_range_operator_re, attr("toDateTime", DateTime)

        class ExclusionType(List):
            grammar = [attr("exclusionRange", ExclusionRange),
                       attr("exclusionDateTime", DateTime), attr("exclusionMacro", self.exclusion_macro_re)]

        class ExclusionList(List):
            grammar = some(ExclusionType)

        class ExclusionCommands(str):
            grammar = attr("exclusionKeyword", ExclusionKeyword), attr("exclusionList", ExclusionList)

        class Commands(str):
            grammar = [

                (attr("dateTime1", DateTime), attr("operandList1", OperandList), "-", attr("dateTime2", DateTime),
                 attr("operandList2", OperandList),
                 attr("format", Format)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("exclusionCommands", ExclusionCommands),
                 attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList),
                 attr("exclusionCommands", ExclusionCommands)),

                (attr("dateTime", DateTime), attr("dateFormat", DateFormat)),

                (attr("dateTime", DateTime), attr("operandList", OperandList))

            ]

        return parse(command_string, Commands)
