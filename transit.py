import sys
import re
from datetime import datetime
import datetime as dt
import unittest


class Entry:
    # Initialization. Options for: Entry, Exit, Average
    def __init__(self, a_dict):
        # Class properties
        self.error_messages = {}
        self.card_number = a_dict['card_number'] if 'card_number' in a_dict else ''
        self.station_in = a_dict['station_in'] if 'station_in' in a_dict else ''
        self.station_out = a_dict['station_out'] if 'station_out' in a_dict else ''
        self.swipe_in = a_dict['swipe_in'] if 'swipe_in' in a_dict else ''
        self.swipe_out = a_dict['swipe_out'] if 'swipe_out' in a_dict else ''
        self.average_transit = a_dict['average_transit'] if 'average_transit' in a_dict else ''
        self.transit_stations = a_dict['transit_stations'] if 'transit_stations' in a_dict else []
        self.entry_complete = False  # We set to True if the entry contains in and out

        # Run Validation
        self.validate_entry()

    # Validatation
    def validate_entry(self):
        # Validates card number. Number only
        if self.card_number and not self.card_number.isdigit():
            self.error_messages['card_number'] = "Invalid card number!"
            return False
        # Validates station name. It shouldn't be a number
        if self.station_in and self.station_in.isdigit():
            self.error_messages['station_in'] = "Should be a valid station name"
            return False
        if self.station_out and self.station_out.isdigit():
            self.error_messages['station_out'] = "Should be a valid station name"
            return False
        # Validates date and time
        if self.swipe_in and not self.is_validatetime(self.swipe_in):
            self.error_messages['swipe_in'] = "Invalid entry time!"
            return False
        if self.swipe_out and not self.is_validatetime(self.swipe_out):
            self.error_messages['swipe_out'] = "Invalid entry time!"
            return False

        return True

    # Display error messages
    def display_error_message(self):
        # Error message(s) numbering

        # Adds 's' as a plural form if there are more than 1 error
        pluralize = 's' if len(self.error_messages) > 1 else ''

        print(f"\nError{pluralize} found:")
        for key, value in self.error_messages.items():
            print(f"({key}): {value}")

    # Check if datetime is valid. Returns either True/False
    def is_validatetime(self, _date):
        try:
            datetime.strptime(_date, '%Y/%m/%d %H:%M:%S')
            return True
        except ValueError:
            return False

# Cleaned user input.Remove whitespace
def cleaned_input(user_input):
    return user_input.replace(" ", "")

# Remove leading/trailing whitespace and multiple whitespace
def cleaned_input_time(_time):
    return re.sub(' +', ' ', _time.strip())

# Accepts the user entry inputs and return as dict
def transit_entry(entry_type):
    entry = {}
    entry['card_number'] = cleaned_input(input(f'card number: '))

    if entry_type.lower() == 'entry':
        # Swipe In
        entry['station_in'] = cleaned_input(input(f'station: '))
        entry['swipe_in'] = cleaned_input_time(input(f'time: '))
    elif entry_type.lower() == 'exit':
        # Swipe Out
        entry['station_out'] = cleaned_input(input(f'station: '))
        entry['swipe_out'] = cleaned_input_time(input(f'time: '))

    return entry


# Calculate Average Transit time between stations
def get_average_transit(completed_entries, stations_dict):
    average_transit = -1
    sum = 0
    total_transits = 0
    sum_stations = []

    if len(completed_entries) > 0:
        for entry in completed_entries:
            for key, value in entry.items():
                if key == 'transit_stations' and value[0].lower() == stations_dict[0].lower() and value[1].lower() == stations_dict[1].lower():
                    sum_stations.append(entry['average_transit'])

    if sum_stations:
        total_transits = len(sum_stations)
        for number in sum_stations:
            sum = sum + number

    if sum and total_transits:
        average_transit = int(sum / total_transits)

    return average_transit

# Calculate average transit time
def calculate_average(time_in, time_out):
    date_format = '%Y/%m/%d %H:%M:%S'
    time_in = datetime.strptime(time_in, date_format)
    time_out = datetime.strptime(time_out, date_format)
    station_a = dt.datetime(time_in.year, time_in.month,
                            time_in.day, time_in.hour, time_in.minute, time_in.second)
    station_b = dt.datetime(time_out.year, time_out.month, time_out.day,
                            time_out.hour, time_out.minute, time_out.second)
    return int((station_b - station_a).total_seconds())

# Add or update an entry
def add_update_entry(entry, records, input_option):
    # Find current entry in the entry records
    entry_completed = False
    save_allowed = True
    entry_found = False

    for record in records:
        for key, value in record.items():
            if entry.card_number == value:
                entry_found = True
                # Card number exist in the records
                # We check if it needs to EXIT/swipe out
                if record['swipe_out'] == '' and record['entry_complete'] == False and input_option == 'exit':
                    average_transit = calculate_average(
                        record['swipe_in'], entry.swipe_out)

                    # Swipe out time should be greater than Swipe in
                    if average_transit <= 0:
                        save_allowed = False
                        print(
                            f"\n Card {entry.card_number} swipe out time {entry.swipe_out} should be ahead or NOT equal to swipe in {record['swipe_in']}")
                        break
                    else:
                        record['station_out'] = entry.station_out
                        record['swipe_out'] = entry.swipe_out
                        record['average_transit'] = average_transit
                        record['entry_complete'] = True
                        record['transit_stations'] = [
                            record['station_in'], entry.station_out]
                        entry_completed = True
                        print("\nEntry Saved!")
                        break
                elif record['swipe_out'] == '' and record['entry_complete'] == False and input_option == 'entry':
                    # Preven rider from swiping in again with pending swipe out status
                    save_allowed = False
                    print(
                        f"\nCard number {entry.card_number} found to be swiped in {record['station_in']}. Needs to be swiped out before swiping in")
                    break

    if not entry_completed and input_option == 'exit' and not entry_found:
        # Prevent swiping out without swiping in first
        print(
            f"\nCard number {entry.card_number} needs to swipe in first before swiping out")
    elif not entry_completed and save_allowed:
        records.append(entry.__dict__)
        print("\nEntry Saved!")

    # Return newly updated/added records
    return records

def get_station_entries(station_entry):
    # Return an array from the user input. i.e. "Average A B"
    station_entries = re.sub(' +', ' ', station_entry).split(" ")

    # Validate if the length entered is correct
    if len(station_entries) == 3:
        # Remove the first text which we dont really need
        del station_entries[0]
        return station_entries
    else:
        sys.exit(
            "Please enter the correct format to get the transit average. i.e. 'Average A B'")

def get_completed_entries(completed_entries, entries):
    complete_list = []

    for entry in entries:
        for key, value in entry.items():
            if key == 'entry_complete' and value == True:
                complete_list.append(entry)

    return complete_list


def main():
    print("Welcome to Transit App! Choose an option below:")

    # Array dicts to hold the record(s) of Entry and Exits
    entries = []
    completed_entries = []

    while True:
        print("\nTo swipe in type 'Entry'.\nTo swipe out type 'Exit'. \nAverage time between station, type 'Average' and followed by the two stations. i.e. 'Average A B'.\n 'q' to quit the program")
        option = input("Please type in the option you want: ")
        if cleaned_input(option).lower() == 'entry' or cleaned_input(option).lower() == 'exit':

            # Creates entry/exit record
            swipe_entry = Entry(transit_entry(cleaned_input(option)))

            if len(swipe_entry.error_messages) == 0:
                # Add/Update the current list of entries
                entries = add_update_entry(
                    swipe_entry, entries, cleaned_input(option.lower()))

                # Store those completed entries
                completed_entries = get_completed_entries(
                    completed_entries, entries)
            else:
                swipe_entry.display_error_message()

        elif 'average' in option.lower().strip():
            # #Make sure that entry is in correct format
            station_entry = get_station_entries(option)

            # #Check 'station_entry' contains the station A and B
            if station_entry and len(station_entry) > 1:
                # We retun the average transit time between stations
                average_transit = get_average_transit(
                    completed_entries, station_entry)
                print(f"\n{average_transit}")

        elif cleaned_input(option) == 'q':
            print("Good Bye!")
            sys.exit(0)
        else:
            print(f"Incorrect option '{option}' entered. Please try again")


if __name__ == '__main__':
    main()
