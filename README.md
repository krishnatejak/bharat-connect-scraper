# Bharat Connect Biller Operating Units Scraper

This project scrapes data from the Bharat Connect website about Biller Operating Units, including their downtime statistics and uptime percentages.

## Features

- Scrapes data for all Biller Operating Units
- Supports multiple year and month combinations
- Exports data to CSV format
- Includes error handling and rate limiting
- Automatically handles pagination

## Requirements

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (will be automatically managed)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/krishnatejak/bharat-connect-scraper.git
cd bharat-connect-scraper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the scraper:
```bash
python scraper.py
```

The script will:
- Open Chrome browser
- Navigate to the Bharat Connect website
- Scrape data for all available year/month combinations
- Save the data to `biller_operating_units_data.csv` in the current directory

## Output Format

The script generates a CSV file with the following columns:
- biller_operating_unit: Name of the operating unit
- year: Financial year
- month: Month of data
- downtime_count: Number of downtimes
- downtime_hhmm: Duration of downtime in HH:MM format
- uptime_percentage: Uptime percentage

## Troubleshooting

1. If you see WebDriver related errors:
   - Make sure Chrome is installed
   - The script uses webdriver_manager to handle ChromeDriver installation automatically
   - Try updating Chrome to the latest version

2. If the script fails to scrape data:
   - Check your internet connection
   - Verify the website is accessible
   - Try increasing the wait times in the script

## Rate Limiting

The script includes built-in delays to avoid overwhelming the server:
- 2-second delay between page loads
- 1-second delay between filter selections

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details