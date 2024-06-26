from constants import (YR, MON, DAY, DEP, ARR, ROW, SEAT, FFN,
                       WINDOW, AISLE, MIDDLE, SA, SB, SC, SD, SE, SF)


def get_date(ticket: str) -> str:
    """Return the date of ticket 'ticket' in YYYYMMDD format.

    >>> get_date('20230915YYZYEG12F')
    '20230915'
    >>> get_date('20240915YYZYEG12F1236')
    '20240915'
    """

    return get_year(ticket) + get_month(ticket) + get_day(ticket)

def get_year(ticket: str) -> str:
    """Return the year of ticket 'ticket' in YYYY format.

    >>> get_year('20230915YYZYEG12F')
    '2023'
    >>> get_year('20240915YYZYEG12F1236')
    '2024'
    """

    return ticket[YR:YR + 4]


def get_month(ticket: str) -> str:
    """Return the month of ticket 'ticket' in MM format.

    >>> get_month('20230915YYZYEG12F')
    '09'
    >>> get_month('20241215YYZYEG12F1236')
    '12'
    """

    return ticket[MON:MON + 2]


def get_day(ticket: str) -> str:
    """Return the day of ticket 'ticket' in DD format.
    
    >>> get_day('20230915YYZYEG12F')
    '15'
    >>> get_day('20241215YYZYEG12F1236')
    '15'
    """

    return ticket[DAY:DAY + 2]


def get_departure(ticket: str) -> str:
    """Return the code of the departure airport of ticket 'ticket'.
    
    >>> get_departure('20230915YYZYEG12F')
    'YYZ'
    >>> get_departure('20241215YYZYEG12F1236')
    'YYZ'
    """

    return ticket[DEP:DEP + 3]


def get_arrival(ticket: str) -> str:
    """Return the code of the arrival airport of ticket 'ticket'.
    
    >>> get_arrival('20230915YYZYEG12F')
    'YEG'
    >>> get_arrival('20241215YYZYEG12F1236')
    'YEG'
    """

    return ticket[ARR:ARR + 3]


def get_row(ticket: str) -> int:
    """Return the row number of the ticket 'ticket'.
    
    >>> get_row('20230915YYZYEG12F')
    12
    >>> get_row('20241215YYZYEG12F1236')
    12
    """

    return int(ticket[ROW:ROW + 2])


def get_seat(ticket: str) -> str:
    """Return the seat in the row of the ticket 'ticket'.
    
    >>> get_seat('20230915YYZYEG12F')
    'F'
    >>> get_seat('20241215YYZYEG12F1236')
    'F'
    """

    return ticket[SEAT]


def get_ffn(ticket: str) -> str:
    """Return the frequent flyer number for the passenger the ticket 'ticket'
     belongs to. If there is no frequent flyer number, return '' instead.
    
    >>> get_ffn('20230915YYZYEG12F')
    ''
    >>> get_ffn('20241215YYZYEG12F1236')
    '1236'
    """

    return ticket[FFN:FFN + 4]


def visits_airport(ticket: str, airport: str) -> bool:
    """Return True if and only if either departure or arrival airport on
    ticket 'ticket' is the same as 'airport'.

    >>> visits_airport('20230915YYZYEG12F1236', 'YEG')
    True
    >>> visits_airport('20230915YEGYYZ12F1236', 'YEG')
    True
    >>> visits_airport('20230915YYZYEG12F1236', 'YVR')
    False
    """

    return airport in (get_arrival(ticket), get_departure(ticket))


def connecting(ticket1: str, ticket2: str) -> bool:
    """Return True if and only if the first flight, found in 'ticket1', arrives
     in the same airport as the departure point of the second flight,
     found in 'ticket2', and the two flights are on the same dates.
    
    Precondition: 'ticket1' and 'ticket2' are in valid format.
    
    >>> connecting('20230915YYZYEG12F1236', '20230915YEGJFK42F1236')
    True
    >>> connecting('20230915YYZYEG12F1236', '20231015YEGJFK42F1236')
    False
    >>> connecting('20230915YYZYEG12F1236', '20230915JFKATL12F1236')
    False
    """

    return ((get_arrival(ticket1) == get_departure(ticket2))
            and (get_date(ticket1) == get_date(ticket2)))


def get_seat_type(ticket: str) -> str:
    """Return WINDOW, AISLE, or MIDDLE depending on the type of seat in
    ticket 'ticket'.

    Precondition: 'ticket' is a valid ticket.

    >>> get_seat_type('20230915YYZYEG12F1236')
    'window'
    >>> get_seat_type('20230915YYZYEG08B')
    'middle'
    >>> get_seat_type('20230915YYZYEG12C1236')
    'aisle'
    """
    if get_seat(ticket) in (SA, SF):
        return WINDOW
    if get_seat(ticket) in (SB, SE):
        return MIDDLE
    if get_seat(ticket) in (SC, SD):
        return AISLE

    return 'Not a valid seat.'


def is_valid_seat(ticket: str, first_row: int, last_row: int) -> bool:
    """Return True if and only if this ticket has a valid seat. That is,
    if the seat row is between 'first_row' and 'last_row', inclusive,
    and the seat is SA, SB, SC, SD, SE, or SF.

    Precondition: 'ticket' is in valid format.

    >>> is_valid_seat('20230915YYZYEG12F1236', 1, 30)
    True
    >>> is_valid_seat('20230915YYZYEG42F1236', 1, 30)
    False
    >>> is_valid_seat('20230915YYZYEG21Q1236', 1, 30)
    False
    """

    return (first_row <= int(get_row(ticket)) <= last_row
            and get_seat(ticket) in (SA, SB, SC, SD, SE, SF)
            and is_valid_ticket_format(ticket))


def is_valid_ffn(ticket: str) -> bool:
    """Return True if and only if the frequent flyer number 
    of the ticket 'ticket' is valid. That is if the sum of the first three
    digits modulo 10 must be the same as the last (fourth) digit.
    The empty string '' is also a valid ffn.
    
    Precondition: 'ticket' is a valid ticket.
    
    >>> is_valid_ffn('20231221YYZYEG25F4442')
    True
    >>> is_valid_ffn('20231221YYZYEG25F3924')
    True
    >>> is_valid_ffn('20231221YYZYEG25F')
    True
    >>> is_valid_ffn('20231221YYZYEG25F8133')
    False
    """

    valid = is_valid_ticket_format(ticket)

    total_sum = 0
    for digit in ticket[FFN:FFN + 3]:
        total_sum = total_sum + int(digit)

    if get_ffn(ticket) == "" and valid:
        return True
    if total_sum % 10 == int(ticket[FFN + 3]) and valid:
        return True

    return False


def leap_year_check(year: int) -> bool:
    """Return true if and only if the entered year 'year' is a leap year, if not
    return false.

    >>> leap_year_check(2024)
    True
    >>> leap_year_check(2000)
    True
    >>> leap_year_check(2100)
    False
    >>> leap_year_check(2005)
    False
    """

    if (year % 400) == 0:
        return True
    if (year % 4) == 0 and (year % 100) != 0:
        return True

    return False


def is_valid_date(ticket: str) -> bool:
    """Return true if and only if the date on the ticket, 'ticket',
    is a valid date. That is if the days of months January, March, May, July,   
    August, October and December satisfy the range of 1-31 days, the days of
    months April, June, September, and November satisfy the range of 1-30 days,
    and if the days in February satisfy the range of 1-28 days (unless it is a 
    leap year, in which case days must satisfy the range of 1-29 days).
    
    Precondition: 'ticket' is a valid ticket.
    
    >>> is_valid_date('20240229YYZYEG25F4442')
    True
    >>> is_valid_date('20000229YYZYEG25F4442')
    True
    >>> is_valid_date('21000229YYZYEG25F4442')
    False
    >>> is_valid_date('20230217YYZYEG25F4442')
    True
    >>> is_valid_date('20230832YYZYEG25F4442')
    False
    >>> is_valid_date('20230631YYZYEG25F4442')
    False
    """

    month = get_month(ticket)
    year = int(get_year(ticket))
    day = int(get_day(ticket))
    valid = is_valid_ticket_format(ticket)

    if month == '02' and valid:
        if leap_year_check(year):
            return day in range(1, 30)

        return day in range(1, 29)

    if int(month) in (1, 3, 5, 7, 8, 10, 12) and valid:
        return day in range(1, 32)

    if int(month) in (4, 6, 9, 11) and valid:
        return day in range(1, 31)

    return False


def is_valid_ticket(ticket: str, first_row: int, last_row: int) -> bool:
    """Return True if and only if this ticket is valid. That is,
    if the seat row is between 'first row' and 'last_row', inclusive,
    the seat is SA, SB, SC, SD, SE, or SF,
    the sum of the first three digits (of the FFN) modulo 10 must be the same as
    the last (fourth) digit (of the FFN), and the ticket 'ticket' is in 
    valid form.
    
    Precondition: 'ticket' is a valid ticket.

    >>> is_valid_ticket('20230631YYZYEG25F4442', 1, 30)
    False
    >>> is_valid_ticket('20000229YYZYEG16B4442', 1, 30)
    True
    >>> is_valid_ticket('20231221YYZYEG25A', 1, 30)
    True
    >>> is_valid_ticket('20000229YYZYEG12H1236', 1, 30)
    False
    >>> is_valid_ticket('20000229YYZYYZ16B4442', 1, 30)
    False
    """

    return (is_valid_ticket_format(ticket)
            and is_valid_date(ticket)
            and is_valid_ffn(ticket)
            and is_valid_seat(ticket, first_row, last_row)
            and get_departure(ticket) != get_arrival(ticket))


def adjacent(ticket1: str, ticket2: str) -> bool:
    """Return True if any only if the seats in tickets 'ticket1' and
    'ticket2' are adjacent. Seats across an aisle are not considered 
    to be adjacent.

    Precondition: ticket1 and ticket2 are valid tickets.

    >>> adjacent('20230915YYZYEG12D1236', '20230915YYZYEG12E1236')
    True
    >>> adjacent('20230915YYZYEG12B1236', '20230915YYZYEG12A1236')
    True
    >>> adjacent('20230915YYZYEG12C1236', '20230915YYZYEG12D1236')
    False
    >>> adjacent('20230915YYZYEG12A1236', '20230915YYZYEG11B1236')
    False
    """

    seat1 = get_seat(ticket1)
    seat2 = get_seat(ticket2)

    if get_row(ticket1) == get_row(ticket2):
        return ((seat1 in (SA, SC) and seat2 == SB)
                or (seat1 == SB and seat2 in (SA, SC))
                or (seat1 in (SD, SF) and seat2 == SE)
                or (seat1 == SE and seat2 in (SD, SF)))

    return False


def behind(ticket1: str, ticket2: str) -> bool:
    """Return true if and only if if the seats in tickets 'ticket1' 
    and 'ticket2' are directly behind another.
    
    Precondition: ticket1 and ticket2 are valid tickets.
    
    >>> behind('20230915YYZYEG12D1236', '20230915YYZYEG13E1236')
    False
    >>> behind('20230915YYZYEG12B1236', '20230915YYZYEG11B1236')
    True
    >>> behind('20230915YYZYEG10B1236', '20230915YYZYEG02C1236')
    False
    """

    return (get_seat(ticket1) == get_seat(ticket2)
            and (int(get_row(ticket1))
                 in (int(get_row(ticket2)) - 1, int(get_row(ticket2)) + 1)))


def change_seat(ticket: str, rownum: str, seat: str) -> str:
    """Return the input ticket 'ticket' with the newly assigned
    row number 'rownum' and seat 'seat'. All other aspects of
    the input ticket remains unchanged.
    
    Precondition: ticket, rownum, and seat are all valid.
    
    >>> change_seat('20230915YYZYEG12B1236', '10', 'A')
    '20230915YYZYEG10A1236'
    >>> change_seat('20231221YYZYEG25F', '15', 'C')
    '20231221YYZYEG15C'
    >>> change_seat('20231221YYZYEG25F3924', '25', 'F')
    '20231221YYZYEG25F3924'
    """

    part_ticket1 = ticket[YR:ARR + 3]
    part_ticket2 = ticket[FFN:FFN + 4]

    return part_ticket1 + rownum + seat + part_ticket2


def change_date(ticket: str, day: str, mon: str, yr: str) -> str:
    """The first parameter represents the ticket. The second parameter
     represents the day. The third parameter represents the months. The last
     parameter represents the year. The function should return a new ticket
     that is in the same format as the input ticket, has the same departure,
     arrival, seat information, and frequent flyer number as the input
     ticket, and has a new date. You may assume the ticket and the new
     date information are valid. 
    
    >>> change_date('20230915YYZYEG12B1236', '15', '12', '2005')
    '20051215YYZYEG12B1236'
    >>> change_date('20231221YYZYEG25F', '21', '08', '1976')
    '19760821YYZYEG25F'
    >>> change_date('20241020YYZYEG12C1236', '17', '01', '2192')
    '21920117YYZYEG12C1236'
    """

    part_ticket = ticket[DEP:FFN + 4]

    return yr + mon + day + part_ticket


def is_valid_ticket_format(ticket: str) -> bool:
    """Return True if and only if ticket 'ticket' is in valid format:

    - year is 4 digits
    - months is 2 digits
    - day is 2 digits
    - departure is 3 letters
    - arrival is 3 letters
    - row is 2 digits
    - seat is a characters
    - frequent flyer number is either empty or 4 digits, and
      it is the last record in 'ticket'

    >>> is_valid_ticket_format('20241020YYZYEG12C1236')
    True
    >>> is_valid_ticket_format('20241020YYZYEG12C12361236')
    False
    >>> is_valid_ticket_format('ABC41020YYZYEG12C1236')
    False
    """

    return (FFN == 17
            and (len(ticket) == 17
                 or len(ticket) == 21 and ticket[FFN:FFN + 4].isdigit())
            and ticket[YR:YR + 4].isdigit()
            and ticket[MON:MON + 2].isdigit()
            and ticket[DAY:DAY + 2].isdigit()
            and ticket[DEP:DEP + 3].isalpha()
            and ticket[ARR:ARR + 3].isalpha()
            and ticket[ROW:ROW + 2].isdigit()
            and ticket[SEAT].isalpha())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
