def readline():
    # Open serial connection to XIAO
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    time.sleep(2)  # allow XIAO to reset

    ser.flush()

    # Read one line from XIAO
    line = ser.readline().decode().strip()
    if line:
        print("XIAO says:", line)
    else:
        print("No response received from XIAO.")

    ser.close()