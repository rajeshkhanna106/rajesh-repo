





import datetime
import random
import statistics

# --- CONFIGURATION ---
# Define the latitude and longitude for the location you want to simulate.
# Default is Nanakramguda, Telangana, India.
LATITUDE = 17.4138
LONGITUDE = 78.3414


# --- SCRIPT ---

def generate_mock_weather_data(lat, lon):
    """
    Generates realistic mock weather data for the last 7 days for a given location.
    This function simulates an API response, so no API key is needed.
    """
    print(f"Generating mock weather data for Latitude: {lat}, Longitude: {lon}...")
    weather_data = []
    weather_conditions = ['clear sky', 'few clouds', 'scattered clouds', 'light rain', 'moderate rain']

    # Loop through the last 7 days to create data
    for i in range(1, 8):
        day = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')

        # Create 24 hourly records for each day
        for hour in range(24):
            # Simulate daily temperature fluctuation (cooler at night, warmer in the day)
            # This is a generic model and won't change with lat/lon in this mock script
            base_temp = 25 + (hour - 12) ** 2 / -20
            temp = round(base_temp + random.uniform(-1.5, 1.5), 2)

            # Create the timestamp for this hour
            record_time = day.replace(hour=hour, minute=0, second=0, microsecond=0)
            unix_timestamp = int(record_time.timestamp())

            # Structure the data to look like a real API response
            weather_data.append({
                'dt': unix_timestamp,
                'date_str': date_str,
                'temp': temp,
                'weather': [{'description': random.choice(weather_conditions)}]
            })

    # --- Manually insert some anomalies to test the detection ---
    # Anomaly 1: A sudden cold snap
    weather_data[20]['temp'] = 15.0
    # Anomaly 2: A sudden heat spike
    weather_data[80]['temp'] = 40.0

    print("Mock data generation complete.")
    return weather_data


def analyze_weather_data(weather_data):
    """
    Analyzes the collected weather data to find min/max temperatures and anomalies.
    """
    if not weather_data or len(weather_data) == 0:
        print("\nNo weather data to analyze.")
        return

    # --- 1. Print Weather Records ---
    print("\n" + "=" * 50)
    print("Weather Records for the Last 7 Days (Mock Data)")
    print("=" * 50)
    # To avoid printing too much, we'll just show the noon record for each day
    for record in weather_data:
        record_time = datetime.datetime.fromtimestamp(record['dt'], tz=datetime.timezone.utc)
        if record_time.hour == 12:  # Print the noon record for each day
            print(
                f"Date: {record['date_str']}, "
                f"Time: {record_time.strftime('%H:%M:%S')} UTC, "
                f"Temperature: {record['temp']}°C, "
                f"Weather: {record['weather'][0]['description']}"
            )

    # --- 2. Find Highest and Lowest Temperatures ---
    highest_temp_record = max(weather_data, key=lambda x: x['temp'])
    lowest_temp_record = min(weather_data, key=lambda x: x['temp'])

    highest_temp = highest_temp_record['temp']
    highest_temp_date = highest_temp_record['date_str']

    lowest_temp = lowest_temp_record['temp']
    lowest_temp_date = lowest_temp_record['date_str']

    print("\n" + "=" * 50)
    print("Temperature Analysis")
    print("=" * 50)
    print(f"Highest Temperature Recorded: {highest_temp}°C on {highest_temp_date}")
    print(f"Lowest Temperature Recorded: {lowest_temp}°C on {lowest_temp_date}")

    # --- 3. Spot Anomalies ---
    # An anomaly is defined as a temperature that is more than 2 standard deviations
    # from the average temperature of the period.
    all_temps = [record['temp'] for record in weather_data]

    if len(all_temps) > 1:
        mean_temp = statistics.mean(all_temps)
        std_dev = statistics.stdev(all_temps)

        # Define the anomaly threshold
        anomaly_threshold_high = mean_temp + (2 * std_dev)
        anomaly_threshold_low = mean_temp - (2 * std_dev)

        anomalies = [
            record for record in weather_data
            if record['temp'] > anomaly_threshold_high or record['temp'] < anomaly_threshold_low
        ]

        print("\n" + "=" * 50)
        print("Anomaly Detection")
        print("=" * 50)
        print(f"Average temperature over the period: {mean_temp:.2f}°C")
        print(f"Standard Deviation: {std_dev:.2f}°C")
        print(f"Anomaly thresholds: < {anomaly_threshold_low:.2f}°C or > {anomaly_threshold_high:.2f}°C")

        if anomalies:
            print("\nFound the following temperature anomalies:")
            for anomaly in anomalies:
                anomaly_time = datetime.datetime.fromtimestamp(anomaly['dt'], tz=datetime.timezone.utc)
                print(
                    f" -> Anomaly Detected on {anomaly['date_str']} at {anomaly_time.strftime('%H:%M:%S')} UTC: "
                    f"Temperature was {anomaly['temp']}°C"
                )
        else:
            print("\nNo significant temperature anomalies detected in the last 7 days.")


def main():
    """Main function to run the script."""
    # This now calls the function to generate mock data for the specified coordinates.
    weather_data = generate_mock_weather_data(LATITUDE, LONGITUDE)

    if weather_data:
        analyze_weather_data(weather_data)


if __name__ == "__main__":
    main()
