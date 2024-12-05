import csv
from PIL import Image, ImageDraw, ImageFont

# Function to create a well-designed Instagram post
def create_instagram_post(csv_file, symbol, output_image):
    try:
        # Read the CSV file and find the relevant row
        data = None
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Symbol'] == symbol:
                    data = row
                    break

        if not data:
            print(f"Symbol '{symbol}' not found in the CSV file.")
            return

        # Extract the necessary data
        current_price = data['Current Stock Price']
        predicted_price = data['Predicted Short Position']
        industry = data['Industry']
        market_cap = data['Market Capital']
        pb_ratio = data['P/B Ratio']

        # Create a blank image
        width, height = 1080, 1080  # Standard Instagram post dimensions
        bg_color = "#ccffcc"  # Light green background
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)

        # Define font settings
        try:
            font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_path_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            header_font = ImageFont.truetype(font_path_bold, 80)
            subheader_font = ImageFont.truetype(font_path_regular, 40)
        except:
            print("Default font will be used. Ensure TrueType fonts are installed.")
            header_font = None
            subheader_font = None

        # Add content to the image
        # Logo or company name at the top
        margin = 50
        spacing = 100
        y = margin

        draw.text((width // 2 - 200, y), symbol.upper(), font=header_font, fill="red", anchor="mm")
        y += spacing

        # A decorative divider
        divider_y = y + 10
        draw.line((margin, divider_y, width - margin, divider_y), fill="blue", width=3)
        y += spacing

        # Add stock details
        details = [
            f"Current Stock Price: ${current_price}",
            f"Predicted Stock in 5 Days: ${predicted_price}",
            f"Industry: {industry}",
            f"Market Capital: ${market_cap}",
            f"P/B Ratio: {pb_ratio}"
        ]

        for detail in details:
            draw.text((margin, y), detail, font=subheader_font, fill="black")
            y += 70

        # Save the image
        image.save(output_image)
        print(f"Image saved as '{output_image}'.")

    except FileNotFoundError:
        print(f"The file '{csv_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file = "stocks_data.csv"  # Replace with your CSV file path
symbol = input("Enter the stock symbol: ")
output_image = f"{symbol}_instagram_post.png"

create_instagram_post(csv_file, symbol, output_image)
