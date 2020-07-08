"""Трекер задач. Финальная работа первого курса питона."""
# Func adds events, if there is not event in dictionary, func creates it.
def add_to_dict(dictionary, day, new_event):
    if day not in dictionary:  # Add key: day and value: new_event, if event of day doesn't exist
        dictionary[day] = [new_event]
    else:  # Add event to existing day
        event_list = dictionary[day]
        event_list.append(new_event)


# Func Delete. Delete all events of day, if event_to_delete=None. Delete one event, if it exists.
def delete(dictionary, day, event_to_delete=None):
    if day not in dictionary:  # When day doesn't exist
        print('Event not found')
    elif event_to_delete is None:  # When event_to_delete is None, delete all events of day
        events = dictionary[day]
        if day in dictionary:  # Delete all events
            del dictionary[day]
            print(f'Deleted {len(events)} events')
        else:
            del dictionary[day]  # When day is empty
            print(f'Deleted 0 events')
    elif event_to_delete in dictionary[day]:  # When event exist
        events = dictionary[day]
        index = events.index(event_to_delete)
        del events[index]
        print('Deleted successfully')
    else:
        print('Event not found')


# Func Find. Search by specific data.
def find_events(dictionary, day):
    if day in dictionary:
        events = dictionary[day]
        events.sort()
        for i in events:
            print(i)
    else:
        print('Event not found')


# Func Print. Printing in the formant yyyy-mm-dd.
def print_dict(dictionary):
    for key, value in dictionary.items():
        key = key.split('-')
        year = str(key[0])
        month = str(key[1])
        day = str(key[2])
        #  Use rjust to add '0' to the beginning of the string.
        print(f"{year.rjust(4, '0')}-{month.rjust(2, '0')}-{day.rjust(2, '0')} {', '.join(value)}")
        # for i in value:
        #     print(f"{year.rjust(4, '0')}-{month.rjust(2, '0')}-{day.rjust(2, '0')} {i}")


start = input()
start = start.rstrip()
note_dict = dict()  # Empty dictionary to create data and events
if start.lower() in ('startapp', 'start'):
    while True:
        command = input()
        command = command.rstrip()
        command = command.lower()
        command = command.split()
        if 'add' in command:
            data = command[1]
            event = command[2:]
            event = ' '.join(event)
            add_to_dict(note_dict, data, event)
            continue
        elif 'del' in command:
            data = command[1]
            if len(command) == 3:
                delete(note_dict, data, command[2])
            else:
                delete(note_dict, data)
        elif 'find' in command:
            data = command[1]
            find_events(note_dict, data)
        elif 'print' in command:
            print_dict(note_dict)
        elif 'quit' in command:
            print('Quit')
            break
        elif not command:
            continue
