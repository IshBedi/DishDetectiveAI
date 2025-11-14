import serial
import time

FILENAME = 'names.txt'
PORT = 'COM3'   # change to your actual Arduino port
BAUD = 9600

def read_names_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("File not found:", filename)
        return []

def main():
    # Open serial ONCE so Arduino doesn't keep resetting
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # wait for Arduino to reset once
    print("Connected to Arduino on", PORT)

    last_sent_count = 0  # how many lines we've already sent

    while True:
        names = read_names_from_file(FILENAME)
        total_lines = len(names)
        print("File contents:", names)

        # Only send NEW lines that were added since last time
        if total_lines > last_sent_count:
            new_names = names[last_sent_count:]  # slice from old count to end
            print("New names to send:", new_names)

            for name in new_names:
                ser.write((name + "\n").encode('utf-8'))
                print("Sent:", name)
                time.sleep(0.5)

            # Update how many lines we've processed
            last_sent_count = total_lines
        else:
            print("No new names.")

        # Wait before checking file again
        time.sleep(3)

    # ser.close()  # not reached in this infinite loop

if __name__ == "__main__":
    main()
